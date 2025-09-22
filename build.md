# Hướng dẫn biên dịch và đóng gói SpeakAndSpeak
## Windows
### Yêu cầu
- [Python](https://www.python.org/downloads/)
- [vosk-model-en-us-0.22-lgraph](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) từ Alphacephei
- [eng_sentences.tsv](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2) từ Tatoeba
- [Inno Setup](https://jrsoftware.org/isdl.php#stable)
- Trình giải nén: Khuyến nghị dùng [7-zip](https://www.7-zip.org/)
- Mã nguồn dự án [SpeakAndSpeak](https://github.com/nguyenhhoa03/SpeakAndSpeak/archive/refs/heads/main.zip)
### Hướng dẫn build
- Cài đặt thư viện cần thiết
```cmd
pip install -r requirements.txt
```
- Giải nén [vosk-model-en-us-0.22-lgraph](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) và [eng_sentences.tsv](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2) thay thế vào 2 files **vosk-model-en-us-0.22-lgraph** và **eng_sentences.tsv** trong thư mục `app`
- Điều hướng `cmd` vào thư mục app

## Linux
### Yêu cầu 
- **python3**
- **git**
- **wget**
