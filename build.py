#!/usr/bin/env python3
"""
SpeakAndSpeak Auto Build Script
Supports: Windows & Linux
Languages: English (Default) & Vietnamese
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import bz2
import shutil
import sqlite3
from pathlib import Path

# Configuration
VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
VOSK_MODEL_NAME = "vosk-model-en-us-0.22-lgraph"
SENTENCES_URL = "https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2"
SENTENCES_FILE = "eng_sentences.tsv"

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message, color=Colors.CYAN):
    """Print colored step message"""
    print(f"\n{color}{'='*60}{Colors.END}")
    print(f"{color}{Colors.BOLD}🔨 {message}{Colors.END}")
    print(f"{color}{'='*60}{Colors.END}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def select_language():
    """Ask user to select build language"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║     SpeakAndSpeak Build - Language Selection         ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    print(f"{Colors.CYAN}Please select the build language:{Colors.END}")
    print(f"  {Colors.BOLD}1.{Colors.END} English (Default)")
    print(f"  {Colors.BOLD}2.{Colors.END} Tiếng Việt (Vietnamese)")
    print()
    
    while True:
        try:
            choice = input(f"{Colors.YELLOW}Enter your choice (1 or 2): {Colors.END}").strip()
            if choice == "1":
                print_success("Selected: English (Default)")
                return "en"
            elif choice == "2":
                print_success("Selected: Tiếng Việt (Vietnamese)")
                return "vi"
            else:
                print_error("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Build cancelled by user{Colors.END}")
            sys.exit(1)

