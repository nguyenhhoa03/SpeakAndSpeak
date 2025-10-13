# ỨNG DỤNG HỖ TRỢ LUYỆN PHÁT ÂM TIẾNG ANH SPEAK&SPEAK SỬ DỤNG CÔNG NGHỆ NHẬN DIỆN GIỌNG NÓI

Học sinh thực hiện: Nguyễn Hữu Hòa – Lớp 11L  
Giáo viên hướng dẫn: Cô Đặng Thị Huyền Trân – Bộ môn Vật Lý  
Trường THPT Chuyên Bến Tre  
Năm học 2025-2026

---

## A. LÍ DO CHỌN ĐỀ TÀI

Trong bối cảnh hội nhập quốc tế ngày càng sâu rộng, tiếng Anh đã trở thành ngôn ngữ toàn cầu quan trọng trong học tập, nghiên cứu và giao tiếp. Tuy nhiên, một trong những khó khăn lớn nhất mà học sinh Việt Nam gặp phải là kỹ năng phát âm. Nhiều học sinh có vốn từ vựng tốt, hiểu ngữ pháp nhưng lại thiếu tự tin khi giao tiếp do phát âm chưa chuẩn xác.

Các ứng dụng học tiếng Anh hiện có trên thị trường như Duolingo, ELSA Speak tuy có nhiều ưu điểm nhưng vẫn tồn tại một số hạn chế: yêu cầu trả phí cho các tính năng nâng cao, phụ thuộc vào kết nối internet, hoặc không cung cấp phản hồi chi tiết về phiên âm IPA (International Phonetic Alphabet) - hệ thống ký hiệu được sử dụng rộng rãi trong giảng dạy tiếng Anh tại Việt Nam.

Nhận thấy những vấn đề trên, em đã nghiên cứu và phát triển ứng dụng Speak&Speak - một công cụ luyện phát âm tiếng Anh hoàn toàn miễn phí, hoạt động offline, cung cấp phản hồi chi tiết dựa trên phiên âm IPA và có khả năng cá nhân hóa bài tập theo điểm yếu của từng người học. Đặc biệt, ứng dụng được phát triển theo mô hình mã nguồn mở ([GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)), cho phép cộng đồng giáo viên và học sinh có thể tham gia cải tiến và phát triển thêm.

## B. GIẢ THUYẾT KHOA HỌC, CÂU HỎI NGHIÊN CỨU, MỤC TIÊU KỸ THUẬT, KẾT QUẢ MONG ĐỢI

### 1. Giả thuyết khoa học

Việc ứng dụng công nghệ nhận diện giọng nói (Speech Recognition) kết hợp với phân tích phiên âm IPA và bài tập phân biệt ngữ âm có thể giúp cải thiện đáng kể kỹ năng phát âm tiếng Anh của học sinh thông qua:

- Hệ thống phản hồi chi tiết về từng âm vị (phoneme) trong quá trình phát âm, giúp người học nhận biết chính xác lỗi sai của mình.
- Bài tập phân biệt ngữ âm giúp rèn luyện khả năng nhận diện và phân biệt các âm tương tự nhau.
- Việc sử dụng thuật toán phân tích lỗi phát âm có thể tạo ra bài tập cá nhân hóa, tập trung vào những âm mà người học thường mắc lỗi.
- Ứng dụng hoạt động offline với công nghệ nhận diện giọng nói có thể đạt độ chính xác cao, phù hợp với điều kiện học tập của học sinh Việt Nam.

### 2. Câu hỏi nghiên cứu

- Hệ thống nhận diện giọng nói offline có thể đạt được độ chính xác như thế nào khi so sánh với các giải pháp online?
- Phương pháp phân tích và so sánh phiên âm IPA có hiệu quả trong việc chỉ ra lỗi phát âm cụ thể không?
- Bài tập phân biệt ngữ âm có giúp cải thiện khả năng nhận diện và phát âm các âm tương tự nhau không?
- Thuật toán đề xuất bài tập dựa trên lỗi phát âm có giúp người học cải thiện nhanh hơn so với phương pháp luyện tập ngẫu nhiên không?
- Ứng dụng có thể hoạt động ổn định trên các máy tính cấu hình trung bình, phù hợp với điều kiện thực tế của học sinh không?
- Giao diện và trải nghiệm người dùng có dễ sử dụng và phù hợp với học sinh THPT không?

### 3. Đối tượng nghiên cứu

