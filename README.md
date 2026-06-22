# BÀI TIỂU LUẬN - MÔN ĐẢM BẢO CHẤT LƯỢNG VÀ KIỂM THỬ PHẦN MỀM
# GVHD: TS. NGUYỄN TUẤN LINH
# THỰC HIỆN: SV. LƯỜNG VĂN HẠNH - K225480106013
## Đề tài: AI trong build/development và kiểm thử hồi quy liên tục.
## Yêu cầu :Nghiên cứu cách AI hỗ trợ code generation, review, phát hiện lỗi sớm và lựa chọn regression test.

---
## Bài toán: Thiết kế và tối ưu hóa hệ thống kiểm thử hồi quy liên tục cho Module tính lương và Thuế thu nhập cá nhân (Payroll & Personal Income Tax Engine)

Dự án thực nghiệm nghiên cứu giải pháp infuse AI nhằm tự động hóa quy trình xây dựng (Build), thiết lập đường ống tích hợp liên tục (CI/CD) và tối ưu hóa chiến lược lựa chọn ca kiểm thử hồi quy (RTS).

## 📊 Các trục nội dung thực nghiệm
1. **Ứng dụng AI khâu phát triển (Build/Development):** Thiết kế Prompt sinh mã nguồn logic và hệ thống kịch bản kiểm thử tự động gồm 22 ca test biên.
2. **Thiết lập đường ống CI/CD Pipeline:** Tự động hóa kiểm thử liên tục (Continuous Testing) qua môi trường độc lập của GitHub Actions.
3. **Tối ưu hóa kiểm thử hồi quy (RTS):** Giả lập thuật toán AI phân tích tầm ảnh hưởng (Change Impact Analysis), tối ưu hóa cắt giảm 81.8% số lượng ca kiểm thử khi thay đổi luật định pháp lý.

## 🛠️ Công nghệ triển khai
- Core Engine: Python 3.17
- Test Automation Framework: Pytest (Cấu hình Pytest Markers để phân vùng RTS)
- CI/CD Infrastructure: GitHub Actions
