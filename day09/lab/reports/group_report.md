# Báo Cáo Nhóm — Lab Day 09: Multi-Agent Orchestration

**Tên nhóm:** Nhóm 29 — E403
**Thành viên:**

| Tên | Vai trò | Sprint |
|-----|---------|--------|
| Nguyễn Bình Thành | Supervisor Owner + Worker Owner | 1, 2 |
| Hàn Quang Hiếu | MCP Owner + Trace & Docs Owner | 3, 4 |

**Repo:** https://github.com/kain205/Nhom29-E403-day08

---

## 1. Kiến trúc nhóm đã xây dựng

Hệ thống gồm 1 Supervisor và 3 Workers chạy tuần tự theo graph: `supervisor_node` → `route_decision` → `[retrieval_worker | policy_tool_worker | human_review]` → `synthesis_worker`. Supervisor đọc task, quyết định route dựa vào keyword matching, ghi `route_reason` vào `AgentState`. Mỗi worker nhận state, xử lý phần việc của mình, ghi output trở lại state để worker tiếp theo dùng. Toàn bộ execution path được ghi vào trace JSON.

**Routing logic cốt lõi — keyword-based, priority order:**

- `policy_keywords` ("hoàn tiền", "refund", "flash sale", "level 2/3", "cấp quyền", "store credit", ...) → `policy_tool_worker`
- `sla_keywords` ("p1", "sla", "ticket", "escalation", "on-call", ...) → `retrieval_worker`
- `err-xxx` không có keyword khác → `human_review`
- Mặc định → `retrieval_worker`

Khi route là `policy_tool_worker`: `retrieval_worker` chạy trước để lấy context, sau đó `policy_tool_worker` phân tích dựa trên chunks đã có.

**MCP tools đã tích hợp (`mcp_server.py`):**

- `search_kb(query, top_k)` — tìm kiếm knowledge base qua ChromaDB, trả về chunks + sources
- `get_ticket_info(ticket_id)` — tra cứu thông tin ticket mock (status, priority, assignee)
- `check_access_permission(access_level, requester_role, is_emergency)` — kiểm tra điều kiện cấp quyền và emergency bypass
- `create_ticket(title, priority, description)` — tạo ticket mới (mock)

Ngoài ra có `mcp_server_http.py` — FastAPI server thật chạy tại `localhost:8080`, expose toàn bộ tools qua HTTP với Swagger UI.

---

## 2. Quyết định kỹ thuật quan trọng nhất

**Quyết định:** Chuyển `policy_tool_worker` từ rule-based sang LLM-only với dynamic MCP schema injection.

**Bối cảnh vấn đề:**

Sprint 2 implement `analyze_policy` theo rule-based: dùng `"flash sale" in context_text`, `"kỹ thuật số" in context_text` để detect exceptions. Khi chạy eval, q02 ("hoàn tiền trong bao nhiêu ngày?") trả về 4 exceptions và `hitl_triggered=True` mặc dù đây chỉ là câu hỏi thông tin. Root cause: chunks từ `policy_refund_v4.txt` luôn chứa các cụm từ "Flash Sale", "kỹ thuật số" vì đó là nội dung doc — mọi câu retrieve được doc này đều bị dính exception.

Song song đó, khi tích hợp MCP, LLM gọi `check_access_permission` với `{"level": "2", "role": "contractor"}` — sai tên parameter và sai kiểu (string thay vì integer). Nguyên nhân: schema được hardcode trong prompt, không sync với `mcp_server.py`.

**Các phương án đã cân nhắc:**

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|-----------|
| Fix rule-based (thêm negative conditions) | Đơn giản, không thêm LLM call | Fragile — thêm doc mới là phải sửa rules, dễ miss edge case |
| LLM-only với schema hardcode trong prompt | LLM hiểu ngữ cảnh tốt hơn rule | Schema trong prompt drift so với mcp_server.py khi thêm tool |
| LLM-only với `_get_mcp_tool_schemas()` động | Schema luôn sync với server, extensible | Thêm 1 function call `list_tools()` mỗi lần gọi LLM |

