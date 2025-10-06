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

Chạy lệnh:
```cmd
md dist 2>nul & copy /Y about.png dist\ & copy /Y app-config.yaml dist\ & copy /Y eng_sentences.tsv dist\ & copy /Y user-data.yaml dist\ & copy /Y welcome.png dist\ & copy /Y arpabet_ipa_database.csv dist\ & copy /Y ipa_confusion_groups.yaml dist\ & copy /Y welcome.ico dist\ & copy /Y LICENSE dist\ & copy /Y SpeakAndSpeak.iss dist\ & pyinstaller --onefile --noconsole --add-binary "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Lib\site-packages\vosk\libvosk.dll;vosk" --add-data "vosk-model-en-us-0.22-lgraph;vosk-model-en-us-0.22-lgraph" --add-data "about.png;." --add-data "app-config.yaml;." --add-data "eng_sentences.tsv;." --add-data "user-data.yaml;." --add-data "welcome.png;." --add-data "arpabet_ipa_database.csv;." --add-data "ipa_confusion_groups.yaml;." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --name "SpeakAndSpeak" app.py & pyinstaller --onefile --noconsole --add-binary "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Lib\site-packages\vosk\libvosk.dll;vosk" --add-data "vosk-model-en-us-0.22-lgraph;vosk-model-en-us-0.22-lgraph" --add-data "arpabet_ipa_database.csv;." --add-data "ipa_confusion_groups.yaml;." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --hidden-import "cmudict" --collect-all "cmudict" --collect-all "pronouncing" --collect-all "customtkinter" --collect-all "wonderwords" --name "discrimination" discrimination.py & move /Y dist\discrimination.exe dist\ 2>nul & cd dist & echo ✅ Build completed! Run with: SpeakAndSpeak.exe & dir
```

### Tạo trình cài đặt

- Copy LICENSE vào dist
- Mở file `dist\SpeakAndSpeak.iss` với **Inno Setup**
- Chọn Build --> Compile

## Linux

### Yêu cầu 
- **python3**
- **git**
- **wget**

### Hướng dẫn build

Điều hướng terminal đến thư mục làm việc và chạy:

```bash
echo "🚀 [$(date)] Starting SpeakAndSpeak build process..." && echo "📥 [$(date)] Cloning repository..." && git clone https://github.com/nguyenhhoa03/SpeakAndSpeak 2>&1 | tee -a build.log || (echo "⚠️  [$(date)] Repository already exists, continuing..." | tee -a build.log) && cd SpeakAndSpeak && echo "📦 [$(date)] Installing Python dependencies..." | tee -a ../build.log && pip install -r requirements.txt 2>&1 | tee -a ../build.log && cd app && echo "🎤 [$(date)] Downloading Vosk speech recognition model..." | tee -a ../../build.log && wget -nc -v https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip 2>&1 | tee -a ../../build.log && echo "📚 [$(date)] Downloading Tatoeba English sentences database..." | tee -a ../../build.log && wget -nc -v https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2 2>&1 | tee -a ../../build.log && echo "📂 [$(date)] Extracting Vosk model..." | tee -a ../../build.log && unzip -o vosk-model-en-us-0.22-lgraph.zip 2>&1 | tee -a ../../build.log && echo "📄 [$(date)] Extracting sentences database..." | tee -a ../../build.log && bunzip2 -fk eng_sentences.tsv.bz2 2>&1 | tee -a ../../build.log && echo "📁 [$(date)] Creating dist directory and copying assets..." | tee -a ../../build.log && mkdir -p dist && cp -f about.png app-config.yaml eng_sentences.tsv user-data.yaml welcome.png arpabet_ipa_database.csv ipa_confusion_groups.yaml dist/ 2>&1 | tee -a ../../build.log && echo "🔧 [$(date)] Starting PyInstaller build for SpeakAndSpeak..." | tee -a ../../build.log && pyinstaller --onefile --noconsole --add-binary "$(python -c 'import vosk, os; print(os.path.join(os.path.dirname(vosk.__file__), "libvosk.so"))'):vosk" --add-data "vosk-model-en-us-0.22-lgraph:vosk-model-en-us-0.22-lgraph" --add-data "about.png:." --add-data "app-config.yaml:." --add-data "eng_sentences.tsv:." --add-data "user-data.yaml:." --add-data "welcome.png:." --add-data "arpabet_ipa_database.csv:." --add-data "ipa_confusion_groups.yaml:." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --name "SpeakAndSpeak" app.py 2>&1 | tee -a ../../build.log && echo "🎯 [$(date)] Starting PyInstaller build for discrimination..." | tee -a ../../build.log && pyinstaller --onefile --noconsole --add-binary "$(python -c 'import vosk, os; print(os.path.join(os.path.dirname(vosk.__file__), "libvosk.so"))'):vosk" --add-data "vosk-model-en-us-0.22-lgraph:vosk-model-en-us-0.22-lgraph" --add-data "arpabet_ipa_database.csv:." --add-data "ipa_confusion_groups.yaml:." --icon "welcome.ico" --hidden-import "PIL._tkinter_finder" --hidden-import "cmudict" --collect-all "cmudict" --collect-all "pronouncing" --collect-all "customtkinter" --collect-all "wonderwords" --name "discrimination" discrimination.py 2>&1 | tee -a ../../build.log && mv -f dist/discrimination dist/ 2>/dev/null && cd dist && echo "📊 [$(date)] Build summary:" | tee -a ../../../build.log && echo "📁 Files in dist directory:" | tee -a ../../../build.log && ls -la | tee -a ../../../build.log && echo "💾 Archive files preserved:" | tee -a ../../../build.log && ls -la ../*.zip ../*.bz2 2>/dev/null | tee -a ../../../build.log || echo "No archive files found" | tee -a ../../../build.log && echo "🎯 Executable info:" | tee -a ../../../build.log && file SpeakAndSpeak discrimination 2>/dev/null | tee -a ../../../build.log && echo "📏 File sizes:" | tee -a ../../../build.log && du -h SpeakAndSpeak discrimination | tee -a ../../../build.log && echo "✅ [$(date)] Build completed successfully!" | tee -a ../../../build.log && echo "🚀 Run with: ./SpeakAndSpeak" | tee -a ../../../build.log && echo "📋 Full build log saved to: $(pwd)/../../../build.log"
```

Vậy là xong.
