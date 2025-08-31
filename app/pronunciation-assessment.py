#!/usr/bin/env python3
"""
Pronunciation Assessment Tool

Đánh giá chi tiết phát âm từ và câu của người dùng bằng cách so sánh
câu gốc với kết quả Speech-to-Text.

Usage:
    python pronunciation-assessment.py
    
    Or import as module:
    from pronunciation_assessment import assess_pronunciation
"""

import re
import difflib
import yaml
import os
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import eng_to_ipa as ipa

@dataclass
class WordError:
    """Lưu thông tin lỗi của một từ"""
    word: str
    expected_ipa: str
    actual_ipa: str
    error_type: str
    ipa_differences: List[str]

class PronunciationAssessment:
    """Class chính để đánh giá phát âm"""
    
    def __init__(self, data_file="user-data.yaml"):
        self.word_errors = []
        self.data_file = data_file
        self.user_data = self._load_user_data()
    
    def _clean_text(self, text: str) -> str:
        """Làm sạch text, loại bỏ dấu câu và chuẩn hóa"""
        # Loại bỏ dấu câu và ký tự đặc biệt
        cleaned = re.sub(r'[^\w\s]', '', text.lower())
        # Chuẩn hóa khoảng trắng
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _get_ipa_pronunciation(self, word: str) -> str:
        """Chuyển từ sang IPA"""
        try:
            return ipa.convert(word)
        except Exception:
            return word  # Fallback nếu không convert được
    
    def _calculate_word_similarity(self, word1: str, word2: str) -> float:
        """Tính độ tương đồng giữa 2 từ"""
        return difflib.SequenceMatcher(None, word1.lower(), word2.lower()).ratio()
    
    def _calculate_ipa_similarity(self, ipa1: str, ipa2: str) -> float:
        """Tính độ tương đồng IPA giữa 2 từ"""
        return difflib.SequenceMatcher(None, ipa1, ipa2).ratio()
    
    def _find_ipa_differences(self, expected_ipa: str, actual_ipa: str) -> List[str]:
        """Tìm các âm IPA khác nhau"""
        differences = []
        matcher = difflib.SequenceMatcher(None, expected_ipa, actual_ipa)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                differences.append(f"'{expected_ipa[i1:i2]}' → '{actual_ipa[j1:j2]}'")
            elif tag == 'delete':
                differences.append(f"missing '{expected_ipa[i1:i2]}'")
            elif tag == 'insert':
                differences.append(f"extra '{actual_ipa[j1:j2]}'")
        
        return differences
    
    def _advanced_word_matching(self, original_words: List[str], spoken_words: List[str]) -> List[Tuple[int, int, float]]:
        """
        Thuật toán matching nâng cao để xử lý các trường hợp:
        - 1 từ thành 2 từ
        - 2 từ thành 1 từ  
        - Từ bị thiếu
        - Từ thừa
        """
        matches = []
        
        # Tạo ma trận similarity
        similarity_matrix = []
        for i, orig_word in enumerate(original_words):
            row = []
            for j, spoken_word in enumerate(spoken_words):
                # So sánh cả text và IPA
                text_sim = self._calculate_word_similarity(orig_word, spoken_word)
                ipa_sim = self._calculate_ipa_similarity(
                    self._get_ipa_pronunciation(orig_word),
                    self._get_ipa_pronunciation(spoken_word)
                )
                combined_sim = (text_sim + ipa_sim) / 2
                row.append(combined_sim)
            similarity_matrix.append(row)
        
        # Tìm best matches sử dụng dynamic programming approach
        used_spoken = set()
        used_original = set()
        
        # Tìm matches với threshold cao trước
        high_threshold = 0.7
        for i in range(len(original_words)):
            if i in used_original:
                continue
            best_j = -1
            best_score = 0
            
            for j in range(len(spoken_words)):
                if j in used_spoken:
                    continue
                if similarity_matrix[i][j] > best_score and similarity_matrix[i][j] >= high_threshold:
                    best_score = similarity_matrix[i][j]
                    best_j = j
            
            if best_j != -1:
                matches.append((i, best_j, best_score))
                used_original.add(i)
                used_spoken.add(best_j)
        
        # Xử lý cases phức tạp: 1 từ gốc match với nhiều từ spoken
        for i in range(len(original_words)):
            if i in used_original:
                continue
            
            # Thử combine 2-3 từ spoken liên tiếp
            for window_size in [2, 3]:
                for j in range(len(spoken_words) - window_size + 1):
                    if any(k in used_spoken for k in range(j, j + window_size)):
                        continue
                    
                    combined_spoken = ''.join(spoken_words[j:j+window_size])
                    combined_sim = self._calculate_word_similarity(original_words[i], combined_spoken)
                    
                    if combined_sim >= 0.6:
                        matches.append((i, j, combined_sim))
                        used_original.add(i)
                        for k in range(j, j + window_size):
                            used_spoken.add(k)
                        break
                else:
                    continue
                break
        
        # Xử lý remaining với threshold thấp hơn
        low_threshold = 0.4
        for i in range(len(original_words)):
            if i in used_original:
                continue
            best_j = -1
            best_score = 0
            
            for j in range(len(spoken_words)):
                if j in used_spoken:
                    continue
                if similarity_matrix[i][j] > best_score and similarity_matrix[i][j] >= low_threshold:
                    best_score = similarity_matrix[i][j]
                    best_j = j
            
            if best_j != -1:
                matches.append((i, best_j, best_score))
                used_original.add(i)
                used_spoken.add(best_j)
        
        return sorted(matches, key=lambda x: x[0])
    
    def _load_user_data(self) -> List[Dict]:
        """Tải dữ liệu user từ file YAML"""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or []
                return data
        except Exception as e:
            print(f"Warning: Could not load {self.data_file}: {e}")
            return []
    
    def _save_user_data(self):
        """Lưu dữ liệu user vào file YAML"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.user_data, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
        except Exception as e:
            print(f"Error saving to {self.data_file}: {e}")
    
    def _extract_wrong_ipa_sounds(self, error: WordError) -> List[str]:
        """Trích xuất các âm IPA bị sai từ WordError"""
        wrong_sounds = []
        
        for diff in error.ipa_differences:
            if '→' in diff:
                # Trường hợp thay thế: 'expected' → 'actual'
                parts = diff.split(' → ')
                if len(parts) == 2:
                    expected = parts[0].strip("'")
                    wrong_sounds.extend(list(expected))
            elif 'missing' in diff:
                # Trường hợp thiếu âm: missing 'sound'
                missing_sound = diff.split("'")[1] if "'" in diff else ""
                if missing_sound:
                    wrong_sounds.extend(list(missing_sound))
            elif 'extra' in diff:
                # Trường hợp thừa âm: extra 'sound'
                extra_sound = diff.split("'")[1] if "'" in diff else ""
                if extra_sound:
                    wrong_sounds.extend(list(extra_sound))
        
        # Loại bỏ các ký tự đặc biệt và khoảng trắng
        wrong_sounds = [sound for sound in wrong_sounds if sound.strip() and sound not in [' ', '\t', '\n']]
        
        # Loại bỏ duplicate nhưng giữ thứ tự
        seen = set()
        unique_sounds = []
        for sound in wrong_sounds:
            if sound not in seen:
                seen.add(sound)
                unique_sounds.append(sound)
        
        return unique_sounds
    
    def _save_assessment_result(self, original_text: str, spoken_text: str):
        """Lưu kết quả đánh giá vào user-data.yaml"""
        # Tạo entry mới
        wrong_words_data = []
        
        for error in self.word_errors:
            if error.error_type != "missing":  # Chỉ lưu từ bị phát âm sai, không lưu từ thiếu
                wrong_ipa_sounds = self._extract_wrong_ipa_sounds(error)
                if wrong_ipa_sounds:  # Chỉ thêm nếu có âm bị sai
                    wrong_words_data.append({
                        "word": error.word,
                        "wrong_ipa": wrong_ipa_sounds
                    })
        
        # Tạo node mới
        new_entry = {
            "sentence": original_text.strip(),
            "result": len(self.word_errors) == 0,  # True nếu không có lỗi
            "wrong_words": wrong_words_data
        }
        
        # Kiểm tra xem câu này đã tồn tại chưa
        existing_index = -1
        for i, entry in enumerate(self.user_data):
            if entry.get("sentence", "").strip().lower() == original_text.strip().lower():
                existing_index = i
                break
        
        if existing_index >= 0:
            # Cập nhật entry cũ
            self.user_data[existing_index] = new_entry
            print(f"Updated existing entry for: '{original_text[:50]}...'")
        else:
            # Thêm entry mới vào cuối
            self.user_data.append(new_entry)
            print(f"Added new entry for: '{original_text[:50]}...'")
        
        # Lưu vào file
        self._save_user_data()
    
    def _identify_word_errors(self, original_words: List[str], spoken_words: List[str]) -> List[WordError]:
        """Xác định các từ bị phát âm sai"""
        errors = []
        matches = self._advanced_word_matching(original_words, spoken_words)
        
        matched_original_indices = {match[0] for match in matches}
        
        for i, original_word in enumerate(original_words):
            if i not in matched_original_indices:
                # Từ bị thiếu hoàn toàn
                expected_ipa = self._get_ipa_pronunciation(original_word)
                errors.append(WordError(
                    word=original_word,
                    expected_ipa=expected_ipa,
                    actual_ipa="[missing]",
                    error_type="missing",
                    ipa_differences=[f"missing entire word '{expected_ipa}'"]
                ))
                continue
            
            # Tìm match tương ứng
            match = next(match for match in matches if match[0] == i)
            _, spoken_idx, similarity = match
            
            if similarity < 0.8:  # Threshold cho từ sai
                spoken_word = spoken_words[spoken_idx] if spoken_idx < len(spoken_words) else "[missing]"
                expected_ipa = self._get_ipa_pronunciation(original_word)
                actual_ipa = self._get_ipa_pronunciation(spoken_word) if spoken_word != "[missing]" else "[missing]"
                
                ipa_diffs = self._find_ipa_differences(expected_ipa, actual_ipa)
                
                error_type = "mispronounced"
                if similarity < 0.4:
                    error_type = "severely_mispronounced"
                
                errors.append(WordError(
                    word=original_word,
                    expected_ipa=expected_ipa,
                    actual_ipa=actual_ipa,
                    error_type=error_type,
                    ipa_differences=ipa_diffs
                ))
        
        return errors
    
    def assess_pronunciation(self, original_text: str, spoken_text: str, save_result: bool = True) -> str:
        """
        Hàm chính để đánh giá phát âm
        
        Args:
            original_text: Câu/từ gốc
            spoken_text: Kết quả từ Speech-to-Text
            save_result: Có lưu kết quả vào user-data.yaml không
            
        Returns:
            str: Kết quả đánh giá với câu được đánh dấu và chi tiết lỗi
        """
        # Làm sạch và tách từ
        original_clean = self._clean_text(original_text)
        spoken_clean = self._clean_text(spoken_text)
        
        original_words = original_clean.split()
        spoken_words = spoken_clean.split()
        
        # Tìm lỗi
        self.word_errors = self._identify_word_errors(original_words, spoken_words)
        
        # Lưu kết quả nếu được yêu cầu
        if save_result:
            self._save_assessment_result(original_text, spoken_text)
        
        # Tạo câu được đánh dấu
        marked_sentence = self._create_marked_sentence(original_text)
        
        # Tạo báo cáo chi tiết
        result = [marked_sentence]
        result.append("")  # Dòng trống
        
        if not self.word_errors:
            result.append("✅ Phát âm chính xác!")
            return "\n".join(result)
        
        result.append("❌ Các lỗi phát âm được phát hiện:")
        result.append("")
        
        for error in self.word_errors:
            result.append(f"🔸 Từ '{error.word}':")
            result.append(f"   Expected IPA: {error.expected_ipa}")
            result.append(f"   Actual IPA:   {error.actual_ipa}")
            result.append(f"   Error type:   {error.error_type}")
            if error.ipa_differences:
                result.append(f"   IPA differences: {', '.join(error.ipa_differences)}")
            result.append("")
        
        return "\n".join(result)
    
    def _create_marked_sentence(self, original_text: str) -> str:
        """Tạo câu được đánh dấu với từ sai"""
        words = original_text.split()
        error_words = {error.word.lower() for error in self.word_errors}
        
        marked_words = []
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in error_words:
                marked_words.append(f"**{word}**")
            else:
                marked_words.append(word)
        
        return " ".join(marked_words)
    
    def get_user_statistics(self) -> Dict:
        """Lấy thống kê từ dữ liệu user"""
        if not self.user_data:
            return {
                "total_assessments": 0,
                "correct_assessments": 0,
                "accuracy_rate": 0.0,
                "most_common_wrong_words": [],
                "most_common_wrong_sounds": []
            }
        
        total = len(self.user_data)
        correct = sum(1 for entry in self.user_data if entry.get("result", False))
        accuracy_rate = (correct / total) * 100 if total > 0 else 0
        
        # Thống kê từ sai nhiều nhất
        wrong_words_count = {}
        wrong_sounds_count = {}
        
        for entry in self.user_data:
            for wrong_word in entry.get("wrong_words", []):
                word = wrong_word.get("word", "")
                if word:
                    wrong_words_count[word] = wrong_words_count.get(word, 0) + 1
                
                for sound in wrong_word.get("wrong_ipa", []):
                    wrong_sounds_count[sound] = wrong_sounds_count.get(sound, 0) + 1
        
        # Sắp xếp theo tần suất
        most_common_words = sorted(wrong_words_count.items(), key=lambda x: x[1], reverse=True)[:10]
        most_common_sounds = sorted(wrong_sounds_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_assessments": total,
            "correct_assessments": correct,
            "accuracy_rate": round(accuracy_rate, 2),
            "most_common_wrong_words": most_common_words,
            "most_common_wrong_sounds": most_common_sounds
        }
    
    def print_user_statistics(self):
        """In thống kê user ra console"""
        stats = self.get_user_statistics()
        
        print("\n" + "="*50)
        print("📊 THỐNG KÊ PHÁT ÂM CỦA USER")
        print("="*50)
        print(f"Tổng số lần kiểm tra: {stats['total_assessments']}")
        print(f"Số lần đúng: {stats['correct_assessments']}")
        print(f"Tỷ lệ chính xác: {stats['accuracy_rate']}%")
        print()
        
        if stats['most_common_wrong_words']:
            print("🔴 Từ phát âm sai nhiều nhất:")
            for word, count in stats['most_common_wrong_words']:
                print(f"   • {word}: {count} lần")
            print()
        
        if stats['most_common_wrong_sounds']:
            print("🔴 Âm IPA sai nhiều nhất:")
            for sound, count in stats['most_common_wrong_sounds']:
                print(f"   • /{sound}/: {count} lần")
        
        print("="*50)


def assess_pronunciation(original_text: str, spoken_text: str, save_result: bool = True) -> str:
    """
    Hàm wrapper để dễ import và sử dụng
    
    Args:
        original_text: Câu/từ gốc
        spoken_text: Kết quả từ Speech-to-Text
        save_result: Có lưu kết quả vào user-data.yaml không
        
    Returns:
        str: Kết quả đánh giá chi tiết
    """
    assessor = PronunciationAssessment()
    return assessor.assess_pronunciation(original_text, spoken_text, save_result)


def main():
    """Chương trình chính để test"""
    print("=== Pronunciation Assessment Tool ===")
    print()
    
    assessor = PronunciationAssessment()
    
    # Test cases
    test_cases = [
        ("I would like a cup of coffee, please.", "I wood like a cup of coffe please"),
        ("The weather is beautiful today.", "The wether is butiful today"),
        ("She sells seashells by the seashore.", "She sells seeshells by the seeshore"),
        ("Hello world", "Hello word"),
        ("Good morning", "Good morening"),
    ]
    
    print("🧪 Running test cases...")
    for i, (original, spoken) in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Original: {original}")
        print(f"Spoken:   {spoken}")
        print()
        
        result = assessor.assess_pronunciation(original, spoken)
        print(result)
        print("="*60)
    
    # Hiển thị thống kê
    assessor.print_user_statistics()
    
    # Interactive mode
    while True:
        print("\n🎤 Interactive Mode")
        print("Options:")
        print("1. Assess pronunciation")
        print("2. View statistics")
        print("3. Exit")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            original = input("\nEnter original text: ").strip()
            if not original:
                continue
                
            spoken = input("Enter spoken text (from Speech-to-Text): ").strip()
            if not spoken:
                continue
                
            print("\n" + "="*50)
            result = assessor.assess_pronunciation(original, spoken)
            print(result)
            print("="*50)
            
        elif choice == '2':
            assessor.print_user_statistics()
            
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please choose 1-3.")


if __name__ == "__main__":
    main()