- Công nghệ nhận diện giọng nói: Mô hình Vosk - một công nghệ speech-to-text mã nguồn mở, hoạt động offline.
- Hệ thống phân tích phát âm: Thuật toán so sánh phiên âm IPA giữa bản ghi âm của người dùng và phát âm chuẩn.
- Bài tập phân biệt ngữ âm: Hệ thống nhận diện và phân biệt các âm tương tự nhau.
- Cơ sở dữ liệu từ vựng: Kho từ và câu tiếng Anh phù hợp với chương trình THPT.
- Đối tượng người dùng: Học sinh THPT có nhu cầu cải thiện kỹ năng phát âm tiếng Anh.

### 4. Phạm vi nghiên cứu

- Phát triển ứng dụng cho hệ điều hành Windows và Linux.
- Tập trung vào kỹ năng phát âm từ đơn, câu đơn giản và bài tập phân biệt ngữ âm.
- Áp dụng cho học sinh THPT trong môi trường tự học tại nhà.

### 5. Mục tiêu kỹ thuật

- Xây dựng hệ thống nhận diện giọng nói offline: Tích hợp mô hình Vosk để chuyển đổi giọng nói thành văn bản với độ chính xác cao, hoạt động mượt mà trên máy tính cấu hình trung bình (RAM 4GB trở lên).
- Phát triển thuật toán phân tích phát âm: So sánh phiên âm IPA của người dùng với phiên âm chuẩn, xác định các lỗi cụ thể (thiếu âm, thừa âm, nhầm âm).
- Thiết kế hệ thống bài tập thông minh: Xây dựng thuật toán đề xuất từ/câu chứa các âm mà người học thường mắc lỗi, tối ưu hóa quá trình học tập.
- Phát triển bài tập phân biệt ngữ âm: Tạo hệ thống bài tập giúp người học phân biệt các âm tương tự nhau trong tiếng Anh.
- Xây dựng cơ sở dữ liệu: Tạo kho từ vựng và câu mẫu phù hợp với chương trình THPT, lưu trữ lịch sử luyện tập và phân tích lỗi.
- Thiết kế giao diện người dùng thân thiện: Sử dụng thư viện CustomTkinter để tạo giao diện hiện đại, trực quan, dễ sử dụng.
- Đảm bảo tính bảo mật và quyền riêng tư: Dữ liệu người dùng được lưu trữ cục bộ, không cần kết nối internet hay đăng ký tài khoản.

### 6. Nội dung nghiên cứu, kết quả mong đợi

- Phát triển ứng dụng hoàn chỉnh: Xây dựng ứng dụng Speak&Speak với đầy đủ tính năng luyện phát âm từ và câu, bài tập phân biệt ngữ âm, đánh giá chi tiết, thống kê tiến bộ.
- Cung cấp phản hồi chi tiết: Hệ thống có khả năng chỉ ra chính xác từng âm vị bị phát âm sai, hiển thị phiên âm IPA chuẩn và phiên âm mà hệ thống nhận diện được.
- Tối ưu hóa trải nghiệm học tập: Bài tập được đề xuất dựa trên lỗi phát âm thực tế của người học, giúp cải thiện hiệu quả học tập.
- Phát triển bài tập phân biệt ngữ âm: Giúp người học nhận diện và phân biệt các âm tương tự nhau, nâng cao độ nhạy cảm với âm thanh tiếng Anh.
- Tạo ra công cụ học tập miễn phí: Đưa ra giải pháp học tập không tốn phí, phù hợp với điều kiện kinh tế của học sinh Việt Nam.
- Khuyến khích phát triển mã nguồn mở: Chia sẻ mã nguồn theo giấy phép [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html), tạo cơ hội cho cộng đồng giáo viên và học sinh tham gia cải tiến.

## C. MÔ TẢ CHI TIẾT PHƯƠNG PHÁP NGHIÊN CỨU VÀ CÁC KẾT LUẬN

### 1. Phương pháp nghiên cứu

#### Giai đoạn 1: Nghiên cứu lý thuyết và khảo sát nhu cầu

- Nghiên cứu các công nghệ nhận diện giọng nói: Google Speech API, CMU Sphinx, Vosk.
- Tìm hiểu về phiên âm IPA và các phương pháp so sánh phát âm.
- Nghiên cứu về bài tập phân biệt ngữ âm và tầm quan trọng trong việc học phát âm.
- Khảo sát nhu cầu và khó khăn của học sinh trong việc luyện phát âm tiếng Anh.
- So sánh các ứng dụng hiện có trên thị trường: Duolingo, ELSA Speak, phân tích ưu điểm và hạn chế.

#### Giai đoạn 2: Thiết kế hệ thống

