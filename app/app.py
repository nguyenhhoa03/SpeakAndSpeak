import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import platform
import os
import yaml
import pyttsx3
import webbrowser
from PIL import Image
import time
import pyaudio
import wave
import subprocess
import sys

from non_random_word import generate_word
from non_random_sentence import generate_sentence
from speech_to_text import transcribe_audio
from pronunciation_assessment import assess_pronunciation
from user_statistics import analyze_pronunciation_data

class SpeakAndSpeakApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Speak & Speak - English Pronunciation Practice")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        self.load_config()
        
        # TTS engine sẽ được tạo mới cho mỗi lần phát âm
        self.tts_engine = None
        
        # PyAudio configuration
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        
        self.current_word = ""
        self.current_sentence = ""
        self.is_recording = False
        self.progress_timer = None
        self.current_difficulty = self.config.get("sentence_difficulty", {}).get("current", "Easy")
        
        self.create_widgets()
        
    def load_config(self):
        try:
            with open("app-config.yaml", "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            
            ctk.set_appearance_mode(self.config["theme"]["current"])
            ctk.set_default_color_theme(self.config["color_scheme"]["current"])
            
            # Load sentence difficulty setting if exists
            if "sentence_difficulty" in self.config:
                self.current_difficulty = self.config["sentence_difficulty"]["current"]
            
        except FileNotFoundError:
            self.config = {
                "theme": {
                    "available": ["light", "dark", "system"],
                    "current": "system"
                },
                "color_scheme": {
                    "available": ["blue", "green", "dark-blue"],
                    "current": "dark-blue"
                },
                "speech_rate": {
                    "words_per_minute": 150,
                    "min_rate": 60,
                    "max_rate": 300
                }
            }
            self.save_config()
        
        # Ensure speech_rate exists in config
        if "speech_rate" not in self.config:
            self.config["speech_rate"] = {
                "words_per_minute": 150,
                "min_rate": 60,
                "max_rate": 300
            }
            self.save_config()
        
        # Ensure sentence_difficulty exists in config
        if "sentence_difficulty" not in self.config:
            self.config["sentence_difficulty"] = {
                "levels": ["Auto", "Easy", "Medium", "Hard"],
                "current": "Easy"
            }
            self.save_config()
    
    def save_config(self):
        with open("app-config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def calculate_recording_time(self, text, is_word=True):
        """Calculate recording time based on text and speech rate"""
        words_per_minute = self.config["speech_rate"]["words_per_minute"]
        
        if is_word:
            # For single word, use a base time with some buffer
            base_time = (60 / words_per_minute) * 1  # Time for 1 word
            recording_time = max(2, int(base_time + 1))  # Minimum 2 seconds with 1s buffer
        else:
            # For sentences, count words
            word_count = len(text.split())
            base_time = (60 / words_per_minute) * word_count
            recording_time = max(4, int(base_time + 2))  # Minimum 4 seconds with 2s buffer
        
        return recording_time
    
    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self.root, width=880, height=680)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.welcome_tab = self.tabview.add("Welcome")
        self.exercise_tab = self.tabview.add("Exercise")
        self.sentence_tab = self.tabview.add("Sentence")
        self.statistics_tab = self.tabview.add("Statistics")
        self.settings_tab = self.tabview.add("Settings")
        self.about_tab = self.tabview.add("About")
        
        self.setup_welcome_tab()
        self.setup_exercise_tab()
        self.setup_sentence_tab()
        self.setup_statistics_tab()
        self.setup_settings_tab()
        self.setup_about_tab()
    
    def setup_welcome_tab(self):
        main_frame = ctk.CTkFrame(self.welcome_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            welcome_img = Image.open("welcome.png")
            welcome_w, welcome_h = welcome_img.size
            new_welcome_w = 300
            new_welcome_h = int(welcome_h * (new_welcome_w / welcome_w))
            welcome_image = ctk.CTkImage(welcome_img, size=(new_welcome_w, new_welcome_h))
            
            image_label = ctk.CTkLabel(main_frame, image=welcome_image, text="")
            image_label.pack(pady=(50, 20))
        except FileNotFoundError:
            icon_label = ctk.CTkLabel(
                main_frame, 
                text="🪶",
                font=ctk.CTkFont(size=120),
                width=300,
                height=200
            )
            icon_label.pack(pady=(50, 20))
        
        welcome_label = ctk.CTkLabel(
            main_frame,
            text="Welcome back! Ready to start?",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_label.pack(pady=20)
        
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        exercise_button = ctk.CTkButton(
            button_frame,
            text="Exercise",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=150,
            height=50,
            command=lambda: self.tabview.set("Exercise")
        )
        exercise_button.pack(side="left", padx=20, pady=20)
        
        sentence_button = ctk.CTkButton(
            button_frame,
            text="Sentence",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=150,
            height=50,
            command=lambda: self.tabview.set("Sentence")
        )
        sentence_button.pack(side="left", padx=20, pady=20)
    
    def setup_exercise_tab(self):
        main_frame = ctk.CTkFrame(self.exercise_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon/Image
        try:
            exercise_img = Image.open("exercise.png")
            exercise_w, exercise_h = exercise_img.size
            new_exercise_w = 200
            new_exercise_h = int(exercise_h * (new_exercise_w / exercise_w))
            exercise_image = ctk.CTkImage(exercise_img, size=(new_exercise_w, new_exercise_h))
            
            image_label = ctk.CTkLabel(main_frame, image=exercise_image, text="")
            image_label.pack(pady=(50, 20))
        except FileNotFoundError:
            icon_label = ctk.CTkLabel(
                main_frame, 
                text="📝",
                font=ctk.CTkFont(size=100),
                width=200,
                height=150
            )
            icon_label.pack(pady=(50, 20))
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Pronunciation Discrimination Exercise",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Description
        description_text = (
            "Practice your pronunciation discrimination skills!\n\n"
            "In this exercise, you will:\n"
            "• Listen to pairs of words\n"
            "• Determine if they sound the same or different\n"
            "• Choose from multiple choice answers (A, B, C, D)\n"
            "• Get instant feedback on your answers\n\n"
            "This exercise helps improve your ability to distinguish\n"
            "between similar-sounding English words."
        )
        
        description_label = ctk.CTkLabel(
            main_frame,
            text=description_text,
            font=ctk.CTkFont(size=16),
            justify="left"
        )
        description_label.pack(pady=30)
        
        # Start Button
        start_button = ctk.CTkButton(
            main_frame,
            text="Start Exercise",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=200,
            height=60,
            command=self.start_discrimination_exercise
        )
        start_button.pack(pady=30)
        
        # Status Label
        self.exercise_status = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        self.exercise_status.pack(pady=10)
    
    def setup_sentence_tab(self):
        main_frame = ctk.CTkFrame(self.sentence_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Difficulty selection frame
        difficulty_frame = ctk.CTkFrame(main_frame)
        difficulty_frame.pack(fill="x", padx=20, pady=10)
        
        difficulty_label = ctk.CTkLabel(
            difficulty_frame,
            text="Difficulty Level:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        difficulty_label.pack(side="left", padx=10)
        
        self.difficulty_var = ctk.StringVar(value=self.current_difficulty)
        difficulty_menu = ctk.CTkOptionMenu(
            difficulty_frame,
            variable=self.difficulty_var,
            values=self.config["sentence_difficulty"]["levels"],
            command=self.change_difficulty_level,
            width=120
        )
        difficulty_menu.pack(side="left", padx=10)
        
        self.sentence_label = ctk.CTkLabel(
            main_frame,
            text="Click 'Random Sentence' to start!",
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=700
        )
        self.sentence_label.pack(pady=30)
        
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=20)
        
        random_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Random Sentence",
            command=self.generate_random_sentence,
            width=140,
            height=35
        )
        random_sentence_btn.pack(side="left", padx=10, pady=10)
        
        listen_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Listen",
            command=self.speak_sentence,
            width=100,
            height=35
        )
        listen_sentence_btn.pack(side="left", padx=10, pady=10)
        
        self.record_sentence_btn = ctk.CTkButton(
            control_frame,
            text="Record",
            command=self.start_sentence_recording,
            width=120,
            height=35
        )
        self.record_sentence_btn.pack(side="left", padx=10, pady=10)
        
        self.sentence_progress = ctk.CTkProgressBar(main_frame, width=600)
        self.sentence_progress.pack(pady=10)
        self.sentence_progress.set(0)
        
        self.sentence_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.sentence_status.pack(pady=10)
        
        self.sentence_result_text = ctk.CTkTextbox(
            main_frame,
            wrap="word",
            width=750,
            height=300
        )
        self.sentence_result_text.pack(fill="both", expand=True, pady=20)

    def setup_statistics_tab(self):
        main_frame = ctk.CTkFrame(self.statistics_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        load_stats_btn = ctk.CTkButton(
            main_frame,
            text="Load Statistics",
            command=self.load_statistics,
            width=150,
            height=40
        )
        load_stats_btn.pack(pady=20)
        
        self.stats_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=14))
        self.stats_status.pack(pady=10)
        
        self.stats_result_text = ctk.CTkTextbox(
            main_frame,
            wrap="word",
            width=750,
            height=500
        )
        self.stats_result_text.pack(fill="both", expand=True, pady=20)
    
    def setup_settings_tab(self):
        main_frame = ctk.CTkFrame(self.settings_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
        
        # Speech Rate Setting
        speech_frame = ctk.CTkFrame(main_frame)
        speech_frame.pack(fill="x", padx=20, pady=10)
        
        speech_label = ctk.CTkLabel(speech_frame, text="Speech Rate (words/minute):", font=ctk.CTkFont(size=16, weight="bold"))
        speech_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        speech_info = ctk.CTkLabel(
            speech_frame, 
            text=f"Range: {self.config['speech_rate']['min_rate']}-{self.config['speech_rate']['max_rate']} words/minute",
            font=ctk.CTkFont(size=12)
        )
        speech_info.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.speech_rate_var = ctk.StringVar(value=str(self.config["speech_rate"]["words_per_minute"]))
        speech_entry = ctk.CTkEntry(
            speech_frame,
            textvariable=self.speech_rate_var,
            width=100,
            placeholder_text="150"
        )
        speech_entry.pack(anchor="w", padx=20, pady=(0, 10))
        
        apply_speech_btn = ctk.CTkButton(
            speech_frame,
            text="Apply Speech Rate",
            command=self.change_speech_rate,
            width=150,
            height=30
        )
        apply_speech_btn.pack(anchor="w", padx=20, pady=(0, 20))
        
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
        main_frame = ctk.CTkFrame(self.about_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            about_img = Image.open("about.png")
            about_w, about_h = about_img.size
            new_about_w = 300
            new_about_h = int(about_h * (new_about_w / about_w))
            about_image = ctk.CTkImage(about_img, size=(new_about_w, new_about_h))
            image_label = ctk.CTkLabel(main_frame, image=about_image, text="")
            image_label.pack(pady=(50, 20))
        except FileNotFoundError:
            placeholder_label = ctk.CTkLabel(
                main_frame, 
                text="About Image\n(about.png not found)",
                font=ctk.CTkFont(size=20),
                width=300,
                height=200
            )
            placeholder_label.pack(pady=(50, 20))
        
        app_name = ctk.CTkLabel(
            main_frame,
            text="Speak & Speak",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        app_name.pack(pady=20)
        
        version_label = ctk.CTkLabel(
            main_frame,
            text="version 1.1",
            font=ctk.CTkFont(size=16)
        )
        version_label.pack(pady=10)
        
        github_link = ctk.CTkLabel(
            main_frame,
            text="https://github.com/nguyenhhoa03/SpeakAndSpeak",
            font=ctk.CTkFont(size=14, underline=True),
            text_color=("blue", "lightblue"),
            cursor="hand2"
        )
        github_link.pack(pady=20)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/nguyenhhoa03/SpeakAndSpeak"))
    
    def start_discrimination_exercise(self):
            """Launch the discrimination.exe (priority) or discrimination.py script"""
            try:
                self.exercise_status.configure(text="Starting exercise...")
                
                # Check if discrimination.exe exists first (priority)
                exe_path = "discrimination.exe"
                py_path = "discrimination.py"
                
                if os.path.exists(exe_path):
                    # Run discrimination.exe in a separate process
                    if platform.system() == "Windows":
                        subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen([exe_path])
                    
                    self.exercise_status.configure(text="Exercise started successfully! (EXE)")
                
                elif os.path.exists(py_path):
                    # Fallback: Run discrimination.py in a separate process
                    if platform.system() == "Windows":
                        subprocess.Popen([sys.executable, py_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen([sys.executable, py_path])
                    
                    self.exercise_status.configure(text="Exercise started successfully! (Python)")
                
                else:
                    # Neither file exists
                    messagebox.showerror("Error", "Neither discrimination.exe nor discrimination.py found!")
                    self.exercise_status.configure(text="Error: File not found")
                    return
                
                # Clear status after 3 seconds
                self.root.after(3000, lambda: self.exercise_status.configure(text=""))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start exercise: {str(e)}")
                self.exercise_status.configure(text=f"Error: {str(e)}")
    
    def start_fake_progress(self, progress_bar, interval=1.0):
        if self.progress_timer:
            self.progress_timer.cancel()
        
        current_progress = 0.0
        remaining = 1.0
        
        def update_progress():
            nonlocal current_progress, remaining
            if remaining > 0.01:
                increment = remaining * 0.3
                current_progress += increment
                remaining -= increment
                progress_bar.set(current_progress)
                
                self.progress_timer = threading.Timer(interval, update_progress)
                self.progress_timer.start()
        
        update_progress()
    
    def complete_progress(self, progress_bar):
        if self.progress_timer:
            self.progress_timer.cancel()
            self.progress_timer = None
        progress_bar.set(1.0)
        threading.Timer(0.5, lambda: progress_bar.set(0)).start()
    
    def change_difficulty_level(self, level):
        """Thay đổi và lưu độ khó câu"""
        self.current_difficulty = level
        self.config["sentence_difficulty"]["current"] = level
        self.save_config()
    
    def generate_random_sentence(self):
        try:
            self.sentence_status.configure(text="Generating sentence...")
            self.start_fake_progress(self.sentence_progress, interval=2.0)
            
            def generate_sentence_thread():
                try:
                    # Convert difficulty level to lv parameter (Auto=0, Easy=1, Medium=2, Hard=3)
                    difficulty_map = {"Auto": 0, "Easy": 1, "Medium": 2, "Hard": 3}
                    lv = difficulty_map.get(self.current_difficulty, 1)
                    
                    sentence = generate_sentence("user-data.yaml", "eng_sentences.tsv", lv)
                    self.root.after(0, lambda: self._update_sentence_generated(sentence))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate sentence: {str(e)}"))
                finally:
                    self.root.after(0, lambda: self.complete_progress(self.sentence_progress))
                    self.root.after(0, lambda: self.sentence_status.configure(text=""))
            
            threading.Thread(target=generate_sentence_thread).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate sentence: {str(e)}")
    
    def _update_sentence_generated(self, sentence):
        self.current_sentence = sentence
        self.sentence_label.configure(text=self.current_sentence)
        self.sentence_result_text.delete("1.0", "end")
        # Update button text with recording time
        recording_time = self.calculate_recording_time(sentence, is_word=False)
        self.record_sentence_btn.configure(text=f"Record ({recording_time}s)")
    
    def _create_fresh_tts_engine(self):
        """Tạo TTS engine mới cho mỗi lần sử dụng"""
        try:
            if self.tts_engine:
                try:
                    self.tts_engine.stop()
                except:
                    pass
                del self.tts_engine
            
            engine = pyttsx3.init()
            
            # Cấu hình engine với settings ổn định
            voices = engine.getProperty('voices')
            if voices and len(voices) > 0:
                # Chọn voice tiếng Anh nếu có
                english_voice = None
                for voice in voices:
                    if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                        english_voice = voice
                        break
                
                if english_voice:
                    engine.setProperty('voice', english_voice.id)
                else:
                    engine.setProperty('voice', voices[0].id)
            
            engine.setProperty('rate', 150)    # Tốc độ vừa phải
            engine.setProperty('volume', 0.9)  # Âm lượng cao
            
            return engine
        except Exception as e:
            print(f"TTS Engine creation error: {e}")
            return None
    
    def speak_sentence(self):
        if self.current_sentence:
            self.sentence_status.configure(text="Speaking...")
            self.start_fake_progress(self.sentence_progress, interval=2.0)
            
            def speak_thread():
                try:
                    self._speak_text(self.current_sentence)
                except Exception as e:
                    print(f"TTS Error: {e}")
                    self.root.after(0, lambda: self.sentence_status.configure(text=f"TTS Error: {e}"))
                finally:
                    self.root.after(0, lambda: self.complete_progress(self.sentence_progress))
                    self.root.after(0, lambda: self.sentence_status.configure(text=""))
            
            threading.Thread(target=speak_thread, daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please generate a sentence first!")
    
    def _speak_text(self, text):
        """Sử dụng engine mới cho mỗi lần phát âm"""
        engine = self._create_fresh_tts_engine()
        if engine:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"TTS playback error: {e}")
                raise e
            finally:
                try:
                    engine.stop()
                except:
                    pass
                del engine
        else:
            raise Exception("Could not initialize TTS engine")
    
    def start_sentence_recording(self):
        if not self.current_sentence:
            messagebox.showwarning("Warning", "Please generate a sentence first!")
            return
        
        recording_time = self.calculate_recording_time(self.current_sentence, is_word=False)
        self.start_recording(recording_time, self.process_sentence_recording)
    
    def start_recording(self, duration, callback):
        if self.is_recording:
            return
        
        self.is_recording = True
        threading.Thread(target=self._record_audio_pyaudio, args=(duration, callback), daemon=True).start()
    
    def _record_audio_pyaudio(self, duration, callback):
        """Record audio using PyAudio"""
        try:
            progress_bar = self.sentence_progress
            status_label = self.sentence_status
            
            self.root.after(0, lambda: status_label.configure(text=f"Recording for {duration} seconds..."))
            
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            
            # Open stream
            stream = audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            total_frames = int(self.rate / self.chunk * duration)
            
            # Record for the specified duration
            for i in range(total_frames):
                data = stream.read(self.chunk)
                frames.append(data)
                
                # Update progress bar
                progress = (i + 1) / total_frames
                self.root.after(0, lambda p=progress: progress_bar.set(p))
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Save the recorded data as a WAV file
            with wave.open("audio.wav", 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.audio_format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            
            self.root.after(0, lambda: status_label.configure(text="Recording completed!"))
            self.root.after(0, lambda: progress_bar.set(0))
            
            # Process the recorded audio
            callback()
            
        except Exception as e:
            error_msg = f"Recording error: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: status_label.configure(text=error_msg))
        finally:
            self.is_recording = False
    
    def process_sentence_recording(self):
        self.sentence_status.configure(text="Processing...")
        self.start_fake_progress(self.sentence_progress, interval=2.0)
        threading.Thread(target=self._process_sentence_audio, daemon=True).start()
    
    def _process_sentence_audio(self):
        try:
            transcribed_text = transcribe_audio("audio.wav")
            result = assess_pronunciation(self.current_sentence, transcribed_text)
            
            self.root.after(0, lambda: self._update_sentence_result(result))
            self.root.after(0, lambda: self.complete_progress(self.sentence_progress))
            self.root.after(0, lambda: self.sentence_status.configure(text="Processing completed!"))
            
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda: self.complete_progress(self.sentence_progress))
            self.root.after(0, lambda msg=error_msg: self.sentence_status.configure(text=msg))
    
    def _update_sentence_result(self, result):
        self.sentence_result_text.delete("1.0", "end")
        self.sentence_result_text.insert("1.0", result)
    
    def load_statistics(self):
        self.stats_status.configure(text="Processing...")
        threading.Thread(target=self._load_stats, daemon=True).start()
    
    def _load_stats(self):
        try:
            result = analyze_pronunciation_data("user-data.yaml")
            self.root.after(0, lambda: self._update_stats_result(result))
            self.root.after(0, lambda: self.stats_status.configure(text="Statistics loaded!"))
        except Exception as e:
            error_msg = f"Error: {e}"
            self.root.after(0, lambda msg=error_msg: self.stats_status.configure(text=msg))
    
    def _update_stats_result(self, result):
        self.stats_result_text.delete("1.0", "end")
        self.stats_result_text.insert("1.0", result)
    
    def change_theme(self, theme):
        self.config["theme"]["current"] = theme
        self.save_config()
        ctk.set_appearance_mode(theme)
    
    def change_color_scheme(self, color_scheme):
        self.config["color_scheme"]["current"] = color_scheme
        self.save_config()
        messagebox.showinfo("Info", "Please restart the app to apply color scheme changes.")
    
    def change_speech_rate(self):
        try:
            new_rate = int(self.speech_rate_var.get())
            min_rate = self.config["speech_rate"]["min_rate"]
            max_rate = self.config["speech_rate"]["max_rate"]
            
            if min_rate <= new_rate <= max_rate:
                self.config["speech_rate"]["words_per_minute"] = new_rate
                self.save_config()
                messagebox.showinfo("Success", f"Speech rate updated to {new_rate} words/minute!")
                
                # Update button texts if sentences are already generated
                if self.current_sentence:
                    recording_time = self.calculate_recording_time(self.current_sentence, is_word=False)
                    self.record_sentence_btn.configure(text=f"Record ({recording_time}s)")
            else:
                messagebox.showerror("Error", f"Speech rate must be between {min_rate} and {max_rate} words/minute!")
                self.speech_rate_var.set(str(self.config["speech_rate"]["words_per_minute"]))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            self.speech_rate_var.set(str(self.config["speech_rate"]["words_per_minute"]))
    
    def change_welcome_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose Welcome Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                with open(file_path, "rb") as src:
                    with open("welcome.png", "wb") as dst:
                        dst.write(src.read())
                
                messagebox.showinfo("Success", "Welcome image updated! Please restart the app to see changes.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update image: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpeakAndSpeakApp()
    app.run()
