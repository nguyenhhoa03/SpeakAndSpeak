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

Chạy lệnh
```cmd
md dist 2>nul & copy about.png dist\ 2>nul & copy app-config.yaml dist\ 2>nul & copy eng_sentences.tsv dist\ 2>nul & copy user-data.yaml dist\ 2>nul & copy welcome.png dist\ 2>nul & pyinstaller --onefile --noconsole --add-binary "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Lib\site-packages\vosk\libvosk.dll;vosk" --add-data "vosk-model-en-us-0.22-lgraph;vosk-model-en-us-0.22-lgraph" --add-data "about.png;." --add-data "app-config.yaml;." --add-data "eng_sentences.tsv;." --add-data "user-data.yaml;." --add-data "welcome.png;." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --name "SpeakAndSpeak" app.py & cd dist & echo ✅ Build completed! Run with: SpeakAndSpeak.exe & dir
```
### Tạo trình cài đặt
- Copy các file: `welcome.ico`, `LICENSE`, `SpeakAndSpeak.iss` vào trong thư mục dist
- Đổi tên file `SpeakAndSpeak.exe` thành `app.exe`
- Mở file `SpeakAndSpeak.iss` với **Inno Setup**
- Chọn Build --> Compile

## Linux
### Yêu cầu 
- **python3**
- **git**
- **wget**
 ### Hướng dẫn build
  Điều hướng terminal đến thư mục làm việc và chạy
  ```bash
# Lệnh build SpeakAndSpeak một dòng - copy và paste vào terminal:

echo "Downloading source code and installing dependencies..."; git clone https://github.com/nguyenhhoa03/SpeakAndSpeak 2>/dev/null || echo "Repository exists"; cd SpeakAndSpeak; pip install -r requirements.txt; cd app; wget -nc https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip; wget -nc https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2; unzip -o vosk-model-en-us-0.22-lgraph.zip; bunzip2 -f eng_sentences.tsv.bz2; rm -f vosk-model-en-us-0.22-lgraph.zip eng_sentences.tsv.bz2; mkdir -p dist; cp about.png app-config.yaml eng_sentences.tsv user-data.yaml welcome.png dist/ 2>/dev/null || true; pyinstaller --onefile --noconsole --add-binary "$(python -c 'import vosk, os; print(os.path.join(os.path.dirname(vosk.__file__), "libvosk.so"))'):vosk" --add-data "vosk-model-en-us-0.22-lgraph:vosk-model-en-us-0.22-lgraph" --add-data "about.png:." --add-data "app-config.yaml:." --add-data "eng_sentences.tsv:." --add-data "user-data.yaml:." --add-data "welcome.png:." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --name "SpeakAndSpeak" app.py; cd dist; echo "✅ Build completed! Run with: ./SpeakAndSpeak"; ls -la
```
Vậy là xong.
