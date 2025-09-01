#!/usr/bin/env python3
"""
non-random-sentence.py

A script that generates sentences based on user performance analysis.
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
from wonderwords import RandomSentence
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


def generate_random_sentences_with_ipa(count=30):
    """Generate random sentences and convert words to IPA."""
    r = RandomSentence()
    sentences_with_ipa = []
    
    for _ in range(count):
        try:
            sentence = r.sentence()
            # Convert sentence to word-IPA pairs
            words = sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '').split()
            word_ipa_pairs = []
            
            for word in words:
                try:
                    # Clean word from punctuation
                    clean_word = word.strip('.,!?;:"()[]{}')
                    if clean_word:
                        ipa = ipa_list(clean_word.lower())
                        if ipa:
                            word_ipa_pairs.append((clean_word, ipa[0]))
                except:
                    # Skip words that cause IPA conversion errors
                    continue
            
            if word_ipa_pairs:  # Only add sentences with successful IPA conversions
                sentences_with_ipa.append((sentence, word_ipa_pairs))
                
        except Exception as e:
            # Skip sentences that cause errors
            continue
    
    return sentences_with_ipa


def count_ipa_sounds_in_sentence(word_ipa_pairs, target_ipa_sounds):
    """
    Count how many target IPA sounds appear in a sentence.
    
    Args:
        word_ipa_pairs: List of (word, ipa) tuples for the sentence
        target_ipa_sounds: Counter object with target IPA sounds
    
    Returns:
        Counter: IPA sounds found in this sentence
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
    
    Args:
        word_ipa_pairs: List of (word, ipa) tuples for the sentence
        target_ipa_frequencies: Counter with target IPA sound frequencies
    
    Returns:
        float: Score (higher is better match)
    """
    if not target_ipa_frequencies:
        return 0
    
    found_sounds = count_ipa_sounds_in_sentence(word_ipa_pairs, target_ipa_frequencies)
    
    score = 0
    for sound, target_freq in target_ipa_frequencies.items():
        found_freq = found_sounds.get(sound, 0)
        # Give points for each matching sound, with bonus for matching frequency
        if found_freq > 0:
            score += min(found_freq, target_freq)  # Don't over-reward excess sounds
    
    return score


def select_best_sentences(sentences_with_ipa, target_ipa_frequencies, top_n=10):
    """
    Select the best sentences based on IPA sound matching.
    
    Args:
        sentences_with_ipa: List of (sentence, word_ipa_pairs) tuples
        target_ipa_frequencies: Counter with target IPA sound frequencies
        top_n: Number of top sentences to return
    
    Returns:
        list: Top sentences with their scores
    """
    if not target_ipa_frequencies:
        return sentences_with_ipa
    
    scored_sentences = []
    
    for sentence, word_ipa_pairs in sentences_with_ipa:
        score = score_sentence(word_ipa_pairs, target_ipa_frequencies)
        scored_sentences.append((sentence, score, word_ipa_pairs))
    
    # Sort by score (descending) and take top_n
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return scored_sentences[:top_n]


def generate_sentence(file_path="user-data.yaml"):
    """
    Main function to generate a sentence based on user performance analysis.
    
    Args:
        file_path: Path to user data YAML file
    
    Returns:
        str: Generated sentence
    """
    # Load user data
    data = load_user_data(file_path)
    
    # Analyze last 20 nodes
    wrong_ipa_counter, error_rate = analyze_last_20_nodes(data)
    
    print(f"Error rate: {error_rate:.1f}%")
    print(f"Wrong IPA sounds: {dict(wrong_ipa_counter)}")
    
    # Determine if we should use non-random approach
    # Error rate becomes the probability of non-random sentence generation
    use_non_random = random.random() * 100 < error_rate
    
    if not use_non_random or not wrong_ipa_counter:
        # Generate truly random sentence
        print("Generating truly random sentence...")
        r = RandomSentence()
        return r.sentence()
    
    else:
        # Generate non-random sentence based on wrong IPA sounds
        print("Generating non-random sentence based on error patterns...")
        
        # Generate 30 random sentences with IPA
        sentences_with_ipa = generate_random_sentences_with_ipa(30)
        print(f"Generated {len(sentences_with_ipa)} sentences with IPA")
        
        if not sentences_with_ipa:
            # Fallback to random sentence if IPA conversion fails
            r = RandomSentence()
            return r.sentence()
        
        # Select best sentences based on IPA sound matching
        best_sentences = select_best_sentences(sentences_with_ipa, wrong_ipa_counter)
        
        if best_sentences:
            # Show scoring information
            print("Top scored sentences:")
            for i, (sentence, score, _) in enumerate(best_sentences[:3]):
                print(f"{i+1}. Score: {score} - {sentence}")
            
            # Randomly select from top sentences (weighted by score)
            if len(best_sentences) > 1:
                # Use weighted random selection favoring higher scores
                sentences = [item[0] for item in best_sentences]
                scores = [item[1] for item in best_sentences]
                
                # Add 1 to all scores to avoid zero weights
                weights = [score + 1 for score in scores]
                selected_sentence = random.choices(sentences, weights=weights, k=1)[0]
            else:
                selected_sentence = best_sentences[0][0]
            
            return selected_sentence
        else:
            # Fallback: select random sentence from generated ones
            print("No sentences with matching IPA sounds, selecting randomly...")
            return random.choice([sentence for sentence, _ in sentences_with_ipa])


def main():
    """Main function for standalone execution."""
    print("=== Non-Random Sentence Generator ===")
    
    try:
        sentence = generate_sentence()
        print(f"\nGenerated sentence: {sentence}")
        
        # Show IPA for words in the sentence (first few words)
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