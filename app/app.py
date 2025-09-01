import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
import platform
import os
import yaml
import pyttsx3
import webbrowser
from PIL import Image
import time

# Import các module đánh giá (không có fallback như yêu cầu)
from non_random_word import generate_word
from non_random_sentence import generate_sentence
from speech_to_text import transcribe_audio
from pronunciation_assessment import assess_pronunciation
from user_statistics import analyze_pronunciation_data

class SpeakAndSpeakApp:
    def __init__(self):
        # Khởi tạo cửa sổ chính
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Speak & Speak - English Pronunciation Practice")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Load config
        self.load_config()
        
        # Khởi tạo TTS engine
        self.tts_engine = pyttsx3.init()
        
        # Variables
        self.current_word = ""
        self.current_sentence = ""
        self.is_recording = False
        
        # Tạo giao diện
        self.create_widgets()
        
    def load_config(self):
        """Load cấu hình từ app-config.yaml"""
        try:
            with open("app-config.yaml", "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            
            # Áp dụng theme và color scheme
            ctk.set_appearance_mode(self.config["theme"]["current"])
            ctk.set_default_color_theme(self.config["color_scheme"]["current"])
            
        except FileNotFoundError:
            # Tạo config mặc định
            self.config = {
                "theme": {
                    "available": ["light", "dark", "system"],
                    "current": "system"
                },
                "color_scheme": {
                    "available": ["blue", "green", "dark-blue"],
                    "current": "dark-blue"
                }
            }
            self.save_config()
    
    def save_config(self):
        """Lưu cấu hình vào app-config.yaml"""
        with open("app-config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def create_widgets(self):
        """Tạo giao diện chính"""
        # Tạo notebook (tab container)
        self.tabview = ctk.CTkTabview(self.root, width=880, height=680)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tạo các tab
        self.welcome_tab = self.tabview.add("Welcome")
        self.word_tab = self.tabview.add("Word")
        self.sentence_tab = self.tabview.add("Sentence")
        self.statistics_tab = self.tabview.add("Statistics")
        self.settings_tab = self.tabview.add("Settings")
        self.about_tab = self.tabview.add("About")
        
        # Setup từng tab
        self.setup_welcome_tab()
        self.setup_word_tab()
        self.setup_sentence_tab()
        self.setup_statistics_tab()
        self.setup_settings_tab()
        self.setup_about_tab()
    
    def setup_welcome_tab(self):
        """Setup tab Welcome"""

        # Frame chính
        main_frame = ctk.CTkFrame(self.welcome_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Hiển thị ảnh welcome
        try:
            welcome_img = Image.open("welcome.png")
            welcome_w, welcome_h = welcome_img.size
            new_welcome_w = 300
            new_welcome_h = int(welcome_h * (new_welcome_w / welcome_w))
            welcome_image = ctk.CTkImage(welcome_img, size=(new_welcome_w, new_welcome_h))
            
            image_label = ctk.CTkLabel(main_frame, image=welcome_image, text="")
            image_label.pack(pady=(50, 20))
        except FileNotFoundError:
            # Placeholder nếu không có ảnh
            placeholder_label = ctk.CTkLabel(
                main_frame, 
                text="Welcome Image\n(welcome.png not found)",
                font=ctk.CTkFont(size=20),
                width=300,
                height=200
            )
            placeholder_label.pack(pady=(50, 20))
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            main_frame,
            text="Welcome back! Ready to start?",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_label.pack(pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        # Word button
        word_button = ctk.CTkButton(
            button_frame,
            text="Word",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=150,
            height=50,
            command=lambda: self.tabview.set("Word")
        )
        word_button.pack(side="left", padx=20, pady=20)
        
        # Sentence button
        sentence_button = ctk.CTkButton(
            button_frame,
            text="Sentence",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=150,
            height=50,
            command=lambda: self.tabview.set("Sentence")
        )
        sentence_button.pack(side="left", padx=20, pady=20)
    
    def setup_word_tab(self):
        """Setup tab Word"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.word_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Word display
        self.word_label = ctk.CTkLabel(
            main_frame,
            text="Click 'Random Word' to start!",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.word_label.pack(pady=30)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=20)
        
        # Random word button
        random_word_btn = ctk.CTkButton(
            control_frame,
            text="Random Word",
            command=self.generate_random_word,
            width=120,
            height=35
        )
        random_word_btn.pack(side="left", padx=10, pady=10)
        
        # Listen button
        listen_word_btn = ctk.CTkButton(
            control_frame,
            text="Listen",
            command=self.speak_word,
            width=100,
            height=35
        )
        listen_word_btn.pack(side="left", padx=10, pady=10)
        
        # Record button
        self.record_word_btn = ctk.CTkButton(
            control_frame,
            text="Record (3s)",
            command=lambda: self.start_recording(3, self.process_word_recording),
            width=120,
            height=35
        )
        self.record_word_btn.pack(side="left", padx=10, pady=10)
        
        # Progress bar
        self.word_progress = ctk.CTkProgressBar(main_frame, width=600)
        self.word_progress.pack(pady=10)
        self.word_progress.set(0)
        
        # Status label
        self.word_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.word_status.pack(pady=10)
        
        # Result text area
        self.word_result_frame = ctk.CTkScrollableFrame(main_frame, width=750, height=250)
        self.word_result_frame.pack(fill="both", expand=True, pady=20)
        
        self.word_result_text = ctk.CTkTextbox(self.word_result_frame, wrap="word")
        self.word_result_text.pack(fill="both", expand=True)
    
    def setup_sentence_tab(self):
        """Setup tab Sentence"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.sentence_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sentence display
        self.sentence_label = ctk.CTkLabel(
            main_frame,
            text="Click 'Random Sentence' to start!",
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=700
        )
        self.sentence_label.pack(pady=30)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=20)
        
        # Random sentence button
        random_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Random Sentence",
            command=self.generate_random_sentence,
            width=140,
            height=35
        )
        random_sentence_btn.pack(side="left", padx=10, pady=10)
        
        # Listen button
        listen_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Listen",
            command=self.speak_sentence,
            width=100,
            height=35
        )
        listen_sentence_btn.pack(side="left", padx=10, pady=10)
        
        # Record button
        self.record_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Record (7s)",
            command=lambda: self.start_recording(7, self.process_sentence_recording),
            width=120,
            height=35
        )
        self.record_sentence_btn.pack(side="left", padx=10, pady=10)
        
        # Progress bar
        self.sentence_progress = ctk.CTkProgressBar(main_frame, width=600)
        self.sentence_progress.pack(pady=10)
        self.sentence_progress.set(0)
        
        # Status label
        self.sentence_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.sentence_status.pack(pady=10)
        
        # Result text area
        self.sentence_result_frame = ctk.CTkScrollableFrame(main_frame, width=750, height=250)
        self.sentence_result_frame.pack(fill="both", expand=True, pady=20)
        
        self.sentence_result_text = ctk.CTkTextbox(self.sentence_result_frame, wrap="word")
        self.sentence_result_text.pack(fill="both", expand=True)
    
    def setup_statistics_tab(self):
        """Setup tab Statistics"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.statistics_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Load button
        load_stats_btn = ctk.CTkButton(
            main_frame,
            text="Load Statistics",
            command=self.load_statistics,
            width=150,
            height=40
        )
        load_stats_btn.pack(pady=20)
        
        # Status label
        self.stats_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.stats_status.pack(pady=10)
        
        # Result text area
        self.stats_result_frame = ctk.CTkScrollableFrame(main_frame, width=750, height=500)
        self.stats_result_frame.pack(fill="both", expand=True, pady=20)
        
        self.stats_result_text = ctk.CTkTextbox(self.stats_result_frame, wrap="word")
        self.stats_result_text.pack(fill="both", expand=True)
    
    def setup_settings_tab(self):
        """Setup tab Settings"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.settings_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Theme settings
        theme_frame = ctk.CTkFrame(main_frame)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:", font=ctk.CTkFont(size=16, weight="bold"))
        theme_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.theme_var = ctk.StringVar(value=self.config["theme"]["current"])
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=self.config["theme"]["available"],
            command=self.change_theme
        )
        theme_menu.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Color scheme settings
        color_frame = ctk.CTkFrame(main_frame)
        color_frame.pack(fill="x", padx=20, pady=10)
        
        color_label = ctk.CTkLabel(color_frame, text="Color Scheme:", font=ctk.CTkFont(size=16, weight="bold"))
        color_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.color_var = ctk.StringVar(value=self.config["color_scheme"]["current"])
        color_menu = ctk.CTkOptionMenu(
            color_frame,
            variable=self.color_var,
            values=self.config["color_scheme"]["available"],
            command=self.change_color_scheme
        )
        color_menu.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Welcome image settings
        image_frame = ctk.CTkFrame(main_frame)
        image_frame.pack(fill="x", padx=20, pady=10)
        
        image_label = ctk.CTkLabel(image_frame, text="Welcome Image:", font=ctk.CTkFont(size=16, weight="bold"))
        image_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        change_image_btn = ctk.CTkButton(
            image_frame,
            text="Choose Welcome Image",
            command=self.change_welcome_image,
            width=200,
            height=35
        )
        change_image_btn.pack(anchor="w", padx=20, pady=(0, 20))
    
    def setup_about_tab(self):
        """Setup tab About"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.about_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # About image
        try:
            about_img = Image.open("about.png")
            about_w, about_h = about_img.size
            new_about_w = 300
            new_about_h = int(about_h * (new_about_w / about_w))
            about_image = ctk.CTkImage(about_img, size=(new_about_w, new_about_h))
            image_label = ctk.CTkLabel(main_frame, image=about_image, text="")
            image_label.pack(pady=(50, 20))
        except FileNotFoundError:
            # Placeholder nếu không có ảnh
            placeholder_label = ctk.CTkLabel(
                main_frame, 
                text="About Image\n(about.png not found)",
                font=ctk.CTkFont(size=20),
                width=300,
                height=200
            )
            placeholder_label.pack(pady=(50, 20))
        
        # App name
        app_name = ctk.CTkLabel(
            main_frame,
            text="Speak & Speak",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        app_name.pack(pady=20)
        
        # Version
        version_label = ctk.CTkLabel(
            main_frame,
            text="version 1.0",
            font=ctk.CTkFont(size=16)
        )
        version_label.pack(pady=10)
        
        # GitHub link
        github_link = ctk.CTkLabel(
            main_frame,
            text="https://github.com/nguyenhhoa03/SpeakAndSpeak",
            font=ctk.CTkFont(size=14, underline=True),
            text_color=("blue", "lightblue"),
            cursor="hand2"
        )
        github_link.pack(pady=20)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/nguyenhhoa03/SpeakAndSpeak"))
    
    def generate_random_word(self):
        """Tạo từ ngẫu nhiên"""
        try:
            self.current_word = generate_word("user-data.yaml")
            self.word_label.configure(text=self.current_word)
            self.word_result_text.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate word: {str(e)}")
    
    def generate_random_sentence(self):
        """Tạo câu ngẫu nhiên"""
        try:
            self.current_sentence = generate_sentence("user-data.yaml")
            self.sentence_label.configure(text=self.current_sentence)
            self.sentence_result_text.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate sentence: {str(e)}")
    
    def speak_word(self):
        """Phát âm từ"""
        if self.current_word:
            threading.Thread(target=self._speak_text, args=(self.current_word,)).start()
        else:
            messagebox.showwarning("Warning", "Please generate a word first!")
    
    def speak_sentence(self):
        """Phát âm câu"""
        if self.current_sentence:
            threading.Thread(target=self._speak_text, args=(self.current_sentence,)).start()
        else:
            messagebox.showwarning("Warning", "Please generate a sentence first!")
    
    def _speak_text(self, text):
        """Helper function để phát âm text"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def start_recording(self, duration, callback):
        """Bắt đầu ghi âm"""
        if self.is_recording:
            return
        
        self.is_recording = True
        threading.Thread(target=self._record_audio, args=(duration, callback)).start()
    
    def _record_audio(self, duration, callback):
        """Ghi âm audio"""
        try:
            # Determine sox command based on OS
            system = platform.system()
            if system == "Windows":
                sox_path = "./sox.exe"
            else:
                sox_path = "sox"
            
            # Update progress bar
            progress_bar = self.word_progress if duration == 3 else self.sentence_progress
            status_label = self.word_status if duration == 3 else self.sentence_status
            
            status_label.configure(text="Recording...")
            
            # Record audio command with sox - high quality settings
            if system == "Windows":
                cmd = [sox_path, "-t", "waveaudio", "-d", "-r", "44100", "-c", "1", "-b", "16", "audio.wav", "trim", "0", str(duration)]
            else:
                # Linux/Mac - high quality settings
                cmd = [sox_path, "-t", "alsa", "default", "-r", "44100", "-c", "1", "-b", "16", "audio.wav", "trim", "0", str(duration)]
            
            # Start ffmpeg process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Update progress bar while recording
            for i in range(duration * 10):
                if process.poll() is not None:  # Process finished early
                    break
                progress = (i + 1) / (duration * 10)
                progress_bar.set(progress)
                time.sleep(0.1)
            
            # Wait for process to complete and get result
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd, stderr)
            
            status_label.configure(text="Recording completed!")
            progress_bar.set(0)
            
            # Process the recording
            callback()
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Recording failed: {e}"
            self.root.after(0, lambda msg=error_msg: status_label.configure(text=msg))
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda msg=error_msg: status_label.configure(text=msg))
        finally:
            self.is_recording = False
    
    def process_word_recording(self):
        """Xử lý ghi âm từ"""
        self.word_status.configure(text="Đang xử lý...")
        threading.Thread(target=self._process_word_audio).start()
    
    def _process_word_audio(self):
        """Xử lý audio từ"""
        try:
            # Transcribe audio
            transcribed_text = transcribe_audio("audio.wav")
            
            # Assess pronunciation
            result = assess_pronunciation(self.current_word, transcribed_text)
            
            # Update UI
            self.root.after(0, lambda: self._update_word_result(result))
            self.root.after(0, lambda: self.word_status.configure(text="Processing completed!"))
            
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda msg=error_msg: self.word_status.configure(text=msg))
    
    def _update_word_result(self, result):
        """Cập nhật kết quả từ"""
        self.word_result_text.delete("1.0", "end")
        self.word_result_text.insert("1.0", result)
    
    def process_sentence_recording(self):
        """Xử lý ghi âm câu"""
        self.sentence_status.configure(text="Đang xử lý...")
        threading.Thread(target=self._process_sentence_audio).start()
    
    def _process_sentence_audio(self):
        """Xử lý audio câu"""
        try:
            # Transcribe audio
            transcribed_text = transcribe_audio("audio.wav")
            
            # Assess pronunciation
            result = assess_pronunciation(self.current_sentence, transcribed_text)
            
            # Update UI
            self.root.after(0, lambda: self._update_sentence_result(result))
            self.root.after(0, lambda: self.sentence_status.configure(text="Processing completed!"))
            
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda msg=error_msg: self.sentence_status.configure(text=msg))
    
    def _update_sentence_result(self, result):
        """Cập nhật kết quả câu"""
        self.sentence_result_text.delete("1.0", "end")
        self.sentence_result_text.insert("1.0", result)
    
    def load_statistics(self):
        """Load thống kê"""
        self.stats_status.configure(text="Đang xử lý...")
        threading.Thread(target=self._load_stats).start()
    
    def _load_stats(self):
        """Load thống kê trong thread riêng"""
        try:
            result = analyze_pronunciation_data("user-data.yaml")
            self.root.after(0, lambda: self._update_stats_result(result))
            self.root.after(0, lambda: self.stats_status.configure(text="Statistics loaded!"))
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda msg=error_msg: self.stats_status.configure(text=msg))
    
    def _update_stats_result(self, result):
        """Cập nhật kết quả thống kê"""
        self.stats_result_text.delete("1.0", "end")
        self.stats_result_text.insert("1.0", result)
    
    def change_theme(self, theme):
        """Thay đổi theme"""
        self.config["theme"]["current"] = theme
        self.save_config()
        ctk.set_appearance_mode(theme)
    
    def change_color_scheme(self, color_scheme):
        """Thay đổi color scheme"""
        self.config["color_scheme"]["current"] = color_scheme
        self.save_config()
        messagebox.showinfo("Info", "Please restart the app to apply color scheme changes.")
    
    def change_welcome_image(self):
        """Thay đổi ảnh welcome"""
        file_path = filedialog.askopenfilename(
            title="Choose Welcome Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Copy image to welcome.png
                with open(file_path, "rb") as src:
                    with open("welcome.png", "wb") as dst:
                        dst.write(src.read())
                
                messagebox.showinfo("Success", "Welcome image updated! Please restart the app to see changes.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update image: {str(e)}")
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SpeakAndSpeakApp()
    app.run()