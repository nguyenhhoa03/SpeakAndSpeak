#!/usr/bin/env python3
"""
sentence-generator.py

A script that generates sentences based on user performance analysis.
Can be run standalone or imported into other scripts.

Requirements:
- eng-to-ipa
- PyYAML

Install with: pip install eng-to-ipa PyYAML
"""

import yaml
import random
import csv
import os
import re
import sqlite3
from collections import Counter
from eng_to_ipa import ipa_list


def load_user_data(file_path="user-data.yaml"):
    """Load and parse user data from YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using empty data.")
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def analyze_last_20_nodes(data):
    """
    Analyze the last 20 nodes to get wrong IPA sounds and calculate error rate.
    
    Returns:
        tuple: (wrong_ipa_counter, error_rate_percentage)
    """
    if not data:
        return Counter(), 0
    
    # Get last 20 nodes
    last_20 = data[-20:] if len(data) >= 20 else data
    
    # Count wrong results
    wrong_count = sum(1 for node in last_20 if not node.get('result', True))
    error_rate = (wrong_count / len(last_20)) * 100
    
    # Collect all wrong IPA sounds
    wrong_ipa_sounds = []
    for node in last_20:
        if not node.get('result', True) and 'wrong_words' in node:
            for word_data in node['wrong_words']:
                if 'wrong_ipa' in word_data:
                    wrong_ipa_sounds.extend(word_data['wrong_ipa'])
    
    return Counter(wrong_ipa_sounds), error_rate


def _get_db_path(file_path):
    """Convert TSV file path to SQLite DB path."""
    if file_path.endswith('.tsv'):
        return file_path.replace('.tsv', '.db')
    return file_path


def _is_sqlite_db(file_path):
    """Check if file is SQLite database."""
    db_path = _get_db_path(file_path)
    if not os.path.exists(db_path):
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sentences'")
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False


def get_file_line_count(file_path):
    """Get total number of lines/rows in file efficiently."""
    db_path = _get_db_path(file_path)
    if _is_sqlite_db(file_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sentences WHERE lang='eng'")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting DB count: {e}")
            return 1991044
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f)
    except:
        return 1991044


def has_numbers(sentence):
    """Check if sentence contains any numbers (digits)."""
    return bool(re.search(r'\d', sentence))


def get_random_words_from_db(file_path="eng_sentences.tsv", count=100, max_attempts=10):
    """
    Extract random words from sentences in SQLite DB.
    Filter out words starting with capital letters (proper nouns).
    
    Args:
        file_path: Path to the TSV file (will auto-convert to .db if exists)
        count: Number of words to retrieve
        max_attempts: Maximum attempts to find valid words
    
    Returns:
        list: List of lowercase words without capital initials or numbers
    """
    db_path = _get_db_path(file_path)
    
    if not _is_sqlite_db(file_path):
        return ["fallback", "word", "test"]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        words = []
        attempts = 0
        fetch_count = count * 3
        
        while len(words) < count and attempts < max_attempts:
            cursor.execute("""
                SELECT sentence FROM sentences 
                WHERE lang='eng' 
                AND LENGTH(sentence) >= 10
                AND LENGTH(sentence) <= 100
                ORDER BY RANDOM() 
                LIMIT ?
            """, (fetch_count,))
            
            results = cursor.fetchall()
            
            for result in results:
                if len(words) >= count:
                    break
                
                sentence = result[0].strip()
                if has_numbers(sentence):
                    continue
                
                # Split sentence into words and filter
                sentence_words = sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(';', '').replace(':', '').split()
                
                for word in sentence_words:
                    if len(words) >= count:
                        break
                    
                    clean_word = word.strip('.,!?;:"()[]{}\'')
                    
                    # Skip words starting with capital letter (likely proper nouns)
                    if clean_word and clean_word[0].isupper():
                        continue
                    
                    # Skip words with numbers or too short
                    if clean_word and len(clean_word) > 2 and not has_numbers(clean_word):
                        if clean_word.lower() not in words:
                            words.append(clean_word.lower())
            
            attempts += 1
            if len(results) == 0:
                break
        
        conn.close()
        
        # Fill with fallback if needed
        while len(words) < count:
            words.append(f"word{len(words) + 1}")
        
        return words[:count]
        
    except Exception as e:
        print(f"Error reading words from SQLite DB {db_path}: {e}")
        return ["fallback", "word", "test"]


def get_random_sentence_from_file(file_path="eng_sentences.tsv", max_attempts=10, lv=0):
    """
    Get a random sentence from TSV file or SQLite DB efficiently.
    Skip sentences containing numbers.
    
    Args:
        file_path: Path to the TSV file (will auto-convert to .db if exists)
        max_attempts: Maximum attempts to find a sentence without numbers
        lv: Difficulty level (0=auto, 1=easy/word, 2=medium, 3=hard/long)
    
    Returns:
        str: Random sentence from column C (3rd column) without numbers, or single word for lv=1
    """
    # Special handling for lv=1: return single word instead of sentence
    if lv == 1:
        words = get_random_words_from_db(file_path, count=1, max_attempts=max_attempts)
        if words:
            return words[0].capitalize()
        return "Word"
    
    db_path = _get_db_path(file_path)
    
    length_ranges = {
        0: (0, 999999),
        2: (40, 60),
        3: (60, 500)
    }
    
    min_len, max_len = length_ranges.get(lv, (0, 999999))
    
    if _is_sqlite_db(file_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            for attempt in range(max_attempts):
                if lv == 0:
                    cursor.execute("""
                        SELECT sentence FROM sentences 
                        WHERE lang='eng' 
                        ORDER BY RANDOM() 
                        LIMIT 1
                    """)
                else:
                    cursor.execute("""
                        SELECT sentence FROM sentences 
                        WHERE lang='eng' 
                        AND LENGTH(sentence) >= ?
                        AND LENGTH(sentence) <= ?
                        ORDER BY RANDOM() 
                        LIMIT 1
                    """, (min_len, max_len))
                
                result = cursor.fetchone()
                
                if result and result[0]:
                    sentence = result[0].strip()
                    if not has_numbers(sentence):
                        if lv == 3 and ',' in sentence:
                            parts = [p.strip() for p in sentence.split(',', 1)]
                            if len(parts) == 2 and len(parts[0]) > 20 and len(parts[1]) > 20:
                                sentence = random.choice(parts)
                                if not sentence[-1] in '.!?':
                                    sentence += '.'
                        
                        conn.close()
                        return sentence
            
            conn.close()
            return "This is a fallback sentence without any numbers."
            
        except Exception as e:
            print(f"Error reading from SQLite DB {db_path}: {e}")
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Using fallback sentence.")
        return "This is a fallback sentence for testing purposes."
    
    try:
        if not hasattr(get_random_sentence_from_file, 'line_count'):
            print("Counting lines in TSV file...")
            get_random_sentence_from_file.line_count = get_file_line_count(file_path)
            print(f"File has {get_random_sentence_from_file.line_count} lines")
        
        total_lines = get_random_sentence_from_file.line_count
        
        for attempt in range(max_attempts):
            random_line = random.randint(1, total_lines)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if i == random_line:
                        try:
                            columns = line.strip().split('\t')
                            if len(columns) >= 3 and columns[2].strip():
                                sentence = columns[2].strip()
                                sentence_len = len(sentence)
                                
                                if lv != 0 and (sentence_len < min_len or sentence_len > max_len):
                                    break
                                
                                if not has_numbers(sentence):
                                    if lv == 3 and ',' in sentence:
                                        parts = [p.strip() for p in sentence.split(',', 1)]
                                        if len(parts) == 2 and len(parts[0]) > 20 and len(parts[1]) > 20:
                                            sentence = random.choice(parts)
                                            if not sentence[-1] in '.!?':
                                                sentence += '.'
                                    
                                    return sentence
                                break
                        except:
                            break
        
        return "This is a fallback sentence without any numbers."
        
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
        return "This is a fallback sentence due to file reading error."


def get_multiple_random_sentences(file_path="eng_sentences.tsv", count=30, max_attempts=100, lv=0):
    """
    Get multiple random sentences from TSV file or SQLite DB efficiently.
    Skip sentences containing numbers.
    For lv=1, return individual words instead of sentences.
    """
    # Special handling for lv=1: return words instead of sentences
    if lv == 1:
        words = get_random_words_from_db(file_path, count=count, max_attempts=max_attempts)
        return [word.capitalize() for word in words]
    
    db_path = _get_db_path(file_path)
    
    length_ranges = {
        0: (10, 200),
        2: (60, 120),
        3: (120, 250)
    }
    
    min_len, max_len = length_ranges.get(lv, (10, 200))
    
    if _is_sqlite_db(file_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            sentences = []
            attempts = 0
            fetch_count = min(count * 3, 200)
            
            while len(sentences) < count and attempts < max_attempts:
                cursor.execute("""
                    SELECT sentence FROM sentences 
                    WHERE lang='eng' 
                    AND LENGTH(sentence) >= ? 
                    AND LENGTH(sentence) <= ?
                    ORDER BY RANDOM() 
                    LIMIT ?
                """, (min_len, max_len, fetch_count))
                
                results = cursor.fetchall()
                
                for result in results:
                    if len(sentences) >= count:
                        break
                    
                    sentence = result[0].strip()
                    if (len(sentence) >= min_len and len(sentence) <= max_len and 
                        not has_numbers(sentence) and sentence not in sentences):
                        
                        if lv == 3 and ',' in sentence:
                            parts = [p.strip() for p in sentence.split(',', 1)]
                            if len(parts) == 2 and len(parts[0]) > 20 and len(parts[1]) > 20:
                                sentence = random.choice(parts)
                                if not sentence[-1] in '.!?':
                                    sentence += '.'
                        
                        sentences.append(sentence)
                
                attempts += 1
                if len(results) == 0:
                    break
            
            conn.close()
            
            while len(sentences) < count:
                sentences.append(f"This is fallback sentence {len(sentences) + 1} without numbers.")
            
            return sentences[:count]
            
        except Exception as e:
            print(f"Error reading multiple sentences from SQLite DB {db_path}: {e}")
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Using fallback sentences.")
        return [f"This is fallback sentence number {i+1} without numbers." for i in range(count)]
    
    try:
        if not hasattr(get_multiple_random_sentences, 'line_count'):
            print("Counting lines in TSV file...")
            get_multiple_random_sentences.line_count = get_file_line_count(file_path)
            print(f"File has {get_multiple_random_sentences.line_count} lines")
        
        total_lines = get_multiple_random_sentences.line_count
        random_lines = sorted(random.sample(range(1, total_lines + 1), min(count * 5, total_lines)))
        
        sentences = []
        current_target = 0
        attempts = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if current_target < len(random_lines) and i == random_lines[current_target]:
                    attempts += 1
                    if attempts > max_attempts:
                        break
                        
                    try:
                        columns = line.strip().split('\t')
                        if len(columns) >= 3 and columns[2].strip():
                            sentence = columns[2].strip()
                            if (len(sentence) > 10 and len(sentence) < 200 and 
                                not has_numbers(sentence)):
                                sentences.append(sentence)
                                if len(sentences) >= count:
                                    break
                    except:
                        pass
                    current_target += 1
        
        additional_attempts = 0
        while len(sentences) < count and additional_attempts < max_attempts:
            try:
                additional = get_random_sentence_from_file(file_path, max_attempts=5, lv=lv)
                if (additional not in sentences and len(additional) >= min_len and 
                    not has_numbers(additional)):
                    sentences.append(additional)
                additional_attempts += 1
            except:
                break
        
        while len(sentences) < count:
            sentences.append(f"This is fallback sentence {len(sentences) + 1} without numbers.")
        
        return sentences[:count]
        
    except Exception as e:
        print(f"Error reading multiple sentences from {file_path}: {e}")
        return [f"Fallback sentence {i+1} due to file reading error." for i in range(count)]


def generate_random_sentences_with_ipa(count=30, file_path="eng_sentences.tsv", lv=0):
    """Generate random sentences from TSV file or SQLite DB and convert words to IPA.
    Skip sentences containing numbers.
    For lv=1, generate individual words with IPA."""
    sentences_with_ipa = []
    
    sentences = get_multiple_random_sentences(file_path, count, lv=lv)
    print(f"Retrieved {len(sentences)} {'words' if lv == 1 else 'sentences'} from file (no numbers, level {lv})")
    
    for sentence in sentences:
        try:
            # For lv=1, sentence is actually a single word
            if lv == 1:
                clean_word = sentence.strip('.,!?;:"()[]{}')
                if clean_word:
                    try:
                        ipa = ipa_list(clean_word.lower())
                        if ipa:
                            sentences_with_ipa.append((sentence, [(clean_word, ipa[0])]))
                    except:
                        continue
            else:
                words = sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '').split()
                word_ipa_pairs = []
                
                for word in words:
                    try:
                        clean_word = word.strip('.,!?;:"()[]{}')
                        if clean_word:
                            ipa = ipa_list(clean_word.lower())
                            if ipa:
                                word_ipa_pairs.append((clean_word, ipa[0]))
                    except:
                        continue
                
                if word_ipa_pairs:
                    sentences_with_ipa.append((sentence, word_ipa_pairs))
                
        except Exception as e:
            continue
    
    return sentences_with_ipa


def count_ipa_sounds_in_sentence(word_ipa_pairs, target_ipa_sounds):
    """
    Count how many target IPA sounds appear in a sentence.
    """
    found_sounds = Counter()
    
    for word, ipa in word_ipa_pairs:
        for target_sound in target_ipa_sounds:
            if target_sound in ipa:
                found_sounds[target_sound] += ipa.count(target_sound)
    
    return found_sounds


def score_sentence(word_ipa_pairs, target_ipa_frequencies):
    """
    Score a sentence based on how well it matches target IPA sound frequencies.
    """
    if not target_ipa_frequencies:
        return 0
    
    found_sounds = count_ipa_sounds_in_sentence(word_ipa_pairs, target_ipa_frequencies)
    
    score = 0
    for sound, target_freq in target_ipa_frequencies.items():
        found_freq = found_sounds.get(sound, 0)
        if found_freq > 0:
            score += min(found_freq, target_freq)
    
    return score


def select_best_sentences(sentences_with_ipa, target_ipa_frequencies, top_n=10):
    """
    Select the best sentences based on IPA sound matching.
    """
    if not target_ipa_frequencies:
        return sentences_with_ipa
    
    scored_sentences = []
    
    for sentence, word_ipa_pairs in sentences_with_ipa:
        score = score_sentence(word_ipa_pairs, target_ipa_frequencies)
        scored_sentences.append((sentence, score, word_ipa_pairs))
    
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return scored_sentences[:top_n]


def generate_sentence(file_path="user-data.yaml", tsv_file_path="eng_sentences.tsv", lv=0):
    """
    Main function to generate a sentence based on user performance analysis.
    
    Args:
        file_path: Path to user data YAML file
        tsv_file_path: Path to TSV sentences file (will auto-convert to .db if exists)
        lv: Difficulty level (0=auto, 1=easy/word, 2=medium, 3=hard/long)
    
    Returns:
        str: Generated sentence without numbers, or single capitalized word for lv=1
    """
    data = load_user_data(file_path)
    wrong_ipa_counter, error_rate = analyze_last_20_nodes(data)
    
    print(f"Error rate: {error_rate:.1f}%")
    print(f"Wrong IPA sounds: {dict(wrong_ipa_counter)}")
    
    level_names = {0: 'auto', 1: 'word', 2: 'medium', 3: 'hard'}
    print(f"Difficulty level: {lv} ({level_names.get(lv, 'unknown')})")
    
    use_non_random = random.random() * 100 < error_rate
    
    if not use_non_random or not wrong_ipa_counter:
        print(f"Generating truly random {'word' if lv == 1 else 'sentence'}...")
        return get_random_sentence_from_file(tsv_file_path, lv=lv)
    
    else:
        print(f"Generating non-random {'word' if lv == 1 else 'sentence'} based on error patterns...")
        
        sentences_with_ipa = generate_random_sentences_with_ipa(30, tsv_file_path, lv=lv)
        print(f"Generated {len(sentences_with_ipa)} {'words' if lv == 1 else 'sentences'} with IPA (no numbers, level {lv})")
        
        if not sentences_with_ipa:
            return get_random_sentence_from_file(tsv_file_path, lv=lv)
        
        best_sentences = select_best_sentences(sentences_with_ipa, wrong_ipa_counter)
        
        if best_sentences:
            print("Top scored items:")
            for i, (sentence, score, _) in enumerate(best_sentences[:3]):
                print(f"{i+1}. Score: {score} - {sentence}")
            
            if len(best_sentences) > 1:
                sentences = [item[0] for item in best_sentences]
                scores = [item[1] for item in best_sentences]
                weights = [score + 1 for score in scores]
                selected_sentence = random.choices(sentences, weights=weights, k=1)[0]
            else:
                selected_sentence = best_sentences[0][0]
            
            return selected_sentence
        else:
            print("No items with matching IPA sounds, selecting randomly...")
            return random.choice([sentence for sentence, _ in sentences_with_ipa])


def main():
    """Main function for standalone execution."""
    print("=== Sentence Generator with IPA (No Numbers) ===")
    
    try:
        sentence = generate_sentence()
        print(f"\nGenerated sentence: {sentence}")
        
        if has_numbers(sentence):
            print("WARNING: Generated sentence contains numbers!")
        else:
            print("✓ Sentence contains no numbers")
        
        words = sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '').split()[:5]
        print("\nIPA for first few words:")
        for word in words:
            try:
                clean_word = word.strip('.,!?;:"()[]{}').lower()
                if clean_word:
                    ipa = ipa_list(clean_word)
                    if ipa:
                        print(f"  {clean_word}: {ipa[0]}")
            except:
                continue
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