**Phương án đã chọn:** LLM-only + dynamic schema injection từ `list_tools()`.

Lý do: đây đúng tinh thần MCP — server là source of truth cho tool schemas, không phải prompt. Khi thêm tool mới vào `mcp_server.py`, LLM tự biết mà không cần sửa prompt hay worker code.

**Bằng chứng từ trace — trước và sau fix (q02):**

```
# Trước (rule-based):
policy_result.exceptions_found: [flash_sale, digital_product, activated, mã_giảm_giá]
confidence: 0.36, hitl_triggered: True

# Sau (LLM-only + prompt rule "câu hỏi thông tin → policy_applies=null, exceptions_found=[]"):
policy_result.exceptions_found: []
policy_result.policy_applies: null
explanation: "Câu hỏi chỉ yêu cầu thông tin về thời gian hoàn tiền..."
confidence: 0.56, hitl_triggered: False
```

---

## 3. Kết quả grading questions

Pipeline chạy `python eval_trace.py --grading` với 10 câu từ `grading_questions.json`. Kết quả được chấm dựa trên rubric trong `SCORING.md`, judge bằng `claude-sonnet-4-6`.

**Tổng điểm raw ước tính: 87 / 96**

| ID | Điểm | Nhận xét tóm tắt |
|----|------|-----------------|
| gq01 | 7/10 | Thiếu đối tượng escalation (Senior Engineer) |
| gq02 | 10/10 | Abstain đúng — nhận ra thiếu doc v3, không hallucinate |
| gq03 | 10/10 | 3 người phê duyệt đúng, thứ tự đúng |
| gq04 | 6/6 | 110% store credit đúng |
| gq05 | 8/8 | "Tự động escalate lên Senior Engineer" — chuẩn |
| gq06 | 8/8 | Probation + 2 ngày/tuần + Team Lead đúng |
| gq07 | 10/10 | Abstain đúng, không bịa con số phạt, HITL triggered |
| gq08 | 8/8 | 90 ngày, 7 ngày cảnh báo, cite đúng nguồn |
| gq09 | 11/16 | Thiếu "escalate → Senior Engineer" và "Level 2 không cần IT Security" |
| gq10 | 9/10 | Flash Sale override lỗi nhà sản xuất đúng |

**Câu pipeline xử lý tốt nhất:** gq02, gq07 — cả hai là câu trap "abstain khi thiếu thông tin". LLM-only policy worker với rule *"câu hỏi thông tin hoặc thiếu tài liệu đúng version → policy_applies=null, exceptions_found=[]"* xử lý đúng cả hai. Đây là điểm cải tiến lớn nhất so với rule-based ban đầu.

**Câu pipeline partial:** gq09 (11/16) — cross-doc multi-hop cần tổng hợp SLA escalation procedure + Level 2 access conditions. Synthesis tổng hợp đủ từ context nhưng thiếu 2 kết luận tường minh: (1) escalation target là Senior Engineer (không phải Lead Engineer), (2) Level 2 không cần IT Security.

**gq07 (abstain):** HITL triggered với `confidence=0.30`. Synthesis nhận diện không có thông tin về mức phạt tài chính trong tài liệu và trả lời "Không đủ thông tin trong tài liệu nội bộ" — không bịa con số. Đúng behavior.

**gq09 (multi-hop):** Trace ghi đúng 2 workers (`retrieval_worker` → `policy_tool_worker` → `synthesis_worker`) và 2 MCP tools (`check_access_permission`, `get_ticket_info`). Route reason ghi rõ `risk_high=True (triggered by: ['emergency', '2am'])`.

---

## 4. So sánh Day 08 vs Day 09 — Điều nhóm quan sát được

| Metric | Day 08 | Day 09 | Delta |
|--------|--------|--------|-------|
| Avg latency | ~2000ms (est.) | 5883ms | **+3883ms** |
| Routing visibility | Không có | Có `route_reason` mọi trace | N/A |
| Debug time (ước tính) | ~20 phút | ~5 phút | -15 phút |
| MCP/tool capability | Không có | 4 tools qua MCP | N/A |
| Abstain/anti-hallucination | Không có cơ chế | `confidence < 0.4 → hitl_triggered` | N/A |

