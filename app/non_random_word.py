#!/usr/bin/env python3
"""
non-random-word.py

A script that generates words based on user performance analysis.
Now uses eng_sentences.tsv instead of wonderwords library.

Requirements:
- eng-to-ipa
- PyYAML

Install with: pip install eng-to-ipa PyYAML
"""

import yaml
import random
import os
import re
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


def get_file_line_count(file_path):
    """Get total number of lines in file efficiently."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f)
    except:
        return 1991044  # Default known count


def has_numbers(text):
    """Check if text contains any numbers (digits)."""
    return bool(re.search(r'\d', text))


def is_proper_noun(word):
    """Check if word is likely a proper noun (starts with capital letter)."""
    return word and word[0].isupper()


def get_words_from_tsv_sentence(file_path="eng_sentences.tsv"):
    """
    Get a sentence from TSV file and extract words (excluding proper nouns).
    
    Args:
        file_path: Path to the TSV file
    
    Returns:
        list: List of words (lowercase, no punctuation, no proper nouns)
    """
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Using fallback words.")
        return ["example", "sentence", "with", "sample", "words", "for", "testing"]
    
    try:
        # Get total line count (cache this if called frequently)
        if not hasattr(get_words_from_tsv_sentence, 'line_count'):
            print("Counting lines in TSV file...")
            get_words_from_tsv_sentence.line_count = get_file_line_count(file_path)
            print(f"File has {get_words_from_tsv_sentence.line_count} lines")
        
        total_lines = get_words_from_tsv_sentence.line_count
        
        # Generate random line number
        random_line = random.randint(1, total_lines)
        
        # Read the specific line
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if i == random_line:
                    try:
                        # Parse TSV line and get column C (index 2)
                        columns = line.strip().split('\t')
                        if len(columns) >= 3 and columns[2].strip():
                            sentence = columns[2].strip()
                            
                            # Skip sentences with numbers
                            if has_numbers(sentence):
                                return []  # Return empty to indicate we need to try again
                            
                            # Extract words from sentence
                            # Remove punctuation and split into words
                            cleaned_sentence = re.sub(r'[^\w\s]', ' ', sentence)
                            words = cleaned_sentence.split()
                            
                            # Filter out proper nouns and convert to lowercase
                            filtered_words = []
                            for word in words:
                                if word and not is_proper_noun(word) and len(word) > 1:
                                    filtered_words.append(word.lower())
                            
                            return filtered_words
                            
                    except Exception as e:
                        return []  # Return empty on error
        
        return []  # If line not found
        
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
        return ["fallback", "words", "due", "to", "file", "error"]


def collect_random_words_from_tsv(target_count=30, file_path="eng_sentences.tsv", max_attempts=50):
    """
    Collect random words from TSV file by extracting words from random sentences.
    
    Args:
        target_count: Number of words to collect
        file_path: Path to the TSV file
        max_attempts: Maximum attempts to avoid infinite loops
    
    Returns:
        list: List of random words
    """
    all_words = []
    attempts = 0
    
    while len(all_words) < target_count and attempts < max_attempts:
        words_from_sentence = get_words_from_tsv_sentence(file_path)
        
        if words_from_sentence:  # Only add if we got valid words
            all_words.extend(words_from_sentence)
        
        attempts += 1
    
    # Remove duplicates while preserving order
    unique_words = []
    seen = set()
    for word in all_words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)
    
    # Return exactly target_count words (or less if we couldn't collect enough)
    return unique_words[:target_count]


def generate_random_words_with_ipa(count=30, file_path="eng_sentences.tsv"):
    """Generate random words from TSV file and convert them to IPA."""
    words_with_ipa = []
    
    # Collect random words from TSV
    random_words = collect_random_words_from_tsv(count * 2, file_path)  # Get more than needed
    print(f"Collected {len(random_words)} words from TSV file")
    
    for word in random_words:
        try:
            ipa = ipa_list(word)
            if ipa:  # Only add if IPA conversion successful
                words_with_ipa.append((word, ipa[0]))  # Take first IPA variant
                if len(words_with_ipa) >= count:  # Stop when we have enough
                    break
        except Exception as e:
            # Skip words that cause errors in IPA conversion
            continue
    
    print(f"Successfully converted {len(words_with_ipa)} words to IPA")
    return words_with_ipa


def filter_words_by_ipa_sounds(words_with_ipa, target_ipa_sounds):
    """
    Filter words that contain target IPA sounds.
    
    Args:
        words_with_ipa: List of (word, ipa) tuples
        target_ipa_sounds: Counter object with IPA sounds and their frequencies
    
    Returns:
        dict: IPA sound -> list of words containing that sound
    """
    ipa_to_words = {}
    
    for ipa_sound in target_ipa_sounds:
        ipa_to_words[ipa_sound] = []
        
        for word, ipa in words_with_ipa:
            if ipa_sound in ipa:
                ipa_to_words[ipa_sound].append(word)
    
    return ipa_to_words


def select_words_by_frequency(ipa_to_words, ipa_frequencies):
    """
    Select words based on IPA sound frequencies.
    
    Args:
        ipa_to_words: dict mapping IPA sounds to lists of words
        ipa_frequencies: Counter with IPA sound frequencies
    
    Returns:
        list: Selected words
    """
    selected_words = []
    
    for ipa_sound, frequency in ipa_frequencies.items():
        available_words = ipa_to_words.get(ipa_sound, [])
        # Take min of frequency and available words
        words_to_take = min(frequency, len(available_words))
        if words_to_take > 0:
            selected_words.extend(random.sample(available_words, words_to_take))
    
    return selected_words


def get_random_word_from_tsv(file_path="eng_sentences.tsv"):
    """
    Get a single random word from TSV file.
    
    Args:
        file_path: Path to the TSV file
    
    Returns:
        str: Random word
    """
    words = collect_random_words_from_tsv(10, file_path)  # Get 10 words and pick one
    if words:
        return random.choice(words)
    else:
        return "fallback"


def generate_word(file_path="user-data.yaml", tsv_file_path="eng_sentences.tsv"):
    """
    Main function to generate a word based on user performance analysis.
    Now uses eng_sentences.tsv instead of wonderwords.
    
    Args:
        file_path: Path to user data YAML file
        tsv_file_path: Path to TSV sentences file
    
    Returns:
        str: Generated word
    """
    # Load user data
    data = load_user_data(file_path)
    
    # Analyze last 20 nodes
    wrong_ipa_counter, error_rate = analyze_last_20_nodes(data)
    
    print(f"Error rate: {error_rate:.1f}%")
    print(f"Wrong IPA sounds: {dict(wrong_ipa_counter)}")
    
    # Determine if we should use non-random approach
    # Error rate becomes the probability of non-random word generation
    use_non_random = random.random() * 100 < error_rate
    
    if not use_non_random or not wrong_ipa_counter:
        # Generate truly random word from TSV
        print("Generating truly random word from TSV...")
        return get_random_word_from_tsv(tsv_file_path)
    
    else:
        # Generate non-random word based on wrong IPA sounds
        print("Generating non-random word based on error patterns...")
        
        # Generate 30 random words with IPA from TSV
        words_with_ipa = generate_random_words_with_ipa(30, tsv_file_path)
        
        if not words_with_ipa:
            # Fallback to random word if IPA conversion fails
            return get_random_word_from_tsv(tsv_file_path)
        
        # Filter words by target IPA sounds
        ipa_to_words = filter_words_by_ipa_sounds(words_with_ipa, wrong_ipa_counter)
        
        # Select words based on frequency
        selected_words = select_words_by_frequency(ipa_to_words, wrong_ipa_counter)
        
        if selected_words:
            # Remove duplicates and select random word
            unique_words = list(set(selected_words))
            print(f"Selected words containing target sounds: {unique_words}")
            return random.choice(unique_words)
        else:
            # Fallback: select from any generated word if no matches found
            print("No words found with target IPA sounds, selecting from generated words...")
            return random.choice([word for word, _ in words_with_ipa])


def main():
    """Main function for standalone execution."""
    print("=== Non-Random Word Generator (TSV-based) ===")
    
    try:
        word = generate_word()
        print(f"\nGenerated word: {word}")
        
        # Show IPA for the generated word
        try:
            ipa = ipa_list(word)
            if ipa:
                print(f"IPA: {ipa[0]}")
        except:
            print("IPA: (conversion failed)")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()