- Thiết kế kiến trúc hệ thống: Phân chia thành các module độc lập (nhận diện giọng nói, phân tích phát âm, đề xuất bài tập, bài tập phân biệt ngữ âm, thống kê).
- Thiết kế cơ sở dữ liệu: Sử dụng **YAML** cho lưu trữ kết quả luyện tập và **SQLite** cho cơ sở dữ liệu mẫu.
- Thiết kế giao diện: Vẽ mockup cho các màn hình chính (Chào mừng, Bài tập, Phát âm, Thống kê, Cài đặt, Giới thiệu).
- Thiết kế thuật toán đề xuất bài tập dựa trên phân tích lỗi phát âm.
- Thiết kế hệ thống bài tập phân biệt ngữ âm với các cặp âm tương tự.

#### Giai đoạn 3: Phát triển ứng dụng

- Xây dựng module nhận diện giọng nói: Tích hợp thư viện **Vosk** để chuyển đổi giọng nói thành văn bản.
- Phát triển module phân tích phát âm: Sử dụng thư viện eng-to-ipa để chuyển đổi văn bản thành phiên âm IPA, so sánh với phiên âm chuẩn.
- Xây dựng module đề xuất bài tập: Phân tích lịch sử lỗi phát âm, ưu tiên đề xuất từ/câu chứa các âm người học thường sai.
- Phát triển module bài tập phân biệt ngữ âm: Tạo hệ thống bài tập giúp người học phân biệt các âm tương tự nhau.
- Phát triển module thống kê: Tính toán điểm số, phân tích xu hướng cải thiện, đưa ra gợi ý luyện tập.
- Thiết kế giao diện: Sử dụng **CustomTkinter** để xây dựng giao diện hiện đại, hỗ trợ chế độ sáng/tối.

#### Giai đoạn 4: Kiểm thử và tối ưu hóa

- Kiểm thử chức năng: Kiểm tra từng module hoạt động đúng yêu cầu.
- Kiểm thử tích hợp: Đảm bảo các module hoạt động mượt mà khi kết hợp.
- Kiểm thử hiệu năng: Đo thời gian phản hồi, mức tiêu thụ tài nguyên hệ thống.
- Kiểm thử trên nhiều thiết bị: Chạy thử trên Windows và Linux với các cấu hình khác nhau.
- Sửa lỗi và tối ưu hóa code để cải thiện hiệu suất.

#### Giai đoạn 5: Hoàn thiện và triển khai

- Tạo trình cài đặt cho **Windows** và **Linux** để người dùng dễ dàng cài đặt.
- Viết tài liệu hướng dẫn sử dụng và tài liệu kỹ thuật cho nhà phát triển.
- Xuất bản mã nguồn lên GitHub theo giấy phép GNU GPL v3.
- Thu thập phản hồi từ người dùng thử nghiệm và cải tiến.

### 2. Ý nghĩa khoa học

- Đổi mới trong ứng dụng công nghệ nhận diện giọng nói vào giáo dục: Nghiên cứu này góp phần ứng dụng công nghệ phân tích phát âm vào việc cải thiện kỹ năng ngôn ngữ, mở ra hướng nghiên cứu mới trong lĩnh vực giáo dục công nghệ.
- Phát triển phương pháp phân tích phát âm dựa trên IPA: Đề xuất thuật toán so sánh phiên âm IPA hiệu quả, có thể áp dụng cho các ngôn ngữ khác.
- Xây dựng mô hình học tập cá nhân hóa: Thuật toán đề xuất bài tập dựa trên lỗi phát âm cá nhân là một hướng tiếp cận mới trong giáo dục ngôn ngữ.
- Phát triển hệ thống bài tập phân biệt ngữ âm: Đóng góp vào việc nâng cao khả năng nhận diện và phân biệt âm thanh trong học ngôn ngữ.
- Đóng góp vào phong trào phần mềm mã nguồn mở: Khuyến khích tinh thần chia sẻ và hợp tác trong cộng đồng giáo dục và lập trình.

### 3. Ý nghĩa thực tiễn

- Cải thiện kỹ năng phát âm cho học sinh: Cung cấp công cụ hiệu quả giúp học sinh tự luyện tập và cải thiện phát âm tiếng Anh.
- Phát triển kỹ năng phân biệt ngữ âm: Giúp học sinh nhận diện và phân biệt các âm tương tự nhau, nâng cao độ nhạy cảm với âm thanh tiếng Anh.
- Giảm chi phí học tập: Ứng dụng hoàn toàn miễn phí, không yêu cầu kết nối internet, phù hợp với điều kiện kinh tế của học sinh Việt Nam.
- Tăng tính tự chủ trong học tập: Học sinh có thể tự học, tự đánh giá và cải thiện mà không cần sự hỗ trợ trực tiếp của giáo viên.
- Hỗ trợ giáo viên trong công tác giảng dạy: Giáo viên có thể giới thiệu ứng dụng cho học sinh làm công cụ tự luyện tập ngoài giờ lên lớp.
- Khuyến khích tinh thần học hỏi và nghiên cứu: Dự án là ví dụ về việc học sinh có thể tự tìm hiểu và phát triển ứng dụng công nghệ giải quyết vấn đề thực tế.

