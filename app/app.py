import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import yaml
import os
import threading
import queue
import json
import vosk
import pyaudio
import pyttsx3
import webbrowser
from typing import Dict, Any, Optional

# Import các module tùy chỉnh (cần được tạo riêng)
try:
    from non_random_word import generate_word
    from non_random_sentence import generate_sentence
    from pronunciation_assessment import assess_pronunciation
    from user_statistics import analyze_pronunciation_data
except ImportError:
    # Fallback functions nếu các module không tồn tại
    def generate_word(file_path):
        import random
        words = ["hello", "world", "python", "programming", "computer", "language", "education", "practice", "learning", "development"]
        return random.choice(words)
    
    def generate_sentence(file_path):
        import random
        sentences = [
            "Hello, how are you today?",
            "I love programming in Python.",
            "This is a great learning experience.",
            "Practice makes perfect in pronunciation.",
            "Technology helps us learn better."
        ]
        return random.choice(sentences)
    
    def assess_pronunciation(original, recognized):
        # Mock assessment function
        import random
        accuracy = random.randint(60, 95)
        return {
            "overall_score": accuracy,
            "pronunciation_score": accuracy + random.randint(-5, 5),
            "accuracy_score": accuracy + random.randint(-3, 3),
            "fluency_score": accuracy + random.randint(-7, 7),
            "completeness_score": accuracy + random.randint(-2, 2),
            "details": f"Original: {original}\nRecognized: {recognized}\nAccuracy: {accuracy}%"
        }
    
    def analyze_pronunciation_data(file_path):
        # Mock statistics function
        return {
            "total_attempts": 45,
            "average_score": 78.5,
            "improvement_rate": "+12.3%",
            "common_mistakes": ["th sounds", "r sounds", "vowel length"],
            "best_categories": ["consonants", "short vowels"],
            "practice_time": "2h 30m this week"
        }

