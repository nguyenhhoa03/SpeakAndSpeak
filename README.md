# SpeakAndSpeak 🪶

Một ứng dụng đơn giản được thiết kế để giúp bạn cải thiện phát âm tiếng Anh của mình. SpeakAndSpeak cung cấp các bài tập phát âm từ và câu, sử dụng công nghệ chuyển đổi giọng nói thành văn bản (Speech-to-Text) và đánh giá phát âm để cung cấp phản hồi chi tiết.

## Tính năng chính

*   **Luyện phát âm từ:** Thực hành phát âm các từ ngẫu nhiên và nhận phản hồi về độ chính xác.
*   **Luyện phát âm câu:** Luyện tập với các câu ngẫu nhiên để cải thiện ngữ điệu và sự trôi chảy.
*   **Đánh giá phát âm thông minh:** Ứng dụng phân tích lỗi phát âm của bạn, đặc biệt là các âm IPA (International Phonetic Alphabet) bị sai, và đề xuất các từ/câu luyện tập phù hợp để khắc phục.
*   **Thống kê tiến độ:** Theo dõi hiệu suất phát âm của bạn theo thời gian với các số liệu thống kê chi tiết.
*   **Giao diện tùy chỉnh:** Thay đổi chủ đề (theme) và bảng màu (color scheme) của ứng dụng.

## Cài đặt

Để chạy SpeakAndSpeak, bạn cần cài đặt các thư viện Python cần thiết và công cụ `sox`.

### 1. Cài đặt `sox`

`sox` (Sound eXchange) là một công cụ xử lý âm thanh dòng lệnh cần thiết để ghi âm trong ứng dụng.

*   **Trên Windows:**
    (Trong dự án này, `sox` được thay thế bằng ffmpeg, vui lòng thay thế bằng file ffmpeg gốc tại [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) hoặc chỉ tải mã nguồn ở bước 2).

*   **Trên macOS:**
    Sử dụng Homebrew:
    ```bash
    brew install sox
    ```

*   **Trên Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get install sox libsox-fmt-all
    ```

### 2. Tải toàn bộ mã nguồn
Toàn bộ mã nguồn có thể tải tại [Mega Mirror](https://mega.nz/file/VOcAzRYa#vkQWT2jf9dLLV0JpXovf4sbl6z_YObhjcQittbr2gF4) hoặc [Google Drive](https://drive.google.com/file/d/1OZztGiC7oW7LPIsmkX9O77Dr-2fsvkAd/view?usp=drive_link)

### 3. Cài đặt thư viện Python

Sử dụng `pip` để cài đặt các thư viện cần thiết từ `requirements.txt`:

```bash
pip install -r requirements.txt
```


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
| about.png | [Fandom](https://genshin-impact.fandom.com/wiki/Chat/Gallery) | [CC BY-SA](https://www.fandom.com/licensing) | Không cần thay thế |
| vosk-model-en-us-0.22-lgraph | [Alphacephei](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | Cần thay thế bằng thư mục gốc |
| eng_sentences.tsv | [Tatoeba](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2) | [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) & [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | Cần thay thế bằng file gốc |
| sox-14.4.2rc2-win32.exe | [Sourceforge](https://sourceforge.net/projects/sox/) | [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) & [LGPLv2](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html) | Không cần thay thế |
| FFmpeg | [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) | [LGPL 2.1+](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html) | Cần thay thế bằng file gốc |