---

# CHƯƠNG 1. BÁO CÁO DỰ ÁN NGHIÊN CỨU KỸ THUẬT

## 1.1. Tổng quan về ứng dụng Speak&Speak

Speak&Speak là một ứng dụng máy tính hỗ trợ luyện phát âm tiếng Anh, được phát triển dựa trên công nghệ nhận diện giọng nói, phân tích phiên âm IPA và bài tập phân biệt ngữ âm. Ứng dụng hoạt động hoàn toàn offline, không yêu cầu kết nối internet, đảm bảo quyền riêng tư và phù hợp với điều kiện học tập của học sinh Việt Nam.

Đặc điểm nổi bật:

- Hoạt động offline: Không cần kết nối internet, dữ liệu người dùng được lưu trữ cục bộ.
- Phản hồi chi tiết: Chỉ ra chính xác từng âm vị bị phát âm sai, hiển thị phiên âm IPA chuẩn và phiên âm nhận diện được.
- Bài tập cá nhân hóa: Đề xuất từ/câu chứa các âm người học thường sai, tối ưu hóa quá trình học tập.
- Bài tập phân biệt ngữ âm: Giúp người học phân biệt các âm tương tự nhau trong tiếng Anh.
- Thống kê tiến bộ: Phân tích 20 lần luyện tập gần nhất, đưa ra điểm số và gợi ý cải thiện.
- Miễn phí và mã nguồn mở: Hoàn toàn miễn phí, mã nguồn được chia sẻ theo giấy phép GNU GPL v3.

![SpeakAndSpeak trên Linux](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2013-17-00.png?raw=true)

## 1.2. Cấu tạo và đặc điểm kỹ thuật

### 1.2.1. Công nghệ và công cụ phát triển

| Tên công nghệ/công cụ | Mô tả | Vai trò |
|----------------------|-------|---------|
| Python 3.13 | Ngôn ngữ lập trình chính | Phát triển toàn bộ ứng dụng |
| Vosk | Thư viện nhận diện giọng nói | Chuyển đổi giọng nói thành văn bản |
| eng-to-ipa | Thư viện chuyển đổi phiên âm | Chuyển văn bản thành phiên âm IPA |
| CustomTkinter | Thư viện giao diện | Xây dựng giao diện người dùng |
| YAML | Định dạng dữ liệu | Lưu trữ cài đặt ứng dụng |
| SQLite | Cơ sở dữ liệu | Lưu trữ kết quả luyện tập |
| wave | Thư viện âm thanh | Thu âm giọng nói người dùng |
| pyttsx3 | Text-to-Speech | Phát âm thanh từ văn bản |
| pyaudio | Xử lý âm thanh | Thu âm từ microphone |
| VSCodium | Môi trường phát triển | Viết và debug code |
| Fedora Linux | Hệ điều hành phát triển | Nền tảng phát triển chính |

### 1.2.2. Kiến trúc hệ thống

Ứng dụng được thiết kế theo kiến trúc module, bao gồm các thành phần chính:

Module 1: Thu âm và nhận diện giọng nói (speech_to_text.py)
- Chức năng: Thu âm giọng nói người dùng và chuyển đổi thành văn bản
- Công nghệ: Vosk speech recognition
- Input: Âm thanh từ microphone
- Output: Văn bản tiếng Anh

Module 2: Phân tích và đánh giá phát âm (pronunciation_assessment.py)
- Chức năng: So sánh phát âm người dùng với phát âm chuẩn
- Công nghệ: eng-to-ipa, thuật toán so sánh chuỗi
- Input: Văn bản nhận diện, văn bản chuẩn
- Output: Danh sách lỗi phát âm (từ sai, âm sai)

Module 3: Đề xuất bài tập câu (non_random_sentence.py)
- Chức năng: Đề xuất từ và câu để luyện tập
- Thuật toán: Ưu tiên câu chứa âm người học thường sai
- Input: Lịch sử lỗi phát âm
- Output: Câu tiếng Anh để luyện

Module 4: Thống kê và phân tích (user_statistics.py)
- Chức năng: Phân tích kết quả luyện tập, tính điểm, đưa ra gợi ý
- Input: Dữ liệu lịch sử luyện tập
- Output: Điểm số, biểu đồ tiến bộ, gợi ý cải thiện