def check_python_version():
    """Check if Python version is adequate"""
    print_step("Checking Python version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error(f"Python 3.7+ required. Current: {version.major}.{version.minor}")
        sys.exit(1)
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")

def install_requirements():
    """Install required Python packages"""
    print_step("Installing Python dependencies")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("All dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        sys.exit(1)

def download_file(url, filename):
    """Download file with progress indicator"""
    print(f"📥 Downloading {filename}...")
    try:
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r   Progress: {percent}% ")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, reporthook)
        print()  # New line after progress
        print_success(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print_error(f"Failed to download {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to="."):
    """Extract ZIP file"""
    print(f"📦 Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print_success(f"Extracted to: {extract_to}")
        return True
    except Exception as e:
        print_error(f"Failed to extract {zip_path}: {e}")
        return False

def extract_bz2(bz2_path, output_path):
    """Extract BZ2 file"""
    print(f"📦 Extracting {bz2_path}...")
    try:
        with bz2.open(bz2_path, 'rb') as source, open(output_path, 'wb') as dest:
            shutil.copyfileobj(source, dest)
        print_success(f"Extracted to: {output_path}")
        return True
    except Exception as e:
        print_error(f"Failed to extract {bz2_path}: {e}")
        return False

def tsv_to_sqlite(tsv_path, db_path):
    """Convert TSV file to SQLite database"""
    print_step("Converting TSV to SQLite database")
    try:
        # Create database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentences (
                id INTEGER PRIMARY KEY,
                lang TEXT,
                sentence TEXT
            )
        ''')
        
        # Read and insert data
        print("📊 Reading TSV file...")
        with open(tsv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📝 Inserting {len(lines)} sentences into database...")
        batch_size = 1000
        for i in range(0, len(lines), batch_size):
            batch = []
            for line in lines[i:i+batch_size]:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    batch.append((int(parts[0]), parts[1], parts[2]))
            
            cursor.executemany('INSERT OR REPLACE INTO sentences VALUES (?, ?, ?)', batch)
            percent = min(100, int((i + batch_size) * 100 / len(lines)))
            sys.stdout.write(f"\r   Progress: {percent}% ")
            sys.stdout.flush()
        
        print()  # New line
        conn.commit()
        
        # Create index for faster queries
        print("🔍 Creating index...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_lang ON sentences(lang)')
        conn.commit()
        
        conn.close()
        print_success(f"Database created: {db_path}")
        print(f"   Total sentences: {len(lines)}")
        return True
    except Exception as e:
        print_error(f"Failed to convert TSV to SQLite: {e}")
        return False

def check_resources():
    """Check and download missing resources"""
    print_step("Checking resources")
    
    # Check Vosk model
    if not os.path.exists(VOSK_MODEL_NAME):
        print_warning(f"Vosk model not found: {VOSK_MODEL_NAME}")
        zip_file = f"{VOSK_MODEL_NAME}.zip"
        if not os.path.exists(zip_file):
            if not download_file(VOSK_MODEL_URL, zip_file):
                return False
        if not extract_zip(zip_file):
            return False
    else:
        print_success(f"Vosk model found: {VOSK_MODEL_NAME}")
    
    # Check sentences file
    if not os.path.exists(SENTENCES_FILE):
        print_warning(f"Sentences file not found: {SENTENCES_FILE}")
        bz2_file = f"{SENTENCES_FILE}.bz2"
        if not os.path.exists(bz2_file):
            if not download_file(SENTENCES_URL, bz2_file):
                return False
        if not extract_bz2(bz2_file, SENTENCES_FILE):
            return False
    else:
        print_success(f"Sentences file found: {SENTENCES_FILE}")
    
    return True

def get_vosk_lib_path():
    """Get platform-specific Vosk library path"""
    system = platform.system()
    try:
        if system == "Windows":
            import vosk
            vosk_dir = Path(vosk.__file__).parent
            lib_path = vosk_dir / "libvosk.dll"
            return str(lib_path)
        else:  # Linux/Mac
            result = subprocess.run(
                [sys.executable, "-c", 
                 "import vosk, os; print(os.path.join(os.path.dirname(vosk.__file__), 'libvosk.so'))"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
    except Exception as e:
        print_error(f"Failed to locate Vosk library: {e}")
        sys.exit(1)

def prepare_dist():
    """Prepare dist directory"""
    print_step("Preparing dist directory")
    
    # Create dist directory
    os.makedirs("dist", exist_ok=True)
    
    # Convert TSV to SQLite
    db_path = "dist/eng_sentences.db"
    if not tsv_to_sqlite(SENTENCES_FILE, db_path):
        return False
    
    # Copy required files
    files_to_copy = [
        "about.png",
        "app-config.yaml",
        "user-data.yaml",
        "welcome.png",
        "arpabet_ipa_database.csv",
        "ipa_confusion_groups.yaml",
        "../LICENSE"  # Copy from parent directory
    ]
    
    print("📋 Copying resource files...")
    for file in files_to_copy:
        src = file
        dst = os.path.join("dist", os.path.basename(file))
        try:
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print_success(f"Copied: {os.path.basename(file)}")
            else:
                print_warning(f"File not found: {file}")
        except Exception as e:
            print_error(f"Failed to copy {file}: {e}")
    
    return True

def check_source_files(lang):
    """Check if source files exist for the selected language"""
    print_step("Checking source files")
    
    suffix = ".vi.py" if lang == "vi" else ".py"
    app_file = f"app{suffix}" if lang == "vi" else "app.py"
    disc_file = f"discrimination{suffix}" if lang == "vi" else "discrimination.py"
    
    missing_files = []
    if not os.path.exists(app_file):
        missing_files.append(app_file)
    if not os.path.exists(disc_file):
        missing_files.append(disc_file)
    
    if missing_files:
        print_error(f"Missing source files: {', '.join(missing_files)}")
        return False, None, None
    
    print_success(f"Found: {app_file}")
    print_success(f"Found: {disc_file}")
    return True, app_file, disc_file

def build_executable(name, script, vosk_lib):
    """Build executable with PyInstaller"""
    print_step(f"Building {name}")
    
    system = platform.system()
    separator = ";" if system == "Windows" else ":"
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f"--add-binary={vosk_lib}{separator}vosk",
        f"--add-data={VOSK_MODEL_NAME}{separator}{VOSK_MODEL_NAME}",
        f"--add-data=arpabet_ipa_database.csv{separator}.",
        f"--add-data=ipa_confusion_groups.yaml{separator}.",
        "--icon=welcome.ico",
        "--hidden-import=PIL._tkinter_finder",
    ]
    
    if name == "SpeakAndSpeak":
        cmd.extend([
            f"--add-data=about.png{separator}.",
            f"--add-data=app-config.yaml{separator}.",
            f"--add-data=dist/eng_sentences.db{separator}.",
            f"--add-data=user-data.yaml{separator}.",
            f"--add-data=welcome.png{separator}.",
        ])
    else:  # discrimination
        cmd.extend([
            "--hidden-import=cmudict",
            "--collect-all=cmudict",
            "--collect-all=pronouncing",
            "--collect-all=customtkinter",
            "--collect-all=wonderwords",
        ])
    
    cmd.extend([f"--name={name}", script])
    
    try:
        subprocess.check_call(cmd)
        print_success(f"{name} built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to build {name}: {e}")
        return False

def main():
    """Main build process"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║     SpeakAndSpeak Auto Build Script                 ║")
    print("║     Platform: {:<40}║".format(platform.system()))
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Select language first
    lang = select_language()
    
    # Change to app directory
    if os.path.exists("app"):
        os.chdir("app")
        print(f"📂 Working directory: {os.getcwd()}\n")
    
    # Check source files
    files_ok, app_file, disc_file = check_source_files(lang)
    if not files_ok:
        print_error("Source file check failed")
        sys.exit(1)
    
    # Build steps
    check_python_version()
    
    print_step("Installing requirements")
    os.chdir("..")  # Go back to install requirements
    install_requirements()
    os.chdir("app")  # Return to app directory
    
    if not check_resources():
        print_error("Resource check failed")
        sys.exit(1)
    
    if not prepare_dist():
        print_error("Failed to prepare dist directory")
        sys.exit(1)
    
    vosk_lib = get_vosk_lib_path()
    print(f"📚 Vosk library: {vosk_lib}\n")
    
    # Build executables with selected language files
    if not build_executable("SpeakAndSpeak", app_file, vosk_lib):
        sys.exit(1)
    
    if not build_executable("discrimination", disc_file, vosk_lib):
        sys.exit(1)
    
    # Move executables to dist
    print_step("Organizing build output")
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    
    for exe in ["SpeakAndSpeak", "discrimination"]:
        src = f"dist/{exe}{exe_ext}"
        if os.path.exists(src):
            print_success(f"Found: {exe}{exe_ext}")
    
    # Final message
    lang_name = "Vietnamese" if lang == "vi" else "English"
    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║          BUILD COMPLETED SUCCESSFULLY!               ║")
    print("║          Language: {:<35}║".format(lang_name))
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    print(f"\n📂 Output directory: {os.path.abspath('dist')}")
    print(f"🚀 Run: ./dist/SpeakAndSpeak{exe_ext}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Build cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
