# Báo Cáo Cá Nhân — Lab Day 09: Multi-Agent Orchestration

**Họ và tên:** Nguyễn Bình Thành  
**Vai trò trong nhóm:** Supervisor Owner + Worker Owner  
**Ngày nộp:** 14/04/2026  

---

## 1. Tôi phụ trách phần nào?

Tôi phụ trách Sprint 1 và Sprint 2 — toàn bộ orchestration layer và workers.

**Module/file tôi chịu trách nhiệm:**
- File chính: `graph.py`, `workers/retrieval.py`, `workers/policy_tool.py`, `workers/synthesis.py`
- Functions tôi implement: `AgentState`, `supervisor_node`, `route_decision`, `human_review_node`, `retrieval_worker_node`, `policy_tool_worker_node`, `synthesis_worker_node`, `build_graph`, `run_graph`, `save_trace`; `retrieve_dense` trong retrieval.py; `analyze_policy`, `run` trong policy_tool.py; `synthesize`, `_build_context`, `_estimate_confidence` trong synthesis.py

**Cách công việc của tôi kết nối với phần của thành viên khác:**

`AgentState` là contract trung tâm — Hiếu cần biết chính xác các fields (`mcp_tools_used`, `policy_result`, `needs_tool`) để implement MCP integration trong Sprint 3. Tôi define `worker_contracts.yaml` cùng với code để Hiếu có thể implement MCP server đúng output format mà không cần đợi tôi xong.

**Bằng chứng:**

`graph.py` line 27–55: định nghĩa `AgentState` với đầy đủ fields. `workers/retrieval.py`: standalone test chạy được với `python workers/retrieval.py`. `workers/synthesis.py`: standalone test với 2 test cases.

---

## 2. Tôi đã ra một quyết định kỹ thuật gì?

**Quyết định:** Giảm số chunk trong ChromaDB từ ~600 xuống ~150 để retrieval phân biệt được các section khác nhau.

Với 600 chunk, mọi query đều trả về kết quả gần giống nhau — retrieval không phân biệt được "refund section" với "warranty section" hay "access section". Chunk quá nhỏ và nhiều khiến embedding space bị loãng, các vector nằm gần nhau hơn và làm giảm recall precision.

**Lý do:** Chunk lớn hơn giúp mỗi chunk chứa đủ context để embedding capture được topic boundary, từ đó retrieval trả về đúng section theo từng loại câu hỏi.

**Trade-off đã chấp nhận:** Chunk lớn hơn dùng nhiều token hơn per query — chấp nhận được vì corpus nhỏ (policy manual, không phải large-scale document store).

**Bằng chứng từ trace:**

```
# Trước (600 chunks): mọi query trả về chunk từ cùng 1 section
retrieved_chunks[*].metadata.section = "general_policy"  # dù query về refund hay access

# Sau (~150 chunks): retrieval phân biệt được section
retrieved_chunks[0].metadata.section = "refund_policy"   # query về refund
retrieved_chunks[0].metadata.section = "access_policy"   # query về access
```

---

## 3. Tôi đã sửa một lỗi gì?

**Lỗi:** `synthesis_worker` không enforce `policy_applies=False` — LLM tự kết luận ngược lại với policy_result.

**Symptom:** q12 trace cho thấy `policy_result.policy_applies=False` nhưng `final_answer` nói "Khách hàng được hoàn tiền". Mâu thuẫn hoàn toàn giữa policy worker output và synthesis output.

**Root cause:** `_build_context` chỉ đưa `exceptions_found` vào context dưới dạng text list, không nói rõ kết luận cuối. LLM đọc chunks thấy điều kiện được đáp ứng (sản phẩm lỗi, trong 7 ngày, chưa kích hoạt) rồi tự kết luận "được hoàn tiền" — bỏ qua `policy_applies=False`.

**Cách sửa:** Thêm section "KẾT QUẢ PHÂN TÍCH POLICY" vào context với dòng explicit:

```python
if policy_applies is False:
    parts.append("POLICY TỪ CHỐI: Request này KHÔNG được chấp thuận.")
    parts.append("Bắt buộc phản ánh kết luận này trong answer. KHÔNG được kết luận ngược lại.")
```

**Bằng chứng trước/sau:**

```
# Trước:
final_answer: "Khách hàng được hoàn tiền trong trường hợp này..."

# Sau:
final_answer: "Yêu cầu hoàn tiền của khách hàng không được chấp thuận..."
```

---

## 4. Tôi tự đánh giá đóng góp của mình

**Tôi làm tốt nhất ở điểm nào?**

Hoàn thiện Sprint 1 và Sprint 2 cực kỳ nhanh — chỉ trong 1 giờ đã có thể bàn giao toàn bộ orchestration layer cho nhóm tiếp tục. Việc define rõ `AgentState` và `worker_contracts.yaml` từ đầu giúp Hiếu implement MCP integration mà không cần đợi hoặc hỏi về data format.

**Tôi làm chưa tốt hoặc còn yếu ở điểm nào?**

Policy worker ban đầu dùng rule-based keyword matching quá đơn giản — gây ra nhiều false positive exceptions. Nếu thiết kế LLM-only từ đầu sẽ không cần Hiếu refactor lại ở Sprint 3, tiết kiệm thời gian cho cả nhóm.

**Nhóm phụ thuộc vào tôi ở đâu?**

`AgentState` schema và `worker_contracts.yaml` — Hiếu không thể implement MCP integration nếu chưa biết `mcp_tools_used` format và `needs_tool` flag hoạt động thế nào.

**Phần tôi phụ thuộc vào thành viên khác:**

Tôi cần Hiếu implement `mcp_server.py` để test `_call_mcp_tool` trong policy worker. Trong Sprint 2, tôi dùng mock in-process call và để TODO cho Sprint 3.

---

## 5. Nếu có thêm 2 giờ, tôi sẽ làm gì?

Tôi sẽ dành thời gian hiểu sâu hơn từng phần trong hệ thống — đặc biệt là MCP server và evaluation pipeline do Hiếu implement trong Sprint 3 và Sprint 4. Hiện tại tôi còn phụ thuộc vào những phần đó và chưa hiểu hết toàn bộ luồng end-to-end. Với hiểu biết đầy đủ hơn, tôi có thể cải thiện integration giữa policy worker và MCP tool một cách tối ưu hơn thay vì chỉ để TODO mock.