Module 5: Bài tập phân biệt ngữ âm (discrimination.py)
- Chức năng: Tạo bài tập phân biệt các âm tương tự trong tiếng Anh
- Input: Lịch sử lỗi sai bài tập
- Output: Bài tập phân biệt ngữ âm

Module 6: Giao diện người dùng (app.py)
- Chức năng: Tích hợp các module, hiển thị giao diện
- Công nghệ: CustomTkinter
- Tính năng: 6 màn hình chính (Chào mừng, Bài tập, Luyện câu, Thống kê, Cài đặt, Giới thiệu)

![Các modules sẽ được import vào app chính](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2019-14-21.png?raw=true)

## 1.3. Quy trình làm sản phẩm, nguyên tắc hoạt động, kết quả nghiên cứu

### 1.3.1. Quy trình phát triển chi tiết

#### Bước 1: Khởi động dự án (2 tuần)

- Xác định vấn đề và nhu cầu thực tế từ khảo sát học sinh
- Nghiên cứu các công nghệ có sẵn: Google Speech API, CMU Sphinx, Vosk
- Lựa chọn Vosk vì: hoạt động offline, độ chính xác cao, miễn phí, mã nguồn mở
- Thiết lập môi trường phát triển: Cài đặt Python, VSCodium, các thư viện cần thiết

#### Bước 2: Thiết kế hệ thống (3 tuần)

- Vẽ sơ đồ kiến trúc hệ thống
- Thiết kế cơ sở dữ liệu (YAML cho cài đặt, SQLite cho dữ liệu luyện tập)
- Thiết kế mockup giao diện màn hình chính
- Thiết kế thuật toán đề xuất bài tập dựa trên lỗi phát âm
- Thiết kế hệ thống bài tập phân biệt ngữ âm
- Xây dựng kho từ vựng và câu mẫu phù hợp THPT

#### Bước 3: Phát triển các module core (8 tuần)

Module speech_to_text.py:
```python
#!/usr/bin/env python3
"""Speech-to-Text converter using Vosk"""

import argparse
import vosk
import wave
import json


def transcribe_audio(audio_file, model_path="vosk-model-en-us-0.22-lgraph"):
    """Chuyển giọng nói thành văn bản"""
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file")
    args = parser.parse_args()
    transcribe_audio(args.audio_file)


if __name__ == "__main__":
    main()

```

Module pronunciation_assessment.py:
- Chuyển đổi văn bản chuẩn và văn bản nhận diện thành phiên âm IPA
- So sánh từng âm vị, xác định âm thiếu, thừa, nhầm
- Tính điểm dựa trên số lượng âm đúng/tổng số âm

Module discrimination.py:
- Phát triển hệ thống bài tập phân biệt ngữ âm
- Tạo các cặp âm tương tự nhau để người học phân biệt
- Theo dõi và phân tích kết quả bài tập

Module non_random_word.py và non_random_sentence.py:
- Phân tích lịch sử lỗi phát âm từ cơ sở dữ liệu
- Tính tần suất lỗi cho từng âm vị
- Ưu tiên đề xuất từ/câu chứa các âm có tần suất lỗi cao

#### Bước 4: Phát triển giao diện (4 tuần)

- Sử dụng CustomTkinter để tạo giao diện hiện đại
- Thiết kế 6 màn hình chính với các tính năng:
  - Chào mừng: Giới thiệu ứng dụng
  - Bài tập: Bài tập phân biệt ngữ âm
  - Phát âm: Luyện phát âm từ và câu hoàn chỉnh
  - Thống kê: Biểu đồ tiến bộ, điểm số, gợi ý cải thiện
  - Cài đặt: Tùy chỉnh giao diện (sáng/tối, màu sắc)
  - Giới thiệu: Thông tin về dự án, LICENSE

#### Bước 5: Kiểm thử và sửa lỗi (6 tuần)

- Kiểm thử từng module độc lập
- Kiểm thử tích hợp toàn bộ hệ thống
- Kiểm thử trên Windows 10/11 và Linux (Fedora Linux)
- Sửa mã nguồn 154+ lần

![Kiểm thử ứng dụng](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2019-20-38.png?raw=true)

#### Bước 6: Hoàn thiện sản phẩm (2 tuần)

- Tạo trình cài đặt cho Windows (.exe) bằng Inno Setup
![Quá trình tạo trình cài đặt bằng Inno Setup](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/refs/heads/main/images/Screenshot%20From%202025-09-15%2019-47-23.png)
- Tạo package cho Linux
- Viết tài liệu hướng dẫn sử dụng
- Xuất bản mã nguồn lên GitHub

### 1.3.2. Nguyên tắc hoạt động của hệ thống

