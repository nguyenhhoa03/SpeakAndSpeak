#!/usr/bin/env python3
"""
non-random-word.py

A script that generates words based on user performance analysis.
Can be run standalone or imported into other scripts.

Requirements:
- wonderwords
- eng-to-ipa
- PyYAML

Install with: pip install wonderwords eng-to-ipa PyYAML
"""

import yaml
import random
from collections import Counter
from wonderwords import RandomWord
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


def generate_random_words_with_ipa(count=30):
    """Generate random words and convert them to IPA."""
    r = RandomWord()
    words_with_ipa = []
    
    for _ in range(count):
        try:
            word = r.word()
            ipa = ipa_list(word)
            if ipa:  # Only add if IPA conversion successful
                words_with_ipa.append((word, ipa[0]))  # Take first IPA variant
        except Exception as e:
            # Skip words that cause errors in IPA conversion
            continue
    
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
        selected_words.extend(random.sample(available_words, words_to_take))
    
    return selected_words


def generate_word(file_path="user-data.yaml"):
    """
    Main function to generate a word based on user performance analysis.
    
    Args:
        file_path: Path to user data YAML file
    
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
        # Generate truly random word
        print("Generating truly random word...")
        r = RandomWord()
        return r.word()
    
    else:
        # Generate non-random word based on wrong IPA sounds
        print("Generating non-random word based on error patterns...")
        
        # Generate 30 random words with IPA
        words_with_ipa = generate_random_words_with_ipa(30)
        print(f"Generated {len(words_with_ipa)} words with IPA")
        
        if not words_with_ipa:
            # Fallback to random word if IPA conversion fails
            r = RandomWord()
            return r.word()
        
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
    print("=== Non-Random Word Generator ===")
    
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