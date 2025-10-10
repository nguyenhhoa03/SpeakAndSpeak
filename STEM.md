# Báo cáo sản phẩm STEM: Speak\&Speak

## I. Thông tin chung

* **Tên dự án:** Speak\&Speak
* **Học sinh thực hiện:** Nguyễn Hữu Hòa – Lớp 11L
* **Giáo viên hướng dẫn:**  Thầy Nguyễn Hữu Hợp – Bộ môn Tin học

---

## II. Lý do và mục tiêu

Tiếng Anh quan trọng trong học tập và hội nhập. Tuy nhiên, nhiều học sinh vẫn phát âm chưa chuẩn, thiếu tự tin nói tiếng Anh. Các ứng dụng hiện có thường phức tạp, tốn phí, hoặc không phù hợp với học sinh Việt Nam.

**Speak\&Speak** ra đời để:

* Cung cấp công cụ luyện phát âm **miễn phí, dễ dùng, phù hợp học sinh THPT**.
* Hỗ trợ người học tự luyện nói chính xác, tự tin.
* Đảm bảo **mã nguồn mở** (GNU GPL v3) để cộng đồng cùng học hỏi và phát triển.

---

## III. Giải pháp

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

## IV. Quy trình triển khai & phát triển

### 1. Khởi động dự án

Xác định nhu cầu, tìm hiểu công nghệ.