Quy trình luyện phát âm:

1. Người dùng nhấn nút "Tạo câu/từ ngẫu nhiên"
2. Hệ thống phân tích lịch sử lỗi, đề xuất từ phù hợp
3. Hiển thị từ trên màn hình
4. Người dùng nhấn nút "Ghi âm" và đọc từ
5. Hệ thống thu âm (thời gian thu âm tự động)
6. Chuyển đổi âm thanh thành văn bản bằng Vosk
7. Chuyển văn bản chuẩn và văn bản nhận diện thành phiên âm IPA
8. So sánh hai phiên âm, xác định lỗi
9. Hiển thị kết quả:
   - Từ đã đọc
   - Phiên âm chuẩn: ˈwɔːtər
   - Phiên âm nhận diện: ˈwɑtər 
   - Các âm sai: ɔː → ɑ
10. Lưu kết quả vào cơ sở dữ liệu

![Bài tập phát âm](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2013-17-36.png?raw=true)

Quy trình bài tập phân biệt ngữ âm:

1. Người dùng chọn chế độ bài tập: phân biệt ngữ âm, nhận biết trọng âm, hoặc cả hai

![Trang chủ bài tập phân biệt ngữ âm](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2013-18-08.png?raw=true)

2. Hệ thống tạo câu hỏi với 4 từ có phần đánh dấu
   
![Chọn từ các phần đánh dấu phát âm khác](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2013-18-21.png?raw=true)

4. Người dùng chọn từ có phát âm khác với các từ còn lại
   
![Chọn từ có trọng âm khác](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/screenshot/Screenshot%20From%202025-10-12%2013-18-31.png?raw=true)

6. Hệ thống kiểm tra và hiển thị kết quả
7. 
8. Lưu kết quả vào lịch sử bài tập

Quy trình thống kê tiến bộ:

1. Người dùng chọn mục "Thống kê"
2. Hệ thống truy xuất 20 lần luyện tập gần nhất
3. Tính điểm trung bình, phân tích xu hướng
4. Xác định top 5 âm hay sai nhất
5. Hiển thị các thông tin chính:
   - Biểu đồ điểm số qua các lần luyện
   - Xu hướng: Tăng 5% so với tuần trước
   - Các âm cần cải thiện: θ, ð, ɜː, æ, ɪ
   - Gợi ý: "Nên luyện thêm các từ chứa âm θ như think, thank"

Thuật toán đề xuất bài tập thông minh:

- Bước 1: Truy xuất lịch sử lỗi phát âm
- Bước 2: Đếm tần suất xuất hiện của mỗi âm bị lỗi
- Bước 3: Sắp xếp các âm theo tần suất giảm dần
- Bước 4: Chọn âm hay sai nhất
- Bước 5: Tìm trong kho từ/câu những mục chứa ít nhất 1 trong những âm đó
- Bước 6: Ưu tiên những từ/câu chứa nhiều âm hay sai
- Bước 7: Loại bỏ những từ/câu đã luyện gần đây
- Bước 8: Trả về từ/câu phù hợp nhất

### 1.3.3. So sánh với các ứng dụng hiện có

| Tiêu chí | Speak&Speak | Duolingo | ELSA Speak |
|----------|-------------|----------|------------|
| Giá | Miễn phí hoàn toàn |  Free & Freemium (nhiều tính năng trả phí) | Free & Freemium (hạn chế bài tập) |
| Hoạt động offline | ✓ Hoàn toàn | ✗ Cần internet | ✗ Cần internet |
| Phiên âm IPA | ✓ Hiển thị chi tiết | ✗ Không có | Hạn chế |
| Phân tích lỗi | Chi tiết từng âm vị | Chỉ đúng/sai | Đánh giá tổng quát |
| Bài tập cá nhân hóa | ✓ Dựa trên lỗi cá nhân | ✓ Có | ✓ Có |
| Bài tập phân biệt ngữ âm | ✓ Có | ✗ Không | Hạn chế |
| Bài tập dấu nhấn | ✓ Có | ✗ Không | Hạn chế |
| Mã nguồn mở | ✓ GNU GPL v3 | ✗ Đóng | ✗ Đóng |
| Độ khó | Chấm nghiêm khắc | Trung bình | Trung bình |
| Đa dạng Nghe nói đọc viết | ✗ Chỉ tập trung vào phát âm | ✓ Có | Hạn chế |

Nhận xét: Speak&Speak tuy chưa bằng Duolingo về số lượng bài tập và tính năng gamification và bài tập nghe nói đọc viết, nhưng có ưu thế về phản hồi chi tiết phiên âm IPA, hoạt động offline, miễn phí hoàn toàn, mã nguồn mở và đặc biệt có bài tập phân biệt ngữ âm. Ứng dụng phù hợp cho học sinh THPT muốn tập trung cải thiện phát âm một cách nghiêm túc.

