# Eval Log — q06 variant1

```
============================================================
Running variant1 for: Escalation trong sự cố P1 diễn ra như thế nào?
Config: {'retrieval_mode': 'hybrid', 'top_k_search': 10, 'top_k_select': 3, 'use_rerank': False, 'prompt_version': 'v1', 'label': 'variant1_hybrid'}
============================================================

[RAG] Query: Escalation trong sự cố P1 diễn ra như thế nào?
[RAG] Retrieved 10 candidates (mode=hybrid)
  [1] score=0.017 | it/access-control-sop.md
  [2] score=0.016 | support/sla-p1-2026.pdf
  [3] score=0.016 | support/sla-p1-2026.pdf
[RAG] After select: 3 chunks

[RAG] Prompt:
Answer only from the retrieved context below.
If the context is insufficient to answer the question, say you do not know and do not make up information.
Cite the source field (in brackets like [1]) when possible.
Keep your answer short, clear, and factual.
Respond in the same language as the question.

Question: Escalation trong sự cố P1 diễn ra như thế nào?

Context:
[1] it/access-control-sop.md | Section 4: Escalation khi cần thay đổi quyền hệ thống | score=0.02
Escalation chỉ áp dụng khi cần thay đổi quyền hệ thống ngoài quy trình thông thường.
Ví dụ: Khẩn cấp trong sự cố P1, cần cấp quyền tạm thời để fix incident.

Quy trình escalation khẩn cấp:
1. On-call IT Admin có thể cấp quyền tạm thời (max 24 giờ) sau khi được Tech Lead phê duyệt bằng lời.
2. Sau 24 giờ, phải có ticket chính thức hoặc quyền bị thu hồi tự động.
3. Mọi quyền tạm thời phải được ghi log vào hệ thống Security Audit.

[2] support/sla-p1-2026.pdf | Phần 5: Lịch sử phiên bản | score=0.02
v2026.1 (2026-01-15): Cập nhật SLA P1 resolution từ 6 giờ xuống 4 giờ.
v2025.3 (2025-09-01): Thêm quy trình escalation tự động.
v2025.1 (2025-03-01): Phiên bản đầu tiên.

[3] support/sla-p1-2026.pdf | Phần 1: Định nghĩa mức độ ưu tiên | score=0.02
P1 — CRITICAL (Khẩn cấp):
Định nghĩa: Sự cố ảnh hưởng toàn bộ hệ thống production, không có workaround.
Ví dụ: Database sập, API gateway down, toàn bộ người dùng không thể đăng nhập.

P2 — HIGH (Nghiêm trọng):
Định nghĩa: Sự cố ảnh hưởng một phần hệ thống, có workaround tạm thời.
Ví dụ: Một số tính năng không hoạt động, ảnh hưởng một nhóm người dùng.

P3 — MEDIUM (Trung bình):
Định nghĩa: Lỗi ảnh hưởng không đáng kể, người dùng vẫn làm việc được.

P4 — LOW (Thấp):
Định nghĩa: Yêu cầu cải tiến, gợi ý, hoặc lỗi giao diện nhỏ.

Answer:


============================================================
FULL ANSWER:
Escalation trong sự cố P1 diễn ra như sau: On-call IT Admin có thể cấp quyền tạm thời (tối đa 24 giờ) sau khi được Tech Lead phê duyệt bằng lời. Sau 24 giờ, phải có ticket chính thức hoặc quyền sẽ bị thu hồi tự động. Tất cả quyền tạm thời phải được ghi log vào hệ thống Security Audit [1].

SOURCES: ['it/access-control-sop.md', 'support/sla-p1-2026.pdf']

============================================================
SCORING:
  Faithfulness  : 5 — Every claim in the answer is fully supported by the retrieved context.
  Relevance     : 5 — The answer directly and completely explains the escalation process for P1 incidents.
  Context Recall: 5 — Retrieved: 1/1 expected sources
  Completeness  : 1 — The model answer does not address the automatic escalation of P1 tickets to a Senior Engineer within 10 minutes, which is a key point in the expected answer.
```