**Metric thay đổi rõ nhất:** Latency tăng gấp ~3x (+3883ms). Nguyên nhân trực tiếp: policy query gọi 2–4 LLM calls (policy analysis round 1 + optional round 2 + synthesis) thay vì 1 call. Với MCP: thêm 1–2 LLM rounds nữa, tổng có thể lên 11–13 giây (q15 trong test set: 13401ms).

**Điều nhóm bất ngờ nhất:** Sau khi có trace rõ ràng, debug một bug phức tạp (false positive exceptions của q02) chỉ mất ~10 phút. Không cần đọc code — chỉ cần nhìn `policy_result.exceptions_found` và `llm_used` trong trace là biết ngay lỗi ở đâu. Day 08 không có cơ chế này.

**Trường hợp multi-agent không giúp ích:** Simple queries (gq04, gq06, gq08) — retrieval + generate là đủ, không cần policy check. Overhead supervisor + worker routing thêm ~2000ms mà không cải thiện accuracy.

---

## 5. Phân công và đánh giá nhóm

**Phân công thực tế:**

| Thành viên | Phần đã làm | Sprint |
|------------|-------------|--------|
| Nguyễn Bình Thành | `graph.py` (supervisor routing, AgentState, worker wiring); `workers/retrieval.py` (OpenAI embeddings, ChromaDB search); `workers/policy_tool.py` (base structure, `run()` entry point, rule-based v1); `workers/synthesis.py` (grounded LLM prompt, confidence score); `build_index.py` (chunk 400/overlap 60); contracts update | 1, 2 |
| Hàn Quang Hiếu | `mcp_server.py` (4 tools, `dispatch_tool`, `list_tools`); `mcp_server_http.py` (FastAPI HTTP server, bonus); refactor `analyze_policy` sang LLM-only + dynamic schema injection; `eval_trace.py`; chạy 15 test questions + 10 grading questions; `docs/` templates; individual reports | 3, 4 |

**Điểm nhóm làm tốt:** Phối hợp mượt mà, không có vấn đề trong giao tiếp — mỗi người đều hiểu ý nhau và rõ phần mình làm. Dù chỉ 2 người với 4 sprints, nhóm vẫn kịp thời gian demo trước lớp đúng deadline.

**Điểm nhóm làm chưa tốt:** Chưa đạt max score — cụ thể ở gq01 và gq09: synthesis mô tả step escalation là "Lead Engineer phân công engineer xử lý" thay vì "tự động escalate lên Senior Engineer", và gq09 thiếu kết luận tường minh "Level 2 không cần IT Security". Cả hai lỗi xuất phát từ cùng nguyên nhân: synthesis prompt không enforce rõ khi tổng hợp SLA escalation path.

**Nếu làm lại:** Tổ chức để 2 người làm song song hơn thay vì tuần tự — hiện tại Thành phải hoàn thành Sprint 1+2 trước rồi mới đưa cho Hiếu bắt đầu Sprint 3+4. Nếu Hiếu có thể chuẩn bị MCP server interface và mock tools song song với Sprint 2, tổng thời gian sẽ ngắn hơn và có nhiều thời gian hơn để review output trước khi submit.

---

## 6. Nếu có thêm 1 ngày, nhóm sẽ làm gì?

Xem lại kết quả private test, tìm ra pattern lỗi, rồi debug từ đó. Cụ thể: lỗi gq01 và gq09 cùng liên quan đến SLA escalation — synthesis không kết luận rõ "escalate lên Senior Engineer". Nếu có thêm ngày, sẽ điều chỉnh synthesis prompt để enforce explicit conclusion khi tổng hợp SLA flow, chạy lại grading và verify fix trước khi submit.

---

*File: `reports/group_report.md` · Commit sau 18:00 được phép theo SCORING.md*