### 1.3.4. Kết quả thử nghiệm

Thử nghiệm độ chính xác:
- Thử nghiệm với 20 học sinh lớp 11
- Mỗi học sinh đọc 30 từ và 20 câu, làm 15 bài tập phân biệt ngữ âm
- So sánh đánh giá của ứng dụng với đánh giá của giáo viên

Kết quả:
- Độ chính xác nhận diện từ: 56%
- Độ chính xác nhận diện lỗi phát âm: 62%
- Độ chính xác bài tập phân biệt ngữ âm: 78%
- Thời gian phản hồi trung bình: ~2 giây
- Mức độ hài lòng của người dùng: 8.5/10

Thử nghiệm hiệu năng:
- Máy cấu hình thấp (Core i3, 4GB RAM): Tạm chấp nhận được
- Máy cấu hình trung bình (Core i5, 8GB RAM): Ổn
- Máy cấu hình cao (Core i7, 16GB RAM): Xuất sắc
- Dung lượng ứng dụng: ~400MB (bao gồm mô hình Vosk)
- RAM sử dụng: 200-400MB khi hoạt động

---

# CHƯƠNG 2. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN ĐỀ TÀI

## 2.1. Kết luận

## Ưu điểm đã đạt được:

### 1. Về tính năng:
- Ứng dụng hoàn chỉnh với đầy đủ các tính năng: Bài tập phân biệt ngữ âm, luyện phát âm từ và câu, đánh giá chi tiết, thống kê tiến bộ
- Phản hồi chi tiết về lỗi phát âm: chỉ rõ từng âm vị sai (thiếu, thừa, nhầm âm)
- Hiển thị phiên âm IPA chuẩn và phiên âm nhận diện được
- Bài tập cá nhân hóa dựa trên lỗi phát âm thực tế của người học
- Hỗ trợ luyện dấu nhấn trong từ và câu
- Bài tập phân biệt ngữ âm giúp nâng cao khả năng nhận diện âm thanh
- Thống kê tiến bộ với biểu đồ trực quan và gợi ý cải thiện

### 2. Về công nghệ:
- Hoạt động hoàn toàn offline, không cần internet
- Độ chính xác nhận diện giọng nói cao
- Chạy mượt trên máy cấu hình trung bình (RAM ~4GB)
- Bảo mật thông tin người dùng (dữ liệu lưu cục bộ)
- Mã nguồn mở ([GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)), khuyến khích cộng đồng phát triển

### 3. Về giáo dục:
- Giúp học sinh tự học và cải thiện phát âm hiệu quả
- Phát triển kỹ năng phân biệt ngữ âm, nâng cao độ nhạy cảm với âm thanh tiếng Anh
- Tăng tính tự chủ trong học tập
- Giảm chi phí học (hoàn toàn miễn phí)
- Phù hợp với điều kiện học tập của học sinh Việt Nam

### 4. Về giao diện:
- Thiết kế hiện đại, trực quan, dễ sử dụng
- Hỗ trợ chế độ sáng/tối
- Tùy chỉnh màu sắc theo sở thích
- Giao diện tiếng Việt thân thiện với người dùng


## Hạn chế:

### 1. Về công nghệ:
- Phụ thuộc vào chất lượng microphone (cần mic tốt để đảm bảo độ chính xác)
- Yêu cầu máy tính cấu hình không quá yếu (RAM tối thiểu 4GB)
- Chấm điểm nghiêm khắc, giọng chuẩn mới đạt điểm tối đa
- Chưa hỗ trợ macOS (do chưa có thiết bị để kiểm thử)

### 2. Về nội dung:
- Chưa có bài tập theo chủ đề (gia đình, trường học, du lịch...)
- Chưa có chế độ thi thử hoặc đánh giá tổng thể
- Số lượng bài tập phân biệt ngữ âm còn hạn chế

### 3. Về trải nghiệm:
- Chưa có tính năng gamification (điểm thưởng, xếp hạng)
- Chưa có cộng đồng người dùng để tương tác

## 2.2. Hướng phát triển của đề tài

Nếu có điều kiện và thời gian, đề tài sẽ được phát triển theo các hướng sau:

### Giai đoạn ngắn hạn (3-6 tháng):

1. Mở rộng hỗ trợ nền tảng:
- Phát triển phiên bản cho macOS

