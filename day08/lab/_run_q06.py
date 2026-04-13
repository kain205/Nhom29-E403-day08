import os
from dotenv import load_dotenv
load_dotenv()

from rag_answer import rag_answer
from eval import (
    score_faithfulness, score_answer_relevance,
    score_context_recall, score_completeness,
    VARIANT1_CONFIG,
)

q = {
    "id": "q06",
    "question": "Escalation trong sự cố P1 diễn ra như thế nào?",
    "expected_answer": "Ticket P1 tự động escalate lên Senior Engineer nếu không có phản hồi trong 10 phút sau khi tạo ticket.",
    "expected_sources": ["support/sla-p1-2026.pdf"],
    "expected_abstain": False,
    "category": "SLA",
}

config = VARIANT1_CONFIG
print("=" * 60)
print(f"Running variant1 for: {q['question']}")
print(f"Config: {config}")
print("=" * 60)

result = rag_answer(
    query=q["question"],
    retrieval_mode=config["retrieval_mode"],
    top_k_search=config["top_k_search"],
    top_k_select=config["top_k_select"],
    use_rerank=config["use_rerank"],
    prompt_version=config["prompt_version"],
    verbose=True,
)

print("\n" + "=" * 60)
print("FULL ANSWER:")
print(result["answer"])
print("\nSOURCES:", result["sources"])

print("\n" + "=" * 60)
print("SCORING:")
faith = score_faithfulness(result["answer"], result["chunks_used"], expected_abstain=False)
rel   = score_answer_relevance(q["question"], result["answer"], expected_abstain=False)
rec   = score_context_recall(result["chunks_used"], q["expected_sources"])
comp  = score_completeness(q["question"], result["answer"], q["expected_answer"])

print(f"  Faithfulness  : {faith['score']} — {faith['notes']}")
print(f"  Relevance     : {rel['score']} — {rel['notes']}")
print(f"  Context Recall: {rec['score']} — {rec['notes']}")
print(f"  Completeness  : {comp['score']} — {comp['notes']}")
