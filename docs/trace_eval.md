# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Phương Nam 
> **Mã Sinh Viên / Mã Học viên:** 2A202602869  
> **Chủ đề Lựa chọn:** Trợ lý Đơn hàng & Kho vận (Supply Chain Agent): Tra cứu mã vận đơn, vị trí lưu kho và cập nhật trạng thái đơn hàng  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4 / 5** | Xử lý chuỗi nghiệp vụ phụ thuộc: Khi nhân viên yêu cầu *"Kiểm tra kiện hàng VN2026_001 và nếu đang ở Kho Hà Nội thì chuyển sang 'Đang xuất kho'"*, Agent phải tư duy đa bước: **Bước 1** gọi tool `order_query('VN2026_001')` lấy vị trí -> **Bước 2** phân tích kết quả thấy đang ở kệ B3 Kho Hà Nội -> **Bước 3** mới kích hoạt tool `update_order_status` để đổi trạng thái. Chatbot đơn bước không thể tự nối chuỗi logic này. |
| **2. Tool Interaction** | **5 / 5** | LLM không thể tự biết dữ liệu nội bộ kho WMS. Bắt buộc phải gọi công cụ bên ngoài qua MCP Server: **(1)** Tool đọc `order_query` để lấy mã vận đơn `VN2026_001`, vị trí kệ hàng, tên sản phẩm; **(2)** Tool ghi `update_order_status` để cập nhật trạng thái mới vào cơ sở dữ liệu. Không có 2 tool này, LLM chắc chắn sẽ tự bịa (Hallucination) ra vị trí đơn hàng. |
| **3. Dynamic Decision** | **4 / 5** | Hành động tiếp theo rẽ nhánh động theo dữ liệu trả về từ Tool: <br>• **Nhánh 1:** Nếu `order_query` trả về trạng thái `"Lưu kho"` -> Agent cho phép gọi tiếp tool cập nhật trạng thái giao hàng.<br>• **Nhánh 2:** Nếu tra cứu mã `VN9999_999` trả về `"NOT_FOUND"` (như TC05) -> Agent lập tức dừng luồng xử lý, báo lỗi mã không tồn tại thay vì gọi lệnh cập nhật.<br>• **Nhánh 3:** Nếu đơn đã `"Đã hủy"` -> Agent từ chối xuất kho. |
| **4. Long Horizon Goal** | **4 / 5** | Duy trì mục tiêu tổng thể xuyên suốt: Tiếp nhận yêu cầu nghiệp vụ phức tạp từ nhân viên kho (ví dụ: đối soát kiện hàng `VN2026_001`, kiểm tra vị trí lưu kho, cập nhật xuất kho và gửi xác nhận), Agent duy trì mục tiêu này qua 2-3 vòng lặp ReAct liên tiếp cho đến khi xuất được kết luận cuối cùng (Final Answer) mà không bị quên hay đứt gãy luồng xử lý. |
| **TỔNG ĐIỂM AGENTIC FIT** | **17 / 20** | *Tổng điểm 17/20 (> 12/20): Bài toán vận đơn & kho vận có tính tương tác dữ liệu và phân nhánh rất cao, bắt buộc phải triển khai bằng ReAct Agent.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin vận đơn và vị trí lưu kho của đơn hàng VN2026_001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "order_query",
    "arguments": {
      "tracking_id": "VN2026_001"
    },
    "observation": {
      "status": "SUCCESS",
      "tracking_id": "VN2026_001",
      "data": {
        "item_name": "iPhone 16 Pro Max 256GB",
        "quantity": 1,
        "recipient_name": "Nguyễn Văn An",
        "recipient_phone": "0987654321",
        "warehouse_location": "Kho Tổng Hà Nội - Kệ B3",
        "status": "Lưu kho",
        "carrier": "Viettel Post",
        "created_date": "10/09/2026"
      }
    },
    "latency_ms": 1201.03
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin vận đơn và vị trí lưu kho của đơn hàng VN2026_001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Kết quả tra cứu đơn hàng VN2026_001: Sản phẩm: iPhone 16 Pro Max 256GB (SL: 1), Người nhận: Nguyễn Văn An (0987654321), Vị trí lưu kho: Kho Tổng Hà Nội - Kệ B3, Trạng thái: Lưu kho, Đơn vị vận chuyển: Viettel Post.",
    "latency_ms": 10.0
  },
  {
    "step": 1,
    "query": "Hãy cập nhật trạng thái đơn hàng VN2026_001 sang 'Đang xuất kho' tại 'Kho Tổng Hà Nội - Kệ B3'.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "update_order_status",
    "arguments": {
      "tracking_id": "VN2026_001",
      "warehouse_location": "Kho Tổng Hà Nội - Kệ B3",
      "new_status": "Đang xuất kho"
    },
    "observation": {
      "status": "SUCCESS",
      "update_id": "UP-VN2026_001-2026",
      "tracking_id": "VN2026_001",
      "new_status": "Đang xuất kho",
      "warehouse_location": "Kho Tổng Hà Nội - Kệ B3",
      "message": "Cập nhật thành công: Đơn hàng VN2026_001 đã chuyển sang trạng thái 'Đang xuất kho' tại 'Kho Tổng Hà Nội - Kệ B3'."
    },
    "latency_ms": 1523.87
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini `gemini-2.5-flash`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 / 4 lượt (TC02: `order_query`, TC03: `update_order_status`, TC04: `order_query`, TC05: `order_query`).
- **Kết quả đẩy Repo nộp bài:** [x] Đã hoàn thiện toàn bộ mã nguồn, cấu hình và báo cáo nghiệm thu để Push lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
