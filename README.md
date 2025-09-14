# SpeakAndSpeak 🪶

Một ứng dụng đơn giản được thiết kế để giúp bạn cải thiện phát âm tiếng Anh của mình. SpeakAndSpeak cung cấp các bài tập phát âm từ và câu, sử dụng công nghệ chuyển đổi giọng nói thành văn bản (Speech-to-Text) và đánh giá phát âm để cung cấp phản hồi chi tiết.

## Tính năng chính

*   **Luyện phát âm từ:** Thực hành phát âm các từ ngẫu nhiên và nhận phản hồi về độ chính xác.
*   **Luyện phát âm câu:** Luyện tập với các câu ngẫu nhiên để cải thiện ngữ điệu và sự trôi chảy.
*   **Đánh giá phát âm thông minh:** Ứng dụng phân tích lỗi phát âm của bạn, đặc biệt là các âm IPA (International Phonetic Alphabet) bị sai, và đề xuất các từ/câu luyện tập phù hợp để khắc phục.
*   **Thống kê tiến độ:** Theo dõi hiệu suất phát âm của bạn theo thời gian với các số liệu thống kê chi tiết.
*   **Giao diện tùy chỉnh:** Thay đổi chủ đề (theme) và bảng màu (color scheme) của ứng dụng.

## Cài đặt

Để chạy SpeakAndSpeak, cách đơn giản nhất là dùng trình cài đặt đã được build sẵn tại [Github Release](https://github.com/nguyenhhoa03/SpeakAndSpeak/releases/tag/SpeakAndSpeak)

## Cách sử dụng

1.  **Chạy ứng dụng:**
    ```bash
    cd SpeakAndSpeak/app && python3 app.py
    ```
2.  **Chọn tab:**
    *   **Word:** Luyện phát âm từng từ. Nhấn "Random Word" để tạo từ mới, "Listen" để nghe phát âm chuẩn, và "Record" để ghi âm giọng của bạn.
    *   **Sentence:** Luyện phát âm cả câu. Tương tự như tab "Word".
    *   **Statistics:** Xem thống kê chi tiết về hiệu suất phát âm của bạn.
    *   **Settings:** Tùy chỉnh giao diện và ảnh chào mừng.
    *   **About:** Thông tin về ứng dụng.

## Giấy phép

Dự án này được cấp phép theo Giấy phép Công cộng GNU (GNU General Public License) phiên bản 3.0. Xem chi tiết tại [Trang chủ điều khoản](https://www.gnu.org/licenses/gpl-3.0.en.html) (hoặc tệp [LICENSE](https://github.com/nguyenhhoa03/SpeakAndSpeak/blob/main/LICENSE) trong kho lưu trữ này).

### Tài nguyên bên thứ 3
| Tài nguyên | Nguồn gốc | Giấy phép | Ghi chú |
|------------|-----------|-----------|---------|
| vosk-model-en-us-0.22-lgraph | [Alphacephei](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | Cần thay thế bằng thư mục gốc |
| eng_sentences.tsv | [Tatoeba](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2) | [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) & [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | Cần thay thế bằng file gốc |
