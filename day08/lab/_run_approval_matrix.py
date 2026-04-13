import os
from dotenv import load_dotenv
load_dotenv()

from rag_answer import retrieve_dense, retrieve_sparse, retrieve_hybrid, build_context_block, call_llm, build_grounded_prompt

QUERY = "Approval Matrix để cấp quyền hệ thống là tài liệu nào?"
TOP_K_ALL = 10
TOP_K_SELECT = 3

def print_all_results(label, chunks):
    print(f"\n{'='*60}")
    print(f"Strategy: {label}")
    print(f"{'='*60}")
    print(f"\n--- Tất cả {len(chunks)} kết quả tìm được ---")
    for i, c in enumerate(chunks, 1):
        meta = c['metadata']
        print(f"  [{i}] score={c['score']:.4f} | {meta.get('source','?')} | {meta.get('section','')}")
        print(f"       {c['text'][:120].replace(chr(10), ' ')}...")

    top3 = chunks[:TOP_K_SELECT]
    print(f"\n--- Top {TOP_K_SELECT} được chọn vào prompt ---")
    for i, c in enumerate(top3, 1):
        meta = c['metadata']
        print(f"  [{i}] score={c['score']:.4f} | {meta.get('source','?')} | {meta.get('section','')}")
        print(f"       {c['text'][:200].replace(chr(10), ' ')}...")

    context_block = build_context_block(top3)
    prompt = build_grounded_prompt(QUERY, context_block, version="v1")
    answer = call_llm(prompt)
    print(f"\n--- Answer ---")
    print(answer)


print(f"Query: {QUERY}\n")

# Dense
dense_results = retrieve_dense(QUERY, top_k=TOP_K_ALL)
print_all_results("DENSE", dense_results)

# Sparse
sparse_results = retrieve_sparse(QUERY, top_k=TOP_K_ALL)
print_all_results("SPARSE (BM25)", sparse_results)

# Hybrid
hybrid_results = retrieve_hybrid(QUERY, top_k=TOP_K_ALL)
print_all_results("HYBRID (Dense + BM25 + RRF)", hybrid_results)
