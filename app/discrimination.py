import customtkinter as ctk
import yaml
import random
import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import pronouncing
import pyttsx3
from wonderwords import RandomWord
import threading
import re
from collections import defaultdict
import os

class PhoneticDiscriminationApp:
    def __init__(self):
        # Initialize the app
        self.root = ctk.CTk()
        self.root.title("Phonetic Discrimination Exercise")
        self.root.geometry("800x600")
        
        # Initialize text-to-speech
        self.tts = pyttsx3.init()
        
        # Initialize word generator
        self.word_generator = RandomWord()
        
        # Data storage
        self.arpabet_ipa_map = {}
        self.ipa_confusion_groups = []
        self.exercise_history = {"phonetic": [], "stress": []}
        self.current_mode = "both"
        self.current_question = None
        self.current_answer = None
        self.questions_answered = 0
        self.correct_answers = 0
        
        # Session tracking for real-time updates
        self.session_total = 0
        self.session_correct = 0
        
        # Load configuration and data
        self.load_config()
        self.load_data()
        
        # Apply theme
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme(self.color_scheme)
        
        # Setup UI
        self.setup_main_menu()
        
    def load_config(self):
        """Load application configuration"""
        try:
            with open('app-config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.color_scheme = config.get('color_scheme', {}).get('current', 'blue')
                self.theme = config.get('theme', {}).get('current', 'dark')
                self.speech_rate = config.get('speech_rate', {}).get('words_per_minute', 150)
        except FileNotFoundError:
            self.color_scheme = 'blue'
            self.theme = 'dark'
            self.speech_rate = 150
            
    def load_data(self):
        """Load ARPAbet-IPA mapping and confusion groups"""
        # Load ARPAbet to IPA mapping
        try:
            with open('arpabet_ipa_database.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.arpabet_ipa_map[row['ARPAbet']] = row['IPA']
        except FileNotFoundError:
            print("Warning: arpabet_ipa_database.csv not found")
            
        # Load IPA confusion groups
        try:
            with open('ipa_confusion_groups.yaml', 'r', encoding='utf-8') as f:
                self.ipa_confusion_groups = yaml.safe_load(f)
        except FileNotFoundError:
            print("Warning: ipa_confusion_groups.yaml not found")
            
        # Load exercise history
        try:
            with open('discrimination.yaml', 'r', encoding='utf-8') as f:
                self.exercise_history = yaml.safe_load(f) or {"phonetic": [], "stress": []}
        except FileNotFoundError:
            self.exercise_history = {"phonetic": [], "stress": []}
            
    def save_exercise_history(self):
        """Save exercise history to YAML file"""
        # Keep only last 20 exercises for each type
        for exercise_type in ['phonetic', 'stress']:
            if len(self.exercise_history[exercise_type]) > 20:
                self.exercise_history[exercise_type] = self.exercise_history[exercise_type][-20:]
                
        with open('discrimination.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.exercise_history, f, default_flow_style=False, allow_unicode=True)
            
    def setup_main_menu(self):
        """Setup the main menu interface"""
        self.clear_window()
        
        # Title
        title = ctk.CTkLabel(self.root, text="Phonetic Discrimination Exercise", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=30)
        
        # Mode selection frame
        mode_frame = ctk.CTkFrame(self.root)
        mode_frame.pack(pady=20, padx=50, fill="x")
        
        mode_label = ctk.CTkLabel(mode_frame, text="Select Exercise Mode:", 
                                font=ctk.CTkFont(size=16))
        mode_label.pack(pady=10)
        
        # Mode selection
        self.mode_var = ctk.StringVar(value="both")
        
        phonetic_radio = ctk.CTkRadioButton(mode_frame, text="Phonetic Discrimination (Underlined Part)", 
                                          variable=self.mode_var, value="phonetic")
        phonetic_radio.pack(pady=5)
        
        stress_radio = ctk.CTkRadioButton(mode_frame, text="Stress Pattern Recognition", 
                                        variable=self.mode_var, value="stress")
        stress_radio.pack(pady=5)
        
        both_radio = ctk.CTkRadioButton(mode_frame, text="Both Exercises (Default)", 
                                      variable=self.mode_var, value="both")
        both_radio.pack(pady=5)
        
        # Start button
        start_button = ctk.CTkButton(self.root, text="Start Exercise", 
                                   command=self.start_exercise, font=ctk.CTkFont(size=16))
        start_button.pack(pady=30)
        
        # Statistics
        self.show_statistics()
        
    def show_statistics(self):
        """Display current statistics"""
        stats_frame = ctk.CTkFrame(self.root)
        stats_frame.pack(pady=20, padx=50, fill="x")
        
        stats_label = ctk.CTkLabel(stats_frame, text="Statistics", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        stats_label.pack(pady=10)
        
        # Calculate statistics
        phonetic_total = len(self.exercise_history["phonetic"])
        phonetic_correct = sum(1 for ex in self.exercise_history["phonetic"] if ex.get("correct", False))
        phonetic_rate = (phonetic_correct / phonetic_total * 100) if phonetic_total > 0 else 0
        
        stress_total = len(self.exercise_history["stress"])
        stress_correct = sum(1 for ex in self.exercise_history["stress"] if ex.get("correct", False))
        stress_rate = (stress_correct / stress_total * 100) if stress_total > 0 else 0
        
        phonetic_stats = ctk.CTkLabel(stats_frame, 
                                    text=f"Phonetic Discrimination: {phonetic_correct}/{phonetic_total} ({phonetic_rate:.1f}%)")
        phonetic_stats.pack(pady=2)
        
        stress_stats = ctk.CTkLabel(stats_frame, 
                                  text=f"Stress Pattern: {stress_correct}/{stress_total} ({stress_rate:.1f}%)")
        stress_stats.pack(pady=2)
        
    def start_exercise(self):
        """Start the exercise based on selected mode"""
        self.current_mode = self.mode_var.get()
        self.questions_answered = 0
        self.correct_answers = 0
        
        # Reset session tracking
        self.session_total = 0
        self.session_correct = 0
        
        self.setup_exercise_interface()
        self.generate_next_question()
        
    def setup_exercise_interface(self):
        """Setup the exercise interface"""
        self.clear_window()
        
        # Title and mode display
        mode_text = {
            "phonetic": "Phonetic Discrimination - Underlined Part",
            "stress": "Stress Pattern Recognition", 
            "both": "Mixed Exercise Mode"
        }
        
        title = ctk.CTkLabel(self.root, text=mode_text[self.current_mode], 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Progress bar frame
        progress_frame = ctk.CTkFrame(self.root)
        progress_frame.pack(pady=10, padx=50, fill="x")
        
        # Create progress label and bar
        self.progress_label = ctk.CTkLabel(progress_frame, text="Session Accuracy: 0/0 (0.0%)")
        self.progress_label.pack(side="left", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(side="right", padx=10, fill="x", expand=True)
        self.progress_bar.set(0)
        
        # Historical accuracy display
        current_mode_for_stats = self.current_mode if self.current_mode != "both" else "phonetic"
        total_exercises = len(self.exercise_history[current_mode_for_stats])
        correct_exercises = sum(1 for ex in self.exercise_history[current_mode_for_stats] if ex.get("correct", False))
        historical_accuracy = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        self.historical_label = ctk.CTkLabel(progress_frame, 
                                           text=f"Historical: {correct_exercises}/{total_exercises} ({historical_accuracy:.1f}%)")
        self.historical_label.pack(side="left", padx=(20, 10))
        
        # Question frame
        self.question_frame = ctk.CTkFrame(self.root)
        self.question_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(pady=10, padx=50, fill="x")
        
        self.check_button = ctk.CTkButton(control_frame, text="Check Answer", 
                                        command=self.check_answer, state="normal")
        self.check_button.pack(side="left", padx=10)
        
        self.next_button = ctk.CTkButton(control_frame, text="Next Question", 
                                       command=self.generate_next_question, state="disabled")
        self.next_button.pack(side="left", padx=10)
        
        self.back_button = ctk.CTkButton(control_frame, text="Back to Menu", 
                                       command=self.setup_main_menu)
        self.back_button.pack(side="right", padx=10)
        
        # Result frame (initially hidden)
        self.result_frame = ctk.CTkFrame(self.root)
        
    def update_progress_display(self):
        """Update the progress bar and labels with current session data"""
        # Calculate session accuracy
        session_accuracy = (self.session_correct / self.session_total * 100) if self.session_total > 0 else 0
        
        # Update progress label
        self.progress_label.configure(text=f"Session Accuracy: {self.session_correct}/{self.session_total} ({session_accuracy:.1f}%)")
        
        # Update progress bar
        progress_value = session_accuracy / 100 if self.session_total > 0 else 0
        self.progress_bar.set(progress_value)
        
        # Update historical accuracy (in case new data was added)
        current_mode_for_stats = self.current_mode if self.current_mode != "both" else "phonetic"
        total_exercises = len(self.exercise_history[current_mode_for_stats])
        correct_exercises = sum(1 for ex in self.exercise_history[current_mode_for_stats] if ex.get("correct", False))
        historical_accuracy = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        self.historical_label.configure(text=f"Historical: {correct_exercises}/{total_exercises} ({historical_accuracy:.1f}%)")
        
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def arpabet_to_ipa(self, arpabet_phones):
        """Convert ARPAbet phonemes to IPA"""
        ipa_phones = []
        for phone in arpabet_phones:
            # Remove stress markers
            clean_phone = re.sub(r'[0-2]', '', phone)
            ipa = self.arpabet_ipa_map.get(clean_phone, phone)
            ipa_phones.append(ipa)
        return ipa_phones
        
    def get_stress_pattern(self, arpabet_phones):
        """Extract stress pattern from ARPAbet phonemes"""
        stress_pattern = []
        for phone in arpabet_phones:
            if re.search(r'[0-2]', phone):
                if '1' in phone:
                    stress_pattern.append(1)  # Primary stress
                elif '2' in phone:
                    stress_pattern.append(2)  # Secondary stress
                else:
                    stress_pattern.append(0)  # No stress
        return stress_pattern
        
    def find_confused_ipa_sounds(self):
        """Find IPA sounds that are frequently confused based on history"""
        if self.current_mode == "phonetic" or self.current_mode == "both":
            phonetic_errors = defaultdict(int)
            phonetic_total = defaultdict(int)
            
            for exercise in self.exercise_history["phonetic"]:
                if "target_ipa" in exercise:
                    target_ipa = exercise["target_ipa"]
                    phonetic_total[target_ipa] += 1
                    if not exercise.get("correct", False):
                        phonetic_errors[target_ipa] += 1
                        
            # Calculate error rates
            error_rates = {}
            for ipa in phonetic_total:
                if phonetic_total[ipa] > 0:
                    error_rates[ipa] = phonetic_errors[ipa] / phonetic_total[ipa]
                    
            return error_rates
        return {}
        
    def generate_phonetic_question(self, target_ipa_sounds=None):
        """Generate a phonetic discrimination question"""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            try:
                # Generate random words
                words = []
                for _ in range(20):  # Generate more words to have options
                    word = self.word_generator.word()
                    if word and len(word) > 2:
                        words.append(word.lower())
                
                # Get pronunciations and IPA conversions
                word_data = []
                for word in words:
                    pronunciations = pronouncing.phones_for_word(word)
                    if pronunciations:
                        arpabet = pronunciations[0].split()
                        ipa = self.arpabet_to_ipa(arpabet)
                        word_data.append({
                            'word': word,
                            'arpabet': arpabet,
                            'ipa': ipa
                        })
                
                if len(word_data) < 4:
                    attempts += 1
                    continue
                    
                # Find suitable question set
                question_found = False
                
                # Try to use confusion groups
                for group in self.ipa_confusion_groups:
                    if question_found:
                        break
                        
                    # Find words with sounds from this confusion group
                    group_words = defaultdict(list)
                    for word_info in word_data:
                        for i, ipa_sound in enumerate(word_info['ipa']):
                            if ipa_sound in group:
                                group_words[ipa_sound].append((word_info, i))
                                
                    # Try to create a question from this group
                    for target_sound in group:
                        if len(group_words[target_sound]) >= 3:
                            # Find a different sound from the same group
                            different_sound = None
                            for other_sound in group:
                                if other_sound != target_sound and len(group_words[other_sound]) >= 1:
                                    different_sound = other_sound
                                    break
                                    
                            if different_sound:
                                # Create question
                                correct_words = random.sample(group_words[target_sound], 3)
                                incorrect_word = random.choice(group_words[different_sound])
                                
                                options = [
                                    (word_info['word'], pos, target_sound) for word_info, pos in correct_words
                                ] + [(incorrect_word[0]['word'], incorrect_word[1], different_sound)]
                                
                                random.shuffle(options)
                                
                                correct_answer = None
                                for i, (word, pos, sound) in enumerate(options):
                                    if sound == different_sound:
                                        correct_answer = i
                                        break
                                        
                                self.current_question = {
                                    'type': 'phonetic',
                                    'options': options,
                                    'correct_answer': correct_answer,
                                    'target_ipa': target_sound,
                                    'different_ipa': different_sound
                                }
                                question_found = True
                                break
                                
                if question_found:
                    break
                    
                attempts += 1
                
            except Exception as e:
                attempts += 1
                continue
                
        if not question_found:
            # Fallback: create a simple question
            if len(word_data) >= 4:
                selected = random.sample(word_data, 4)
                options = [(w['word'], 0, w['ipa'][0] if w['ipa'] else '') for w in selected]
                self.current_question = {
                    'type': 'phonetic',
                    'options': options,
                    'correct_answer': random.randint(0, 3),
                    'target_ipa': 'fallback',
                    'different_ipa': 'fallback'
                }
            else:
                # Ultimate fallback
                options = [('cat', 0, 'Ã¦'), ('bat', 0, 'Ã¦'), ('hat', 0, 'Ã¦'), ('beat', 0, 'i')]
                self.current_question = {
                    'type': 'phonetic',
                    'options': options,
                    'correct_answer': 3,
                    'target_ipa': 'Ã¦',
                    'different_ipa': 'i'
                }
                
    def generate_stress_question(self):
        """Generate a stress pattern recognition question"""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            try:
                # Generate words with stress patterns
                words_with_stress = []
                for _ in range(30):
                    word = self.word_generator.word()
                    if word and len(word) > 3:
                        pronunciations = pronouncing.phones_for_word(word.lower())
                        if pronunciations:
                            arpabet = pronunciations[0].split()
                            stress_pattern = self.get_stress_pattern(arpabet)
                            if stress_pattern and len(stress_pattern) >= 2:
                                # Find primary stress position
                                stress_pos = None
                                for i, stress in enumerate(stress_pattern):
                                    if stress == 1:
                                        stress_pos = i
                                        break
                                        
                                if stress_pos is not None:
                                    words_with_stress.append({
                                        'word': word.lower(),
                                        'stress_pattern': stress_pattern,
                                        'stress_position': stress_pos,
                                        'syllables': len(stress_pattern)
                                    })
                
                if len(words_with_stress) < 4:
                    attempts += 1
                    continue
                    
                # Group by stress position and syllable count
                stress_groups = defaultdict(list)
                for word_info in words_with_stress:
                    key = (word_info['stress_position'], word_info['syllables'])
                    stress_groups[key].append(word_info)
                    
                # Find a group with at least 3 words
                target_group = None
                for key, words in stress_groups.items():
                    if len(words) >= 3:
                        target_group = (key, words)
                        break
                        
                if target_group:
                    key, words = target_group
                    target_stress_pos, target_syllables = key
                    
                    # Find words with different stress pattern
                    different_words = []
                    for other_key, other_words in stress_groups.items():
                        if other_key != key and len(other_words) > 0:
                            different_words.extend(other_words)
                            
                    if different_words:
                        correct_words = random.sample(words, min(3, len(words)))
                        incorrect_word = random.choice(different_words)
                        
                        options = [w['word'] for w in correct_words] + [incorrect_word['word']]
                        random.shuffle(options)
                        
                        correct_answer = None
                        for i, word in enumerate(options):
                            if word == incorrect_word['word']:
                                correct_answer = i
                                break
                                
                        self.current_question = {
                            'type': 'stress',
                            'options': [(word, 0, '') for word in options],  # Consistent format
                            'correct_answer': correct_answer,
                            'target_stress_position': target_stress_pos,
                            'target_syllables': target_syllables
                        }
                        break
                        
                attempts += 1
                
            except Exception as e:
                attempts += 1
                continue
                
        # Fallback stress question
        if not hasattr(self, 'current_question') or self.current_question is None:
            options = [('photograph', 0, ''), ('photography', 0, ''), ('photographer', 0, ''), ('computer', 0, '')]
            self.current_question = {
                'type': 'stress',
                'options': options,
                'correct_answer': 3,
                'target_stress_position': 0,
                'target_syllables': 3
            }
            
    def generate_next_question(self):
        """Generate the next question based on current mode"""
        self.current_question = None
        self.current_answer = None
        
        # Determine question type
        if self.current_mode == "both":
            question_type = random.choice(["phonetic", "stress"])
        else:
            question_type = self.current_mode
            
        # Generate question based on type
        if question_type == "phonetic":
            self.generate_phonetic_question()
        else:
            self.generate_stress_question()
            
        # Display the question
        self.display_question()
        
        # Reset buttons
        self.check_button.configure(state="normal")
        self.next_button.configure(state="disabled")
        self.result_frame.pack_forget()
        
    def display_question(self):
        """Display the current question"""
        # Clear previous question
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        if not self.current_question:
            return
            
        question_type = self.current_question['type']
        
        if question_type == "phonetic":
            instruction = "Choose the word with the DIFFERENT underlined sound:"
        else:
            instruction = "Choose the word with the DIFFERENT stress pattern:"
            
        instruction_label = ctk.CTkLabel(self.question_frame, text=instruction, 
                                       font=ctk.CTkFont(size=16))
        instruction_label.pack(pady=20)
        
        # Create option buttons
        self.option_var = ctk.StringVar()
        self.option_buttons = []
        
        for i, (word, pos, ipa) in enumerate(self.current_question['options']):
            if question_type == "phonetic":
                # For phonetic questions, show underlined part
                display_word = self.create_underlined_word(word, pos, ipa)
                text = f"{chr(65+i)}. {display_word}"
            else:
                # For stress questions, show word with stress marks
                text = f"{chr(65+i)}. {word}"
                
            btn = ctk.CTkRadioButton(self.question_frame, text=text, 
                                   variable=self.option_var, value=str(i),
                                   font=ctk.CTkFont(size=14))
            btn.pack(pady=5, anchor="w", padx=50)
            self.option_buttons.append(btn)
            
    def create_underlined_word(self, word, pos, ipa):
        """Create word with underlined part (simplified representation)"""
        # This is a simplified version - in a real app you might want 
        # more sophisticated phoneme-to-letter mapping
        if pos < len(word):
            return f"{word[:pos]}[{word[pos]}]{word[pos+1:]}"
        return f"[{word[0]}]{word[1:]}"
        
    def check_answer(self):
        """Check the user's answer"""
        if not self.current_question or not self.option_var.get():
            return
            
        user_answer = int(self.option_var.get())
        correct_answer = self.current_question['correct_answer']
        is_correct = user_answer == correct_answer
        
        self.current_answer = user_answer
        self.questions_answered += 1
        if is_correct:
            self.correct_answers += 1
            
        # Update session tracking
        self.session_total += 1
        if is_correct:
            self.session_correct += 1
            
        # Update progress display immediately
        self.update_progress_display()
        
        # Save to history
        exercise_type = self.current_question['type']
        exercise_record = {
            'timestamp': datetime.now().isoformat(),
            'question_type': exercise_type,
            'correct': is_correct,
            'user_answer': user_answer,
            'correct_answer': correct_answer
        }
        
        if exercise_type == 'phonetic':
            exercise_record['target_ipa'] = self.current_question.get('target_ipa', '')
        
        self.exercise_history[exercise_type].append(exercise_record)
        self.save_exercise_history()
        
        # Show result
        self.show_result(is_correct)
        
        # Update buttons
        self.check_button.configure(state="disabled")
        self.next_button.configure(state="normal")
        
    def show_result(self, is_correct):
        """Show the result of the answer"""
        self.result_frame.pack(pady=20, padx=50, fill="x")
        
        # Clear previous result
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        # Result message
        if is_correct:
            result_text = "✓ Correct!"
            text_color = "green"
        else:
            correct_option = chr(65 + self.current_question['correct_answer'])
            result_text = f"✗ Incorrect. The correct answer is {correct_option}."
            text_color = "red"
            
        result_label = ctk.CTkLabel(self.result_frame, text=result_text, 
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color=text_color)
        result_label.pack(pady=10)
        
        # Explanation
        explanation = self.get_explanation()
        if explanation:
            exp_label = ctk.CTkLabel(self.result_frame, text=explanation,
                                   font=ctk.CTkFont(size=12))
            exp_label.pack(pady=5)
            
        # Pronunciation buttons
        self.create_pronunciation_buttons()
        
    def get_explanation(self):
        """Get explanation for the question"""
        if not self.current_question:
            return ""
            
        question_type = self.current_question['type']
        
        if question_type == 'phonetic':
            target_ipa = self.current_question.get('target_ipa', '')
            different_ipa = self.current_question.get('different_ipa', '')
            return f"The target sound is /{target_ipa}/, while the different word has /{different_ipa}/."
        else:
            target_pos = self.current_question.get('target_stress_position', 0)
            return f"Three words have primary stress on syllable {target_pos + 1}, while one is different."
            
    def create_pronunciation_buttons(self):
        """Create buttons to hear pronunciation of each word"""
        if not self.current_question:
            return
            
        button_frame = ctk.CTkFrame(self.result_frame)
        button_frame.pack(pady=10, fill="x")
        
        play_label = ctk.CTkLabel(button_frame, text="Listen to pronunciations:")
        play_label.pack(pady=5)
        
        for i, (word, _, _) in enumerate(self.current_question['options']):
            btn = ctk.CTkButton(button_frame, text=f"Play {chr(65+i)}: {word}",
                              command=lambda w=word: self.play_pronunciation(w),
                              width=150, height=30)
            btn.pack(side="left", padx=5, pady=5)
            
    def play_pronunciation(self, word):
        """Play pronunciation of a word using text-to-speech"""
        def speak():
            try:
                self.tts.setProperty('rate', self.speech_rate)
                self.tts.say(word)
                self.tts.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
                
        # Run TTS in a separate thread to avoid blocking UI
        thread = threading.Thread(target=speak, daemon=True)
        thread.start()
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PhoneticDiscriminationApp()
    app.run()
