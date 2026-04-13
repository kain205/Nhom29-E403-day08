# Eval Run Log

```
============================================================
Sprint 4: Evaluation & Scorecard  [--run all]
============================================================

Loading test questions từ: D:\Code\Github\Nhom29-E403-day08\day08\lab\data\test_questions.json
Tìm thấy 10 câu hỏi
  [q01] SLA xử lý ticket P1 là bao lâu? (SLA)
  [q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày? (Refund)
  [q03] Ai phải phê duyệt để cấp quyền Level 3? (Access Control)
  ...

--- Chạy: baseline_dense ---

======================================================================
Chạy scorecard: baseline_dense
Config: {'retrieval_mode': 'dense', 'top_k_search': 10, 'top_k_select': 3, 'use_rerank': False, 'prompt_version': 'v1', 'label': 'baseline_dense'}
======================================================================

[q01] SLA xử lý ticket P1 là bao lâu?
  Answer: SLA xử lý ticket P1 là 4 giờ cho việc khắc phục (resolution) và phản hồi ban đầu trong 15 phút kể từ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?
  Answer: Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng [1]...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q03] Ai phải phê duyệt để cấp quyền Level 3?
  Answer: Để cấp quyền Level 3, cần phê duyệt của Line Manager, IT Admin và IT Security [1]....
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q04] Sản phẩm kỹ thuật số có được hoàn tiền không?
  Answer: Sản phẩm kỹ thuật số không được hoàn tiền, trừ khi có lỗi do nhà sản xuất và đáp ứng các điều kiện k...
  Faithful: 4 | Relevant: 5 | Recall: 5 | Complete: 3

[q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai?
  Answer: Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn cần liên hệ IT Helpdesk hoặc tự...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q06] Escalation trong sự cố P1 diễn ra như thế nào?
  Answer: Escalation trong sự cố P1 diễn ra như sau:

1. On-call engineer nhận alert hoặc ticket và xác nhận s...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q07] Approval Matrix để cấp quyền hệ thống là tài liệu nào?
  Answer: Approval Matrix để cấp quyền hệ thống là tài liệu quy định quy trình cấp phép truy cập vào các hệ th...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 2

[q08] Nhân viên được làm remote tối đa mấy ngày mỗi tuần?
  Answer: Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi hoàn thành thời gian thử việc [1]....
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q09] ERR-403-AUTH là lỗi gì và cách xử lý?
  Answer: ERR-403-AUTH là lỗi liên quan đến quyền truy cập, thường xảy ra khi người dùng không có quyền hợp lệ...
  Faithful: 5 | Relevant: 5 | Recall: None | Complete: 2

[q10] Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?
  Answer: Không có thông tin nào trong bối cảnh đề cập đến quy trình hoàn tiền khẩn cấp cho khách hàng VIP. Tô...
  Faithful: 5 | Relevant: 1 | Recall: 5 | Complete: 1

Average faithfulness: 4.90

Average relevance: 4.60

Average context_recall: 5.00

Average completeness: 3.80
Scorecard lưu tại: D:\Code\Github\Nhom29-E403-day08\day08\lab\results\scorecard_baseline_dense.md

--- Chạy: variant1_hybrid ---

======================================================================
Chạy scorecard: variant1_hybrid
Config: {'retrieval_mode': 'hybrid', 'top_k_search': 10, 'top_k_select': 3, 'use_rerank': False, 'prompt_version': 'v1', 'label': 'variant1_hybrid'}
======================================================================

[q01] SLA xử lý ticket P1 là bao lâu?
  Answer: SLA xử lý ticket P1 là 15 phút cho phản hồi ban đầu và 4 giờ cho xử lý và khắc phục [1]....
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?
  Answer: Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng [1]...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q03] Ai phải phê duyệt để cấp quyền Level 3?
  Answer: Để cấp quyền Level 3, cần có sự phê duyệt của Line Manager, IT Admin và IT Security [2]....
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q04] Sản phẩm kỹ thuật số có được hoàn tiền không?
  Answer: Sản phẩm kỹ thuật số không được hoàn tiền, trừ khi có lỗi do nhà sản xuất và đáp ứng các điều kiện k...
  Faithful: 4 | Relevant: 5 | Recall: 5 | Complete: 3

[q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai?
  Answer: Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, liên hệ IT Helpdesk hoặc tự reset q...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q06] Escalation trong sự cố P1 diễn ra như thế nào?
  Answer: Escalation trong sự cố P1 diễn ra như sau: On-call IT Admin có thể cấp quyền tạm thời (tối đa 24 giờ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 1

[q07] Approval Matrix để cấp quyền hệ thống là tài liệu nào?
  Answer: Approval Matrix để cấp quyền hệ thống là tài liệu quy định quy trình cấp phép truy cập vào các hệ th...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 2

[q08] Nhân viên được làm remote tối đa mấy ngày mỗi tuần?
  Answer: Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi hoàn thành thời gian thử việc, và lịch remo...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q09] ERR-403-AUTH là lỗi gì và cách xử lý?
  Answer: Tôi không biết....
  Faithful: 1 | Relevant: 1 | Recall: None | Complete: 1

[q10] Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?
  Answer: Không có thông tin cụ thể nào trong bối cảnh về việc quy trình hoàn tiền cho khách hàng VIP có khác ...
  Faithful: 5 | Relevant: 1 | Recall: 5 | Complete: 1

Average faithfulness: 4.50

Average relevance: 4.20

Average context_recall: 5.00

Average completeness: 3.30
Scorecard lưu tại: D:\Code\Github\Nhom29-E403-day08\day08\lab\results\scorecard_variant1_hybrid.md

--- Chạy: variant3_nuanced_abstain ---

======================================================================
Chạy scorecard: variant3_nuanced_abstain
Config: {'retrieval_mode': 'dense', 'top_k_search': 10, 'top_k_select': 3, 'use_rerank': False, 'prompt_version': 'v3', 'label': 'variant3_nuanced_abstain'}
======================================================================

[q01] SLA xử lý ticket P1 là bao lâu?
  Answer: SLA xử lý ticket P1 bao gồm các thời gian sau: phản hồi ban đầu trong vòng 15 phút kể từ khi ticket ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?
  Answer: Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng [1]...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q03] Ai phải phê duyệt để cấp quyền Level 3?
  Answer: Để cấp quyền Level 3 (Elevated Access), yêu cầu phải được phê duyệt bởi Line Manager, IT Admin và IT...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q04] Sản phẩm kỹ thuật số có được hoàn tiền không?
  Answer: Sản phẩm thuộc danh mục hàng kỹ thuật số (license key, subscription) không được hoàn tiền. Điều này ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai?
  Answer: Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn có thể liên hệ IT Helpdesk hoặc...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q06] Escalation trong sự cố P1 diễn ra như thế nào?
  Answer: Trong sự cố P1, quy trình escalation diễn ra như sau: Nếu không có phản hồi trong 10 phút, ticket sẽ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q07] Approval Matrix để cấp quyền hệ thống là tài liệu nào?
  Answer: Không đủ dữ liệu để trả lời câu hỏi này. Bạn có thể liên hệ IT Helpdesk để biết thêm thông tin. 

So...
  Faithful: 1 | Relevant: 1 | Recall: 5 | Complete: 1

[q08] Nhân viên được làm remote tối đa mấy ngày mỗi tuần?
  Answer: Nhân viên sau probation period có thể làm remote tối đa 2 ngày/tuần. Tuy nhiên, lịch remote phải đượ...
  Faithful: 5 | Relevant: 5 | Recall: 5 | Complete: 5

[q09] ERR-403-AUTH là lỗi gì và cách xử lý?
  Answer: Không đủ dữ liệu để trả lời câu hỏi này. Bạn có thể liên hệ IT Helpdesk để được hỗ trợ thêm. 

Sourc...
  Faithful: 5 | Relevant: 5 | Recall: None | Complete: 4

[q10] Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?
  Answer: Quy trình hoàn tiền không có thông tin cụ thể về khách hàng VIP. Tuy nhiên, quy trình xử lý yêu cầu ...
  Faithful: 5 | Relevant: 2 | Recall: 5 | Complete: 5

Average faithfulness: 4.60

Average relevance: 4.30

Average context_recall: 5.00

Average completeness: 4.50
Scorecard lưu tại: D:\Code\Github\Nhom29-E403-day08\day08\lab\results\scorecard_variant3_nuanced_abstain.md

================================================================================
Comparison: baseline_dense vs variant1_hybrid vs variant3_nuanced_abstain
================================================================================
Metric                baseline_densevariant1_hybridvariant3_nuanced_abstain  Δvariant1  Δvariant3
-------------------------------------------------------------------------------------------------
faithfulness                  4.90        4.50        4.60     -0.40     -0.30
relevance                     4.60        4.20        4.30     -0.40     -0.30
context_recall                5.00        5.00        5.00     +0.00     +0.00
completeness                  3.80        3.30        4.50     -0.50     +0.70

Câu     baseline_dense        variant1_hybrid       variant3_nuanced_a    Best        
--------------------------------------------------------------------------------------
q01     5/5/5/5               5/5/5/5               5/5/5/5               Tie         
q02     5/5/5/5               5/5/5/5               5/5/5/5               Tie         
q03     5/5/5/5               5/5/5/5               5/5/5/5               Tie         
q04     4/5/5/3               4/5/5/3               5/5/5/5               variant3_nuanced_abstain
q05     5/5/5/5               5/5/5/5               5/5/5/5               Tie         
q06     5/5/5/5               5/5/5/1               5/5/5/5               baseline_dense
q07     5/5/5/2               5/5/5/2               1/1/5/1               baseline_dense
q08     5/5/5/5               5/5/5/5               5/5/5/5               Tie         
q09     5/5/None/2            1/1/None/1            5/5/None/4            variant3_nuanced_abstain
q10     5/1/5/1               5/1/5/1               5/2/5/5               variant3_nuanced_abstain

Kết quả đã lưu vào: D:\Code\Github\Nhom29-E403-day08\day08\lab\results\ab_comparison_all.csv
```
