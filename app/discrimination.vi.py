import customtkinter as ctk
import yaml
import random
import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import pronouncing
from wonderwords import RandomWord
import re
from collections import defaultdict
import os

class PhoneticDiscriminationApp:
    def __init__(self):
        # Initialize the app
        self.root = ctk.CTk()
        self.root.title("Bài tập Phân biệt Ngữ âm")
        self.root.geometry("800x650")
        
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
        except FileNotFoundError:
            self.color_scheme = 'blue'
            self.theme = 'dark'
            
    def load_data(self):
        """Load ARPAbet-IPA mapping and confusion groups"""
        # Load ARPAbet to IPA mapping
        try:
            with open('arpabet_ipa_database.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.arpabet_ipa_map[row['ARPAbet']] = row['IPA']
        except FileNotFoundError:
            print("Cảnh báo: không tìm thấy arpabet_ipa_database.csv")
            
        # Load IPA confusion groups
        try:
            with open('ipa_confusion_groups.yaml', 'r', encoding='utf-8') as f:
                self.ipa_confusion_groups = yaml.safe_load(f)
        except FileNotFoundError:
            print("Cảnh báo: không tìm thấy ipa_confusion_groups.yaml")
            
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
        title = ctk.CTkLabel(self.root, text="Bài tập Phân biệt Ngữ âm", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=30)
        
        # Mode selection frame
        mode_frame = ctk.CTkFrame(self.root)
        mode_frame.pack(pady=20, padx=50, fill="x")
        
        mode_label = ctk.CTkLabel(mode_frame, text="Chọn chế độ bài tập:", 
                                font=ctk.CTkFont(size=16))
        mode_label.pack(pady=10)
        
        # Mode selection
        self.mode_var = ctk.StringVar(value="both")
        
        phonetic_radio = ctk.CTkRadioButton(mode_frame, text="Phân biệt Ngữ âm (Phần đánh dấu)", 
                                          variable=self.mode_var, value="phonetic")
        phonetic_radio.pack(pady=5)
        
        stress_radio = ctk.CTkRadioButton(mode_frame, text="Nhận biết Trọng âm", 
                                        variable=self.mode_var, value="stress")
        stress_radio.pack(pady=5)
        
        both_radio = ctk.CTkRadioButton(mode_frame, text="Cả hai bài tập (Mặc định)", 
                                      variable=self.mode_var, value="both")
        both_radio.pack(pady=5)
        
        # Start button
        start_button = ctk.CTkButton(self.root, text="Bắt đầu", 
                                   command=self.start_exercise, font=ctk.CTkFont(size=16))
        start_button.pack(pady=30)
        
        # Statistics
        self.show_statistics()
        
    def show_statistics(self):
        """Display current statistics"""
        stats_frame = ctk.CTkFrame(self.root)
        stats_frame.pack(pady=20, padx=50, fill="x")
        
        stats_label = ctk.CTkLabel(stats_frame, text="Thống kê", 
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
                                    text=f"Phân biệt Ngữ âm: {phonetic_correct}/{phonetic_total} ({phonetic_rate:.1f}%)")
        phonetic_stats.pack(pady=2)
        
        stress_stats = ctk.CTkLabel(stats_frame, 
                                  text=f"Nhận biết Trọng âm: {stress_correct}/{stress_total} ({stress_rate:.1f}%)")
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
            "phonetic": "Phân biệt Ngữ âm - Phần đánh dấu",
            "stress": "Nhận biết Trọng âm", 
            "both": "Chế độ Hỗn hợp"
        }
        
        title = ctk.CTkLabel(self.root, text=mode_text[self.current_mode], 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Progress bar frame
        progress_frame = ctk.CTkFrame(self.root)
        progress_frame.pack(pady=10, padx=50, fill="x")
        
        # Create progress label and bar
        self.progress_label = ctk.CTkLabel(progress_frame, text="Độ chính xác phiên: 0/0 (0.0%)")
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
                                           text=f"Lịch sử: {correct_exercises}/{total_exercises} ({historical_accuracy:.1f}%)")
        self.historical_label.pack(side="left", padx=(20, 10))
        
        # Question frame
        self.question_frame = ctk.CTkFrame(self.root)
        self.question_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(pady=10, padx=50, fill="x")
        
        self.check_button = ctk.CTkButton(control_frame, text="Kiểm tra", 
                                        command=self.check_answer, state="normal")
        self.check_button.pack(side="left", padx=10)
        
        self.next_button = ctk.CTkButton(control_frame, text="Câu tiếp theo", 
                                       command=self.generate_next_question, state="disabled")
        self.next_button.pack(side="left", padx=10)
        
        self.back_button = ctk.CTkButton(control_frame, text="Về trang chủ", 
                                       command=self.setup_main_menu)
        self.back_button.pack(side="right", padx=10)
        
        # Result frame (initially hidden)
        self.result_frame = ctk.CTkFrame(self.root)
        
    def update_progress_display(self):
        """Update the progress bar and labels with current session data"""
        # Calculate session accuracy
        session_accuracy = (self.session_correct / self.session_total * 100) if self.session_total > 0 else 0
        
        # Update progress label
        self.progress_label.configure(text=f"Độ chính xác phiên: {self.session_correct}/{self.session_total} ({session_accuracy:.1f}%)")
        
        # Update progress bar
        progress_value = session_accuracy / 100 if self.session_total > 0 else 0
        self.progress_bar.set(progress_value)
        
        # Update historical accuracy (in case new data was added)
        current_mode_for_stats = self.current_mode if self.current_mode != "both" else "phonetic"
        total_exercises = len(self.exercise_history[current_mode_for_stats])
        correct_exercises = sum(1 for ex in self.exercise_history[current_mode_for_stats] if ex.get("correct", False))
        historical_accuracy = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        self.historical_label.configure(text=f"Lịch sử: {correct_exercises}/{total_exercises} ({historical_accuracy:.1f}%)")
        
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
    
    def get_letter_representation(self, word, phone_index, arpabet):
        """
        Find which letter(s) in the word correspond to a phoneme
        Returns start_pos, end_pos, and the letter string
        """
        # Common phoneme-to-letter patterns
        phoneme_patterns = {
            'AE': ['a'], 'AA': ['o', 'a'], 'AH': ['u', 'o', 'a'], 'AO': ['aw', 'au', 'o'],
            'AW': ['ow', 'ou'], 'AY': ['i', 'y', 'igh', 'ie'], 'B': ['b', 'bb'],
            'CH': ['ch', 'tch', 't'], 'D': ['d', 'dd', 'ed'], 'DH': ['th'],
            'EH': ['e', 'ea'], 'ER': ['er', 'ir', 'ur', 'or', 'ar'], 'EY': ['a', 'ai', 'ay', 'ea', 'ei'],
            'F': ['f', 'ff', 'ph', 'gh'], 'G': ['g', 'gg', 'gh'], 'HH': ['h', 'wh'],
            'IH': ['i', 'y', 'e'], 'IY': ['ee', 'ea', 'e', 'ie', 'y', 'i'], 'JH': ['j', 'g', 'dge'],
            'K': ['c', 'k', 'ck', 'ch', 'q'], 'L': ['l', 'll'], 'M': ['m', 'mm'],
            'N': ['n', 'nn', 'kn', 'gn'], 'NG': ['ng', 'n'], 'OW': ['o', 'oa', 'ow', 'oe'],
            'OY': ['oi', 'oy'], 'P': ['p', 'pp'], 'R': ['r', 'rr', 'wr'],
            'S': ['s', 'ss', 'c', 'ce'], 'SH': ['sh', 'ti', 'ci', 'ch'], 'T': ['t', 'tt', 'ed'],
            'TH': ['th'], 'UH': ['oo', 'u', 'ou'], 'UW': ['oo', 'u', 'ue', 'ew', 'ou'],
            'V': ['v', 'f'], 'W': ['w', 'wh', 'u'], 'Y': ['y'], 'Z': ['z', 'zz', 's'],
            'ZH': ['s', 'si', 'z']
        }
        
        # Get the phoneme (remove stress markers)
        phoneme = re.sub(r'[0-2]', '', arpabet[phone_index])
        
        # Get possible letter patterns
        patterns = phoneme_patterns.get(phoneme, [phoneme.lower()])
        
        # Try to find the pattern in the word
        # Start from the approximate position based on phoneme index
        estimated_pos = int(len(word) * phone_index / len(arpabet))
        
        # Search around the estimated position
        search_start = max(0, estimated_pos - 2)
        search_end = min(len(word), estimated_pos + 4)
        
        for pattern in patterns:
            for i in range(search_start, search_end):
                if i + len(pattern) <= len(word):
                    if word[i:i+len(pattern)].lower() == pattern:
                        return i, i + len(pattern), word[i:i+len(pattern)]
        
        # Fallback: return single letter at estimated position
        pos = min(estimated_pos, len(word) - 1)
        return pos, pos + 1, word[pos]
        
    def generate_phonetic_question(self, target_ipa_sounds=None):
        """Generate a phonetic discrimination question with same spelling for underlined parts"""
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            try:
                # Generate random words
                words = []
                for _ in range(50):  # Generate more words to have options
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
                
                # Find suitable question set with SAME LETTER(S) but different sounds
                question_found = False
                
                # Try to use confusion groups
                shuffled_groups = random.sample(self.ipa_confusion_groups, len(self.ipa_confusion_groups))
                for group in shuffled_groups:
                    if question_found:
                        break
                    
                    # Find words with sounds from this confusion group
                    # Group by letter representation
                    letter_sound_map = defaultdict(lambda: defaultdict(list))
                    
                    for word_info in word_data:
                        for i, ipa_sound in enumerate(word_info['ipa']):
                            if ipa_sound in group:
                                # Get letter representation
                                start, end, letters = self.get_letter_representation(
                                    word_info['word'], i, word_info['arpabet']
                                )
                                letters_lower = letters.lower()
                                letter_sound_map[letters_lower][ipa_sound].append({
                                    'word_info': word_info,
                                    'phone_index': i,
                                    'start': start,
                                    'end': end,
                                    'letters': letters
                                })
                    
                    # Look for letter patterns that have multiple sounds
                    for letter_pattern, sounds_dict in letter_sound_map.items():
                        if len(sounds_dict) >= 2:  # Same letters, different sounds
                            sounds_list = list(sounds_dict.keys())
                            
                            # Find a combination where we have 3+ words with one sound
                            # and 1+ word with a different sound
                            for i, target_sound in enumerate(sounds_list):
                                for j, different_sound in enumerate(sounds_list):
                                    if i != j:
                                        target_words = sounds_dict[target_sound]
                                        different_words = sounds_dict[different_sound]
                                        
                                        if len(target_words) >= 3 and len(different_words) >= 1:
                                            # Create question
                                            correct_selections = random.sample(target_words, 3)
                                            incorrect_selection = random.choice(different_words)
                                            
                                            options = []
                                            for sel in correct_selections:
                                                options.append((
                                                    sel['word_info']['word'],
                                                    sel['start'],
                                                    sel['end'],
                                                    sel['letters'],
                                                    target_sound
                                                ))
                                            
                                            options.append((
                                                incorrect_selection['word_info']['word'],
                                                incorrect_selection['start'],
                                                incorrect_selection['end'],
                                                incorrect_selection['letters'],
                                                different_sound
                                            ))
                                            
                                            random.shuffle(options)
                                            
                                            # Find correct answer index
                                            correct_answer = None
                                            for idx, (word, start, end, letters, sound) in enumerate(options):
                                                if sound == different_sound:
                                                    correct_answer = idx
                                                    break
                                            
                                            self.current_question = {
                                                'type': 'phonetic',
                                                'options': options,
                                                'correct_answer': correct_answer,
                                                'target_ipa': target_sound,
                                                'different_ipa': different_sound,
                                                'letter_pattern': letter_pattern
                                            }
                                            question_found = True
                                            break
                                
                                if question_found:
                                    break
                        
                        if question_found:
                            break
                
                if question_found:
                    break
                
                attempts += 1
                
            except Exception as e:
                attempts += 1
                continue
        
        # Fallback questions with same spelling but different pronunciation
        if not question_found:
            # Example: 'ea' can be pronounced as /i/ or /ɛ/
            fallback_questions = [
                {
                    'options': [
                        ('read', 1, 3, 'ea', 'i'),  # /ri:d/ (present)
                        ('bead', 1, 3, 'ea', 'i'),
                        ('lead', 1, 3, 'ea', 'i'),  # /li:d/ (metal)
                        ('bread', 2, 4, 'ea', 'ɛ')  # /brɛd/
                    ],
                    'target_ipa': 'i',
                    'different_ipa': 'ɛ',
                    'letter_pattern': 'ea'
                },
                {
                    'options': [
                        ('bow', 1, 2, 'ow', 'aʊ'),  # /baʊ/ (to bend)
                        ('cow', 1, 2, 'ow', 'aʊ'),
                        ('now', 1, 2, 'ow', 'aʊ'),
                        ('low', 1, 2, 'ow', 'oʊ')   # /loʊ/
                    ],
                    'target_ipa': 'aʊ',
                    'different_ipa': 'oʊ',
                    'letter_pattern': 'ow'
                },
                {
                    'options': [
                        ('food', 1, 3, 'oo', 'u'),
                        ('moon', 1, 3, 'oo', 'u'),
                        ('pool', 1, 3, 'oo', 'u'),
                        ('book', 1, 3, 'oo', 'ʊ')
                    ],
                    'target_ipa': 'u',
                    'different_ipa': 'ʊ',
                    'letter_pattern': 'oo'
                }
            ]
            
            fallback = random.choice(fallback_questions)
            random.shuffle(fallback['options'])
            
            # Find correct answer
            correct_answer = None
            for i, (word, start, end, letters, sound) in enumerate(fallback['options']):
                if sound == fallback['different_ipa']:
                    correct_answer = i
                    break
            
            self.current_question = {
                'type': 'phonetic',
                'options': fallback['options'],
                'correct_answer': correct_answer,
                'target_ipa': fallback['target_ipa'],
                'different_ipa': fallback['different_ipa'],
                'letter_pattern': fallback['letter_pattern']
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
                            'options': [(word, 0, 0, '', '') for word in options],
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
            options = [('photograph', 0, 0, '', ''), ('photography', 0, 0, '', ''), ('photographer', 0, 0, '', ''), ('computer', 0, 0, '', '')]
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
            instruction = "Chọn từ có phần đánh dấu phát âm KHÁC:"
        else:
            instruction = "Chọn từ có trọng âm KHÁC:"
            
        instruction_label = ctk.CTkLabel(self.question_frame, text=instruction, 
                                       font=ctk.CTkFont(size=16))
        instruction_label.pack(pady=20)
        
        # Create option buttons
        self.option_var = ctk.StringVar()
        self.option_buttons = []
        
        for i, option_data in enumerate(self.current_question['options']):
            if question_type == "phonetic":
                # For phonetic questions, show underlined part
                word = option_data[0]
                start = option_data[1]
                end = option_data[2]
                letters = option_data[3]
                
                # Create display with underlined section
                display_word = self.create_underlined_word_display(word, start, end)
                text = f"{chr(65+i)}. {display_word}"
            else:
                # For stress questions, show word with stress marks
                word = option_data[0]
                text = f"{chr(65+i)}. {word}"
                
            btn = ctk.CTkRadioButton(self.question_frame, text=text, 
                                   variable=self.option_var, value=str(i),
                                   font=ctk.CTkFont(size=14))
            btn.pack(pady=5, anchor="w", padx=50)
            self.option_buttons.append(btn)
            
    def create_underlined_word_display(self, word, start, end):
        """Create word with underlined part using brackets"""
        if start < len(word) and end <= len(word):
            before = word[:start]
            underlined = word[start:end]
            after = word[end:]
            return f"{before}[{underlined}]{after}"
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
            result_text = "✓ Chính xác!"
            text_color = "green"
        else:
            correct_option = chr(65 + self.current_question['correct_answer'])
            result_text = f"✗ Sai rồi. Đáp án đúng là {correct_option}."
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
        
    def get_explanation(self):
        """Get explanation for the question"""
        if not self.current_question:
            return ""
            
        question_type = self.current_question['type']
        
        if question_type == 'phonetic':
            target_ipa = self.current_question.get('target_ipa', '')
            different_ipa = self.current_question.get('different_ipa', '')
            letter_pattern = self.current_question.get('letter_pattern', '')
            
            if letter_pattern:
                return f"Cả 4 từ đều có '{letter_pattern}' nhưng 3 từ phát âm là /{target_ipa}/, còn 1 từ phát âm là /{different_ipa}/."
            else:
                return f"Âm đích là /{target_ipa}/, trong khi từ khác có âm /{different_ipa}/."
        else:
            target_pos = self.current_question.get('target_stress_position', 0)
            return f"Ba từ có trọng âm chính ở âm tiết thứ {target_pos + 1}, còn một từ khác."
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PhoneticDiscriminationApp()
    app.run()
