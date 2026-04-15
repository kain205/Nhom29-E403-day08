# Grading Reference — Lab Day 10

**Nhóm:** Nhóm 29 — E403  
**run_id:** sprint2-final  
**Ngày chạy:** 2026-04-15  
**Collection:** `day10_kb`  
**top_k:** 5

---

## Kết quả grading_run.jsonl

| id | question | top1_doc_id | contains_expected | hits_forbidden | top1_doc_matches | Đạt tiêu chí? |
|----|----------|-------------|-------------------|----------------|------------------|---------------|
| `gq_d10_01` | Khách hàng có bao nhiêu ngày làm việc để yêu cầu hoàn tiền kể từ khi xác nhận đơn hàng? | `policy_refund_v4` | ✅ true | ✅ false | — | ✅ Pass |
| `gq_d10_02` | SLA phản hồi đầu tiên cho ticket P1 là bao lâu? | `sla_p1_2026` | ✅ true | — | — | ✅ Pass |
| `gq_d10_03` | Theo chính sách nghỉ phép hiện hành năm 2026, nhân viên dưới 3 năm kinh nghiệm được bao nhiêu ngày phép năm? | `hr_leave_policy` | ✅ true | ✅ false | ✅ true | ✅ Pass |

**Tổng: 3/3 câu đạt đủ tiêu chí grading.**

---

## Raw JSONL

```jsonl
{"id": "gq_d10_01", "question": "Khách hàng có bao nhiêu ngày làm việc để yêu cầu hoàn tiền kể từ khi xác nhận đơn hàng?", "top1_doc_id": "policy_refund_v4", "contains_expected": true, "hits_forbidden": false, "top1_doc_matches": null, "top_k_used": 5, "grading_criteria": ["contains_expected=true", "hits_forbidden=false"]}
{"id": "gq_d10_02", "question": "SLA phản hồi đầu tiên cho ticket P1 là bao lâu?", "top1_doc_id": "sla_p1_2026", "contains_expected": true, "hits_forbidden": false, "top1_doc_matches": null, "top_k_used": 5, "grading_criteria": ["contains_expected=true"]}
{"id": "gq_d10_03", "question": "Theo chính sách nghỉ phép hiện hành năm 2026, nhân viên dưới 3 năm kinh nghiệm được bao nhiêu ngày phép năm?", "top1_doc_id": "hr_leave_policy", "contains_expected": true, "hits_forbidden": false, "top1_doc_matches": true, "top_k_used": 5, "grading_criteria": ["contains_expected=true", "hits_forbidden=false", "top1_doc_matches=true"]}
```

---

## Điểm theo SCORING.md

| Tiêu chí | Điểm tối đa | Kết quả |
|----------|-------------|---------|
| JSONL tồn tại, đúng 3 dòng, JSON hợp lệ | 2 | ✅ 2/2 |
| `gq_d10_01`: `contains_expected=true` và `hits_forbidden=false` | 4 | ✅ 4/4 |
| `gq_d10_02`: `contains_expected=true` | 3 | ✅ 3/3 |
| `gq_d10_03`: `contains_expected=true`, `hits_forbidden=false`, `top1_doc_matches=true` | 3 | ✅ 3/3 |
| **Tổng grading** | **12** | **12/12** |

---

## Pipeline state tại thời điểm grading

```
run_id=sprint2-final
raw_records=13 | cleaned_records=6 | quarantine_records=7
expectations: 8/8 OK (không có halt)
embed_upsert count=6 collection=day10_kb
freshness_check=FAIL (age=122.3h, SLA=24h — data snapshot cũ, expected)
PIPELINE_OK
```

**Lưu ý freshness FAIL:** bình thường — CSV mẫu có `exported_at=2026-04-10T08:00:00` cố định. Không ảnh hưởng tính đúng đắn của grading.
