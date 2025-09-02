# Báo cáo sản phẩm STEM: Speak\&Speak

## 1. Thông tin chung

* **Tên dự án:** Speak\&Speak
* **Học sinh thực hiện:** Nguyễn Hữu Hòa – Lớp 11L
* **Giáo viên hướng dẫn:**  Thầy Nguyễn Hữu Hợp – Bộ môn Tin học

---

## 2. Lý do và mục tiêu

Tiếng Anh quan trọng trong học tập và hội nhập. Tuy nhiên, nhiều học sinh vẫn phát âm chưa chuẩn, thiếu tự tin nói tiếng Anh. Các ứng dụng hiện có thường phức tạp, tốn phí, hoặc không phù hợp với học sinh Việt Nam.

**Speak\&Speak** ra đời để:

* Cung cấp công cụ luyện phát âm **miễn phí, dễ dùng, phù hợp học sinh THPT**.
* Hỗ trợ người học tự luyện nói chính xác, tự tin.
* Đảm bảo **mã nguồn mở** (GNU GPL v3) để cộng đồng cùng học hỏi và phát triển.

---

## 3. Giải pháp

Ứng dụng hoạt động như một **trợ lý luyện phát âm**:

1. Người dùng chọn bài luyện (từ/câu).
2. Ứng dụng ghi âm giọng đọc và so sánh với phát âm chuẩn.
3. Hiển thị kết quả rõ ràng: chỉ ra lỗi, đưa gợi ý sửa.
4. Ghi nhớ lỗi để tạo bài luyện tập **tập trung vào điểm yếu**.

Ưu điểm:

* Bài tập cá nhân hóa theo từng người.
* Giao diện trực quan, dễ dùng, không yêu cầu mạng.
* Hoàn toàn miễn phí, minh bạch mã nguồn.

---

## 4. Quy trình triển khai & phát triển

### Công cụ và công nghệ phát triển
* Ngôn ngữ lập trình chính: **Python**
* Môi trường phát triển: **VSCodium** trên **Fedora Linux**
* Cơ sở dữ liệu: **yaml**
* Trình chuyển đổi âm thanh và phiên âm: vosk, eng-to-ipa
* Và các công cụ khác,...

| Giai đoạn                   | Công việc chính                                     |
| --------------------------- | --------------------------------------------------- |
| 1. Khởi động dự án          | Xác định nhu cầu, tìm hiểu công nghệ.               |
| 2. Thiết kế ứng dụng        | Lên sơ đồ hoạt động, giao diện, cách lưu dữ liệu.   |
| 3. Xây dựng tính năng chính | Thu âm, so sánh phát âm, tạo bài tập thông minh.    |
| 4. Hoàn thiện giao diện     | Tối ưu hiển thị, dễ thao tác.                       |
| 5. Kiểm thử và sửa lỗi      | Chạy thử nhiều lần, đảm bảo ổn định.                |
| 6. Hoàn thiện sản phẩm      | Viết tài liệu, đóng gói phần mềm, chuẩn bị báo cáo. |

---

## 5. Qui trình hoạt động: 
* Luyện phát âm từ và câu: Cung cấp từ/câu để người dùng luyện tập.
* Phản hồi chi tiết: Sau khi người dùng ghi âm, ứng dụng sẽ:
* Chỉ ra các từ phát âm sai.
* Hiển thị phiên âm IPA chuẩn và phiên âm mà hệ thống nhận diện được.
* Liệt kê cụ thể các âm IPA bị sai (thiếu âm, thừa âm, thay thế âm).
* Luyện tập thông minh: Tự động đề xuất các từ/câu có chứa âm người dùng hay sai.
* Thống kê tiến độ: Phân tích 20 lần luyện tập gần nhất để đưa ra điểm tổng thể, nhận xét sự tiến bộ và gợi ý các âm cần cải thiện.

## 6. Mô tả chi tiết kết quả

Sản phẩm cuối cùng là một ứng dụng máy tính với đầy đủ tính năng:

* **Luyện phát âm từ và câu:** Có sẵn kho từ/câu để luyện tập.
* **Đánh giá chi tiết:** Khi người dùng ghi âm, ứng dụng sẽ:

  * Chỉ ra các từ phát âm sai.
  * Hiển thị phát âm chuẩn và cách bạn vừa đọc.
  * Liệt kê âm nào đọc sai (thiếu âm, thừa âm, nhầm âm).
* **Luyện tập thông minh:** Hệ thống tự đề xuất bài tập chứa âm bạn thường sai.
* **Theo dõi tiến bộ:** Thống kê kết quả luyện tập gần đây, hiển thị mức độ cải thiện.
* **Tùy chỉnh giao diện:** Hỗ trợ chế độ sáng/tối và màu sắc yêu thích.

Ứng dụng chạy hoàn toàn **offline**, phù hợp cả máy cấu hình thấp, dễ cài đặt và sử dụng cho mọi học sinh.

---

## 7. Giá trị và tiềm năng

* Giúp học sinh tự học phát âm tại nhà, không cần giáo viên kèm trực tiếp.
* Tăng sự tự tin khi giao tiếp tiếng Anh.
* Khuyến khích tinh thần học hỏi, chia sẻ và phát triển phần mềm tự do.

---

## 8. Kết luận

**Speak\&Speak** là một ví dụ rõ ràng về việc học sinh có thể tự tìm giải pháp công nghệ để giải quyết vấn đề thực tế trong học tập. Sản phẩm dễ dùng, miễn phí và có giá trị lâu dài nhờ cộng đồng cùng tham gia phát triển.

## 9. Thư viện ảnh 
# Image Library

| | |
|---|---|
| ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-44-47.png) | ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-45-22.png) |
| ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-46-08.png) | ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-46-16.png) |