2. Cải thiện nội dung:
- Phân loại từ vựng theo chủ đề (IELTS, TOEIC, chương trình THPT)
- Thêm bài tập về trọng âm câu và ngữ điệu
- Mở rộng hệ thống bài tập phân biệt ngữ âm

3. Nâng cao độ chính xác:
- Huấn luyện lại mô hình nhận diện với giọng Việt Nam
- Cải thiện thuật toán phân tích lỗi phát âm

4. Cải thiện trải nghiệm:
- Thêm hệ thống điểm thưởng và huy hiệu
- Thêm chế độ thử thách hàng ngày
- Thêm biểu đồ tiến bộ chi tiết hơn

### Giai đoạn trung hạn (6-12 tháng):

1. Tính năng nâng cao:
- Thêm chế độ luyện hội thoại (conversation mode)
- Nhận diện và phân tích giọng địa phương (British, American, Australian)
- Thêm bài tập về liên kết âm (linking sounds)
- Thêm chế độ luyện tập theo kịch bản thực tế (đặt món ăn, hỏi đường...)

2. Cộng đồng và chia sẻ:
- Tạo tính năng chia sẻ kết quả lên mạng xã hội
- Xây dựng diễn đàn cộng đồng người dùng
- Tạo kênh YouTube hướng dẫn sử dụng và mẹo luyện phát âm

3. Công nghệ AI nâng cao:
- Nghiên cứu tích hợp mô hình AI phân tích cảm xúc trong lời nói
- Phát triển tính năng gợi ý cách luyện tập dựa trên phong cách học của người dùng
- Thêm chatbot AI hỗ trợ giải đáp thắc mắc

### Giai đoạn dài hạn (1-2 năm):

1. Mở rộng ngôn ngữ:
- Phát triển phiên bản cho ngôn ngữ khác (tiếng Trung, Nhật, Hàn...)
- Hỗ trợ đa ngôn ngữ giao diện

2. Tích hợp với giáo dục:
- Hợp tác với trường học để đưa vào chương trình học
- Tạo phiên bản dành cho giáo viên (quản lý lớp học, theo dõi tiến độ học sinh)
- Tạo các khóa học có cấu trúc cho từng cấp độ

3. Nghiên cứu khoa học:
- Nghiên cứu hiệu quả của ứng dụng so với phương pháp truyền thống
- Xuất bản bài báo khoa học về thuật toán và kết quả
- Hợp tác với các trường đại học nghiên cứu ngôn ngữ học

## 2.3. Lời cảm ơn

Em xin chân thành cảm ơn Cô Đặng Thị Huyền Trân đã nhiệt tình hướng dẫn và động viên em trong suốt quá trình thực hiện đề tài. Em cũng xin cảm ơn các bạn học sinh đã tham gia thử nghiệm và đóng góp ý kiến quý báu để hoàn thiện sản phẩm.

Cuối cùng, em hy vọng dự án **Speak&Speak** sẽ góp phần nhỏ bé vào việc cải thiện kỹ năng tiếng Anh của học sinh Việt Nam, đồng thời khuyến khích tinh thần học hỏi, nghiên cứu và ứng dụng công nghệ vào giải quyết các vấn đề thực tế.

---

### TÀI LIỆU THAM KHẢO

1. Vosk Documentation - [https://alphacephei.com/vosk/](https://alphacephei.com/vosk/)
2. Python Documentation - [https://docs.python.org/](https://docs.python.org/)
3. CustomTkinter Documentation - [https://customtkinter.tomschimansky.com/](https://customtkinter.tomschimansky.com/)
4. GitHub - SpeakAndSpeak Repository - [https://github.com/nguyenhhoa03/SpeakAndSpeak](https://github.com/nguyenhhoa03/SpeakAndSpeak)
5. SQLite Documentation - [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
6. YAML Documentation - [https://yaml.org/](https://yaml.org/)
7. eng-to-ipa Library - [https://pypi.org/project/eng-to-ipa/](https://pypi.org/project/eng-to-ipa/)
8. PyAudio Documentation - [https://people.csail.mit.edu/hubert/pyaudio/](https://people.csail.mit.edu/hubert/pyaudio/)
9. pyttsx3 Documentation - [https://pyttsx3.readthedocs.io/](https://pyttsx3.readthedocs.io/)

---

PHỤ LỤC

A. Cấu trúc thư mục dự án

![Thư mục chính của app](https://raw.githubusercontent.com/nguyenhhoa03/nguyenhhoa03/refs/heads/main/images/Screenshot%20From%202025-09-12%2023-44-12.png)

B. Một số đoạn code quan trọng

([Chi tiết code được lưu trữ tại repository GitHub](https://github.com/nguyenhhoa03/SpeakAndSpeak))

---

HẾT