class ConfigManager:
    def __init__(self, config_file="app-config.yaml"):
        self.config_file = config_file
        self.default_config = {
            "theme": {
                "available": ["light", "dark", "system"],
                "current": "system"
            },
            "color_scheme": {
                "available": ["blue", "green", "dark-blue"],
                "current": "dark-blue"
            }
        }
        self.config = self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or self.default_config
        except Exception as e:
            print(f"Error loading config: {e}")
        return self.default_config.copy()

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default

    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.setup_vosk()
        
    def setup_vosk(self):
        try:
            # Kiểm tra xem model có tồn tại không
            model_path = "vosk-model-en-us-0.22"
            if not os.path.exists(model_path):
                print(f"Vosk model not found at {model_path}")
                self.model = None
                self.rec = None
                return
                
            self.model = vosk.Model(model_path)
            self.rec = vosk.KaldiRecognizer(self.model, 16000)
        except Exception as e:
            print(f"Error setting up Vosk: {e}")
            self.model = None
            self.rec = None

    def start_recording(self, callback):
        if self.model is None:
            callback("Error: Vosk model not available")
            return
            
        self.is_recording = True
        self.callback = callback
        threading.Thread(target=self._record_audio, daemon=True).start()

    def stop_recording(self):
        self.is_recording = False

    def _record_audio(self):
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True,
                          frames_per_buffer=1024)
            
            frames = []
            while self.is_recording:
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
                
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get('text', '')
                    if text:
                        self.callback(text)
                        
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Process final result
            final_result = json.loads(self.rec.FinalResult())
            final_text = final_result.get('text', '')
            if final_text:
                self.callback(final_text)
                
        except Exception as e:
            self.callback(f"Recording error: {str(e)}")

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speech rate
        
    def speak(self, text):
        try:
            threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def _speak_thread(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Thread Error: {e}")

class SpeakAndSpeakApp:
    def __init__(self):
        # Initialize components
        self.config_manager = ConfigManager()
        self.audio_recorder = AudioRecorder()
        self.tts_engine = TTSEngine()
        self.current_word = ""
        self.current_sentence = ""
        self.is_recording = False
        
        # Apply theme and color scheme
        self.apply_theme()
        
        # Create main window
        self.window = ctk.CTk()
        self.window.title("Speak & Speak")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Focus window for key bindings
        self.window.focus_set()
        
        # Create main tabview
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_welcome_tab()
        self.create_word_tab()
        self.create_sentence_tab()
        self.create_statistics_tab()
        self.create_settings_tab()
        self.create_about_tab()
        
        # Set default tab
        self.tabview.set("Welcome")
        
        # Bind space key for recording
        self.setup_key_bindings()

    def apply_theme(self):
        theme = self.config_manager.get("theme.current", "system")
        color = self.config_manager.get("color_scheme.current", "dark-blue")
        
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(color)

    def setup_key_bindings(self):
        # Bind space key press and release events to the main window
        self.window.bind('<KeyPress-space>', self.on_space_press)
        self.window.bind('<KeyRelease-space>', self.on_space_release)
        
        # Make sure the window can receive key events
        self.window.focus_set()
        
        # Also bind to the tabview to ensure focus
        self.tabview.bind('<KeyPress-space>', self.on_space_press)
        self.tabview.bind('<KeyRelease-space>', self.on_space_release)

    def on_space_press(self, event):
        # Prevent multiple recording instances
        if self.is_recording:
            return
        
        # Only record if we're on Word or Sentence tab
        current_tab = self.tabview.get()
        if current_tab in ["Word", "Sentence"]:
            self.start_recording(current_tab)

    def on_space_release(self, event):
        if self.is_recording:
            self.stop_recording()

    def create_welcome_tab(self):
        welcome_tab = self.tabview.add("Welcome")
        
        # Main frame
        main_frame = ctk.CTkFrame(welcome_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome image
        try:
            if os.path.exists("welcome.png"):
                image = Image.open("welcome.png")
                image = image.resize((200, 200))
                photo = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
                image_label = ctk.CTkLabel(main_frame, image=photo, text="")
                image_label.pack(pady=20)
        except Exception as e:
            # Fallback text if image not found
            placeholder = ctk.CTkLabel(main_frame, text="🎤 Speak & Speak", font=("Arial", 24))
            placeholder.pack(pady=20)
        
        # Welcome text
        welcome_text = ctk.CTkLabel(main_frame, text="Welcome back! Ready to start?", font=("Arial", 18))
        welcome_text.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(pady=20)
        
        # Word button
        word_btn = ctk.CTkButton(buttons_frame, text="Word", width=120, height=40,
                                command=lambda: self.tabview.set("Word"))
        word_btn.pack(side="left", padx=10)
        
        # Sentence button
        sentence_btn = ctk.CTkButton(buttons_frame, text="Sentence", width=120, height=40,
                                    command=lambda: self.tabview.set("Sentence"))
        sentence_btn.pack(side="left", padx=10)

    def create_word_tab(self):
        word_tab = self.tabview.add("Word")
        
        # Main frame
        main_frame = ctk.CTkFrame(word_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Word display
        self.word_label = ctk.CTkLabel(main_frame, text="Click 'New Word' to start", 
                                      font=("Arial", 32, "bold"))
        self.word_label.pack(pady=20)
        
        # Control buttons
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=10)
        
        new_word_btn = ctk.CTkButton(control_frame, text="New Word", 
                                    command=self.generate_new_word)
        new_word_btn.pack(side="left", padx=5)
        
        random_word_btn = ctk.CTkButton(control_frame, text="Random Again", 
                                       command=self.generate_new_word)
        random_word_btn.pack(side="left", padx=5)
        
        listen_btn = ctk.CTkButton(control_frame, text="Listen", 
                                  command=lambda: self.tts_engine.speak(self.current_word))
        listen_btn.pack(side="left", padx=5)
        
        # Instructions
        instruction_label = ctk.CTkLabel(main_frame, text="Hold SPACE to record your pronunciation")
        instruction_label.pack(pady=5)
        
        # Status label
        self.word_status_label = ctk.CTkLabel(main_frame, text="")
        self.word_status_label.pack(pady=5)
        
        # Results frame with scrollbar
        self.word_results_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        self.word_results_frame.pack(fill="both", expand=True, pady=10)

    def create_sentence_tab(self):
        sentence_tab = self.tabview.add("Sentence")
        
        # Main frame
        main_frame = ctk.CTkFrame(sentence_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sentence display
        self.sentence_label = ctk.CTkLabel(main_frame, text="Click 'New Sentence' to start", 
                                          font=("Arial", 18, "bold"), wraplength=600)
        self.sentence_label.pack(pady=20)
        
        # Control buttons
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=10)
        
        new_sentence_btn = ctk.CTkButton(control_frame, text="New Sentence", 
                                        command=self.generate_new_sentence)
        new_sentence_btn.pack(side="left", padx=5)
        
        random_sentence_btn = ctk.CTkButton(control_frame, text="Random Again", 
                                           command=self.generate_new_sentence)
        random_sentence_btn.pack(side="left", padx=5)
        
        listen_btn = ctk.CTkButton(control_frame, text="Listen", 
                                  command=lambda: self.tts_engine.speak(self.current_sentence))
        listen_btn.pack(side="left", padx=5)
        
        # Instructions
        instruction_label = ctk.CTkLabel(main_frame, text="Hold SPACE to record your pronunciation")
        instruction_label.pack(pady=5)
        
        # Status label
        self.sentence_status_label = ctk.CTkLabel(main_frame, text="")
        self.sentence_status_label.pack(pady=5)
        
        # Results frame with scrollbar
        self.sentence_results_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        self.sentence_results_frame.pack(fill="both", expand=True, pady=10)

    def create_statistics_tab(self):
        statistics_tab = self.tabview.add("Statistics")
        
        # Main frame
        main_frame = ctk.CTkFrame(statistics_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Your Progress Statistics", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(main_frame, text="Refresh Statistics", 
                                   command=self.load_statistics)
        refresh_btn.pack(pady=5)
        
        # Status label
        self.stats_status_label = ctk.CTkLabel(main_frame, text="")
        self.stats_status_label.pack(pady=5)
        
        # Statistics results frame
        self.stats_results_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        self.stats_results_frame.pack(fill="both", expand=True, pady=10)
        
        # Load initial statistics
        self.load_statistics()

    def create_settings_tab(self):
        settings_tab = self.tabview.add("Settings")
        
        # Main frame
        main_frame = ctk.CTkFrame(settings_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Settings", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Theme settings
        theme_frame = ctk.CTkFrame(main_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:")
        theme_label.pack(side="left", padx=10)
        
        self.theme_var = ctk.StringVar(value=self.config_manager.get("theme.current"))
        theme_menu = ctk.CTkOptionMenu(theme_frame, variable=self.theme_var,
                                      values=self.config_manager.get("theme.available"),
                                      command=self.change_theme)
        theme_menu.pack(side="right", padx=10)
        
        # Color scheme settings
        color_frame = ctk.CTkFrame(main_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        color_label = ctk.CTkLabel(color_frame, text="Color Scheme:")
        color_label.pack(side="left", padx=10)
        
        self.color_var = ctk.StringVar(value=self.config_manager.get("color_scheme.current"))
        color_menu = ctk.CTkOptionMenu(color_frame, variable=self.color_var,
                                      values=self.config_manager.get("color_scheme.available"),
                                      command=self.change_color)
        color_menu.pack(side="right", padx=10)
        
        # Welcome image settings
        image_frame = ctk.CTkFrame(main_frame)
        image_frame.pack(fill="x", padx=10, pady=10)
        
        image_label = ctk.CTkLabel(image_frame, text="Welcome Image:")
        image_label.pack(side="left", padx=10)
        
        change_image_btn = ctk.CTkButton(image_frame, text="Change Image", 
                                        command=self.change_welcome_image)
        change_image_btn.pack(side="right", padx=10)

    def create_about_tab(self):
        about_tab = self.tabview.add("About")
        
        # Main frame
        main_frame = ctk.CTkFrame(about_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # About image
        try:
            if os.path.exists("about.png"):
                image = Image.open("about.png")
                image = image.resize((150, 150))
                photo = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))
                image_label = ctk.CTkLabel(main_frame, image=photo, text="")
                image_label.pack(pady=20)
        except Exception as e:
            # Fallback text if image not found
            placeholder = ctk.CTkLabel(main_frame, text="📱 About", font=("Arial", 24))
            placeholder.pack(pady=20)
        
        # App info
        app_name = ctk.CTkLabel(main_frame, text="Speak & Speak", font=("Arial", 24, "bold"))
        app_name.pack(pady=5)
        
        version_label = ctk.CTkLabel(main_frame, text="version 1.0", font=("Arial", 14))
        version_label.pack(pady=2)
        
        # GitHub link
        def open_github():
            webbrowser.open("https://github.com/nguyenhhoa03/SpeakAndSpeak")
        
        github_btn = ctk.CTkButton(main_frame, text="Visit GitHub Repository", 
                                  command=open_github)
        github_btn.pack(pady=10)

    def generate_new_word(self):
        try:
            self.current_word = generate_word("user-data.yaml")
            self.word_label.configure(text=self.current_word)
            # Clear previous results
            for widget in self.word_results_frame.winfo_children():
                widget.destroy()
        except Exception as e:
            self.word_label.configure(text=f"Error: {str(e)}")

    def generate_new_sentence(self):
        try:
            self.current_sentence = generate_sentence("user-data.yaml")
            self.sentence_label.configure(text=self.current_sentence)
            # Clear previous results
            for widget in self.sentence_results_frame.winfo_children():
                widget.destroy()
        except Exception as e:
            self.sentence_label.configure(text=f"Error: {str(e)}")

    def start_recording(self, tab_type):
        if self.is_recording:
            return
            
        self.is_recording = True
        
        if tab_type == "Word":
            if not self.current_word:
                self.is_recording = False
                return
            self.word_status_label.configure(text="🔴 Recording... (Release SPACE to stop)")
            self.audio_recorder.start_recording(lambda result: self.process_word_result(result))
        elif tab_type == "Sentence":
            if not self.current_sentence:
                self.is_recording = False
                return
            self.sentence_status_label.configure(text="🔴 Recording... (Release SPACE to stop)")
            self.audio_recorder.start_recording(lambda result: self.process_sentence_result(result))

    def stop_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.audio_recorder.stop_recording()
        
        current_tab = self.tabview.get()
        if current_tab == "Word":
            self.word_status_label.configure(text="⏳ Đang xử lý...")
        elif current_tab == "Sentence":
            self.sentence_status_label.configure(text="⏳ Đang xử lý...")

    def process_word_result(self, recognized_text):
        def process():
            try:
                if "error" in recognized_text.lower():
                    result = {"error": recognized_text}
                else:
                    result = assess_pronunciation(self.current_word, recognized_text)
                
                self.window.after(0, lambda: self.display_word_result(result, recognized_text))
            except Exception as e:
                self.window.after(0, lambda: self.display_word_result({"error": str(e)}, recognized_text))
            finally:
                # Reset recording state
                self.is_recording = False
        
        threading.Thread(target=process, daemon=True).start()

    def process_sentence_result(self, recognized_text):
        def process():
            try:
                if "error" in recognized_text.lower():
                    result = {"error": recognized_text}
                else:
                    result = assess_pronunciation(self.current_sentence, recognized_text)
                
                self.window.after(0, lambda: self.display_sentence_result(result, recognized_text))
            except Exception as e:
                self.window.after(0, lambda: self.display_sentence_result({"error": str(e)}, recognized_text))
            finally:
                # Reset recording state
                self.is_recording = False
        
        threading.Thread(target=process, daemon=True).start()

    def display_word_result(self, result, recognized_text):
        self.word_status_label.configure(text="")
        
        # Clear previous results
        for widget in self.word_results_frame.winfo_children():
            widget.destroy()
        
        # Display results
        if "error" in result:
            error_label = ctk.CTkLabel(self.word_results_frame, text=f"Error: {result['error']}", 
                                      text_color="red")
            error_label.pack(pady=5)
        else:
            # Display assessment results
            results_text = f"Original: {self.current_word}\n"
            results_text += f"Recognized: {recognized_text}\n\n"
            
            for key, value in result.items():
                if key != "details":
                    results_text += f"{key.replace('_', ' ').title()}: {value}\n"
            
            if "details" in result:
                results_text += f"\nDetails:\n{result['details']}"
            
            result_label = ctk.CTkLabel(self.word_results_frame, text=results_text, 
                                       justify="left", wraplength=500)
            result_label.pack(pady=10, padx=10)

    def display_sentence_result(self, result, recognized_text):
        self.sentence_status_label.configure(text="")
        
        # Clear previous results
        for widget in self.sentence_results_frame.winfo_children():
            widget.destroy()
        
        # Display results
        if "error" in result:
            error_label = ctk.CTkLabel(self.sentence_results_frame, text=f"Error: {result['error']}", 
                                      text_color="red")
            error_label.pack(pady=5)
        else:
            # Display assessment results
            results_text = f"Original: {self.current_sentence}\n"
            results_text += f"Recognized: {recognized_text}\n\n"
            
            for key, value in result.items():
                if key != "details":
                    results_text += f"{key.replace('_', ' ').title()}: {value}\n"
            
            if "details" in result:
                results_text += f"\nDetails:\n{result['details']}"
            
            result_label = ctk.CTkLabel(self.sentence_results_frame, text=results_text, 
                                       justify="left", wraplength=500)
            result_label.pack(pady=10, padx=10)

    def load_statistics(self):
        def load():
            try:
                self.window.after(0, lambda: self.stats_status_label.configure(text="⏳ Đang xử lý..."))
                result = analyze_pronunciation_data("user-data.yaml")
                self.window.after(0, lambda: self.display_statistics(result))
            except Exception as e:
                self.window.after(0, lambda: self.display_statistics({"error": str(e)}))
        
        threading.Thread(target=load, daemon=True).start()

    def display_statistics(self, result):
        self.stats_status_label.configure(text="")
        
        # Clear previous results
        for widget in self.stats_results_frame.winfo_children():
            widget.destroy()
        
        if "error" in result:
            error_label = ctk.CTkLabel(self.stats_results_frame, text=f"Error: {result['error']}", 
                                      text_color="red")
            error_label.pack(pady=5)
        else:
            # Display statistics
            for key, value in result.items():
                if isinstance(value, list):
                    value_text = ", ".join(map(str, value))
                else:
                    value_text = str(value)
                
                stat_text = f"{key.replace('_', ' ').title()}: {value_text}"
                stat_label = ctk.CTkLabel(self.stats_results_frame, text=stat_text, 
                                         font=("Arial", 12), justify="left")
                stat_label.pack(pady=2, padx=10, anchor="w")

    def change_theme(self, theme):
        self.config_manager.set("theme.current", theme)
        self.config_manager.save_config()
        ctk.set_appearance_mode(theme)

    def change_color(self, color):
        self.config_manager.set("color_scheme.current", color)
        self.config_manager.save_config()
        messagebox.showinfo("Color Changed", "Color scheme will be applied on next restart.")

    def change_welcome_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Welcome Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Copy the selected image to welcome.png
                image = Image.open(file_path)
                image.save("welcome.png", "PNG")
                messagebox.showinfo("Success", "Welcome image updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update image: {str(e)}")

    def run(self):
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Application error: {e}")

def main():
    app = SpeakAndSpeakApp()
    app.run()

if __name__ == "__main__":
    main()