#### Công cụ và công nghệ phát triển
* Ngôn ngữ lập trình chính: [**Python**](https://www.python.org/)
* Môi trường phát triển: [**VSCodium**](https://vscodium.com/) trên [**Fedora Linux**](https://fedoraproject.org/)
* Trình chuyển đổi âm thanh và phiên âm tiếng Anh: [**vosk**](https://pypi.org/project/vosk/), [**eng-to-ipa**](https://pypi.org/project/eng-to-ipa/)
* Cơ sở dữ liệu: **yaml**, **SQLite**
* Và các công cụ khác,...

![Cấu trúc thư mục chính của SpeakAndSpeak](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/refs/heads/main/images/Screenshot%20From%202025-09-12%2023-44-12.png)

### 2. Thiết kê ứng dụng

Lên sơ đồ hoạt động, giao diện, cách lưu dữ liệu.

#### Hoạt động

* Luyện phát âm từ và câu: Cung cấp từ/câu để người dùng luyện tập.
* Phản hồi chi tiết: Sau khi người dùng ghi âm, ứng dụng sẽ:
* Chỉ ra các từ phát âm sai.
* Hiển thị phiên âm IPA chuẩn và phiên âm mà hệ thống nhận diện được.
* Liệt kê cụ thể các âm IPA bị sai (thiếu âm, thừa âm, thay thế âm).
* Luyện tập thông minh: Tự động đề xuất các từ/câu có chứa âm người dùng hay sai.
* Thống kê tiến độ: Phân tích 20 lần luyện tập gần nhất để đưa ra điểm tổng thể, nhận xét sự tiến bộ và gợi ý các âm cần cải thiện.

#### Giao diện

Ứng dụng có 6 mục chính: **Chào mừng**, **Luyện từ**, **Luyện câu**, **Thống kê**, **Cài đặt**, và **Giới thiệu**. Mỗi mục được thiết kế trực quan với nút bấm lớn, thanh tiến trình hiển thị quá trình thu âm/xử lý, và khung văn bản để hiển thị kết quả hoặc thống kê.

#### Lưu dữ liệu

* **Cài đặt** (giao diện, màu sắc, ảnh chào mừng) được lưu trong **cơ sở dữ liệu YAML** để giữ nguyên khi mở lại ứng dụng.
* **Kết quả luyện tập và các lỗi phát âm** cũng được ghi vào **cơ sở dữ liệu YAML**, giúp hệ thống chọn từ/câu phù hợp hơn cho lần luyện sau.

### 3. Xây dựng tính năng chính

Để dễ dàng phát triển và bảo trì, ứng dụng được tách ra thành nhiều module nhỏ (mỗi module là một file python chứa các chức năng khác nhau) và một file python chính tổng hợp các module thành một app hoàn chỉnh. 

| Tên module                 | Tên file                      | Chức năng                                                                  |
| -------------------------- | ----------------------------- | -------------------------------------------------------------------------- |
| Tạo câu luyện tập          | `non_random_sentence.py`      | Đưa ra câu tiếng Anh để luyện, ưu tiên những câu chứa lỗi phát âm trước đó |
| Tạo từ luyện tập           | `non_random_word.py`          | Đưa ra từ tiếng Anh để luyện, cũng dựa trên lỗi phát âm đã lưu             |
| Đánh giá phát âm           | `pronunciation_assessment.py` | So sánh phát âm người dùng với chuẩn, chỉ ra từ sai và âm sai              |
| Chuyển giọng nói thành chữ | `speech_to_text.py`           | Nghe giọng người dùng và biến thành văn bản tiếng Anh                      |
| Phân tích thống kê         | `user_statistics.py`          | Xem lại kết quả, điểm số, lỗi thường gặp và lời khuyên luyện tập           |
| Ứng dụng chính             | `app.py`                      | Giao diện tổng thể, kết nối các module lại thành ứng dụng hoàn chỉnh       |

### 4. Hoàn thiện giao diện

Ứng dụng được viết bằng thư viện [CustomTkinter](https://customtkinter.tomschimansky.com/) để xây dựng giao diện, vừa đơn giản và gọn nhẹ nhưng vẫn đảm bảo tính thẩm mỹ.

| | |
|---|---|
| ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-44-47.png) | ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-45-22.png) |
| ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-46-08.png) | ![](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-02%2012-46-16.png) |

### 5. Kiểm thử và sửa lỗi

Sau rất nhiều thời gian sửa lỗi và [update](https://github.com/nguyenhhoa03/SpeakAndSpeak/commits) thì ứng dụng đã hoạt động ổn định trên **Windows** và **Linux**. Tuy nhiên, hiện chưa được chạy thử trên **macOS** do em không có thiết bị để kiểm tra, đây là thiếu sót của dự án tuy nhiên em sẽ cố găng khắc phục trong tương lai gần.

### 6. Hoàn thiện sản phẩn 

Đễ dễ dàng sử dụng, em đã tạo ra trình cài đặt cho SpeakAndSpeak giúp mọi người cài đặt một cách đơn giản và dễ dàng.

![Quá trình tạo ra trình cài đặt cho ứng dụng](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/refs/heads/main/images/Screenshot%20From%202025-09-15%2019-47-23.png)

Cuối cùng là viết báo cáo cho sản phẩm là nội dung mà bạn đang đọc.

## V. Hướng dẫn cài đặt và sử dụng: 

Cài đặt ứng dụng rất đơn giản, chỉ cần bạn tải trình cài đặt [SpeakAndSpeak-Setup-v1.0.exe](https://github.com/nguyenhhoa03/SpeakAndSpeak/releases/download/SpeakAndSpeak/SpeakAndSpeak-Setup-v1.0.exe) ở [Github Releases](https://github.com/nguyenhhoa03/SpeakAndSpeak/releases/tag/SpeakAndSpeak) và chạy nó. Tiếp theo chỉ cần làm theo hướng dẫn là được. 

|  License | Tạo shortcut (cần thiết) | Tóm tắt cài đặt | Đang cài đặt | Hoàn thành |
|-------------------------|--------------|-----------------|--------------|------------|
| ![Phần chấp nhận License](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-15%2019-03-26.png) | ![Tạo shortcut](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-15%2019-03-32.png) | ![Tóm tắt cài đặt](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-15%2019-03-37.png) | ![Đang cài đặt](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-15%2019-03-44.png) | ![Hoàn thành](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/main/images/Screenshot%20From%202025-09-15%2019-04-01.png) |


## VI. Mô tả chi tiết kết quả

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

## VII. Giá trị và tiềm năng

* Giúp học sinh tự học phát âm tại nhà, không cần giáo viên kèm trực tiếp.
* Tăng sự tự tin khi giao tiếp tiếng Anh.
* Khuyến khích tinh thần học hỏi, chia sẻ và phát triển phần mềm tự do.

---

## VIII. Kết luận

**Speak\&Speak** là một ví dụ rõ ràng về việc học sinh có thể tự tìm giải pháp công nghệ để giải quyết vấn đề thực tế trong học tập. Sản phẩm dễ dùng, miễn phí và có giá trị lâu dài nhờ cộng đồng cùng tham gia phát triển.

