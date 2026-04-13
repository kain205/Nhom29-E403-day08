"""
test_question.py — Quick test for a single question across one or all strategies.

Usage:
  # Test one question against all strategies
  python test_question.py --question "SLA xử lý ticket P1 là bao lâu?"

  # Test against a specific strategy
  python test_question.py --question "SLA xử lý ticket P1 là bao lâu?" --strategy baseline

  # Use a question ID from test_questions.json
  python test_question.py --id q01

  # Use a question ID against a specific strategy
  python test_question.py --id q01 --strategy variant2

  # Disable log saving
  python test_question.py --id q01 --no-log

Available strategies: baseline, variant1, variant2, variant3, variant4
Log is saved to: results/test_run_log.txt  (appended each run)
"""

import argparse
import json
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Import configs and pipeline ──────────────────────────────────────────────
from eval import CONFIG_MAP, ALL_CONFIGS
from rag_answer import rag_answer, build_context_block, build_grounded_prompt

TEST_QUESTIONS_PATH = Path(__file__).parent / "data" / "test_questions.json"
LOG_PATH = Path(__file__).parent / "results" / "test_run_log.txt"


def load_question_by_id(qid: str) -> dict | None:
    with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    return next((q for q in questions if q["id"] == qid), None)


def _write_log(text: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(text)


def run_single(query: str, config: dict, expected: dict | None = None, save_log: bool = True) -> None:
    label = config["label"]

    # ── Run pipeline with verbose to capture retrieval info ──────────────────
    from rag_answer import retrieve_dense, retrieve_sparse, retrieve_hybrid, rerank

    retrieval_mode = config["retrieval_mode"]
    top_k_search   = config["top_k_search"]
    top_k_select   = config["top_k_select"]
    use_rerank     = config["use_rerank"]
    prompt_version = config["prompt_version"]

    try:
        # Step 1: retrieve
        if retrieval_mode == "dense":
            candidates = retrieve_dense(query, top_k=top_k_search)
        elif retrieval_mode == "sparse":
            candidates = retrieve_sparse(query, top_k=top_k_search)
        else:
            candidates = retrieve_hybrid(query, top_k=top_k_search)

        # Step 2: rerank / select
        if use_rerank:
            chunks_used = rerank(query, candidates, top_k=top_k_select)
        else:
            chunks_used = candidates[:top_k_select]

        # Step 3: build prompt
        context_block = build_context_block(chunks_used)
        prompt = build_grounded_prompt(query, context_block, version=prompt_version)

        # Step 4: get answer via full pipeline (reuses same call cleanly)
        result = rag_answer(
            query=query,
            retrieval_mode=retrieval_mode,
            top_k_search=top_k_search,
            top_k_select=top_k_select,
            use_rerank=use_rerank,
            prompt_version=prompt_version,
            verbose=False,
        )
        answer = result["answer"]
        sources = result["sources"]

    except Exception as e:
        candidates = []
        chunks_used = []
        prompt = ""
        answer = f"ERROR: {e}"
        sources = []

    # ── Build log/display block ───────────────────────────────────────────────
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Strategy  : {label}")
    lines.append(f"{'='*60}")

    lines.append(f"\n[RAG] Query: {query}")
    lines.append(f"[RAG] Retrieved {len(candidates)} candidates (mode={retrieval_mode})")
    for i, c in enumerate(candidates[:3]):
        lines.append(f"  [{i+1}] score={c.get('score', 0):.3f} | {c['metadata'].get('source', '?')}")
    lines.append(f"[RAG] After select: {len(chunks_used)} chunks")

    lines.append(f"\n[RAG] Prompt:\n{prompt}")

    lines.append(f"\nAnswer: {answer}")
    lines.append(f"Sources: {sources}")

    if expected:
        lines.append(f"\nExpected : {expected.get('expected_answer', 'N/A')}")
        exp_src = expected.get("expected_sources", [])
        if exp_src:
            lines.append(f"Exp.Src  : {exp_src}")

    block = "\n".join(lines) + "\n"

    # Print to console
    print(block)

    # Save to log
    if save_log:
        _write_log(block)


def main():
    parser = argparse.ArgumentParser(
        description="Test a question against one or all RAG strategies.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Question input — one of these is required
    q_group = parser.add_mutually_exclusive_group(required=True)
    q_group.add_argument("--question", "-q", type=str, help="Question text to test")
    q_group.add_argument("--id", type=str, help="Question ID from test_questions.json (e.g. q01)")

    parser.add_argument(
        "--strategy", "-s",
        choices=list(CONFIG_MAP.keys()),
        default=None,
        help=(
            "Strategy to run. Omit to run ALL strategies.\n"
            "  baseline  — dense retrieval + simple prompt\n"
            "  variant1  — hybrid retrieval + simple prompt\n"
            "  variant2  — dense retrieval + nuanced prompt\n"
            "  variant3  — hybrid retrieval + nuanced prompt\n"
            "  variant4  — hybrid + rerank + nuanced prompt\n"
        ),
    )
    parser.add_argument(
        "--no-log", action="store_true",
        help="Skip saving to results/test_run_log.txt",
    )

    args = parser.parse_args()
    save_log = not args.no_log

    # ── Resolve question ──────────────────────────────────────────────────────
    expected_meta = None

    if args.id:
        q_data = load_question_by_id(args.id)
        if not q_data:
            print(f"Question ID '{args.id}' not found in test_questions.json")
            return
        query = q_data["question"]
        expected_meta = q_data
        print(f"Loaded [{args.id}] — category: {q_data.get('category', '?')}")
    else:
        query = args.question

    # ── Resolve strategy/strategies ───────────────────────────────────────────
    configs = [CONFIG_MAP[args.strategy]] if args.strategy else ALL_CONFIGS

    # ── Write run header to log ───────────────────────────────────────────────
    if save_log:
        header = (
            f"\n{'#'*60}\n"
            f"# TEST RUN  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"# Query     : {query}\n"
            f"# Strategies: {args.strategy or 'all'}\n"
            f"{'#'*60}\n"
        )
        _write_log(header)
        print(f"Logging to: {LOG_PATH}")

    print(f"\n{'='*60}")
    print(f"Running {len(configs)} strategy/strategies")
    print(f"{'='*60}")

    for config in configs:
        run_single(query, config, expected=expected_meta, save_log=save_log)

    print(f"\n{'='*60}")
    print("Done." + (f" Log saved → {LOG_PATH}" if save_log else ""))


if __name__ == "__main__":
    main()
