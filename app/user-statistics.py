#!/usr/bin/env python3
"""
Công cụ phân tích và đánh giá dữ liệu phát âm từ user-data.yaml
"""

import yaml
import sys
from collections import Counter, defaultdict
import argparse


def analyze_pronunciation_data(yaml_file_path="user-data.yaml", keep_only_last_20=True):
    """
    Phân tích dữ liệu phát âm từ file YAML và đưa ra đánh giá, lời khuyên.
    
    Args:
        yaml_file_path (str): Đường dẫn đến file user-data.yaml
        keep_only_last_20 (bool): Có xóa các node thừa, chỉ giữ 20 node cuối không
        
    Returns:
        str: Kết quả phân tích dạng chuỗi nhiều dòng
    """
    
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        return f"Lỗi: Không tìm thấy file {yaml_file_path}"
    except yaml.YAMLError as e:
        return f"Lỗi đọc file YAML: {e}"
    
    if not data or len(data) < 20:
        return "Chưa đủ dữ liệu để đánh giá :("
    
    # Lấy 20 câu cuối cùng
    last_20_sentences = data[-20:]
    
    # Xóa các node thừa nếu được yêu cầu
    if keep_only_last_20 and len(data) > 20:
        try:
            with open(yaml_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(last_20_sentences, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
        except Exception as e:
            return f"Lỗi khi ghi file: {e}"
    
    # Tính điểm tổng thể (tỷ lệ câu đúng)
    correct_sentences = sum(1 for item in last_20_sentences if item.get('result', False))
    total_score = (correct_sentences / 20) * 10
    
    result_lines = []
    result_lines.append(f"=== BÁO CÁO PHÂN TÍCH PHÁT ÂM ===")
    result_lines.append(f"Điểm tổng thể: {total_score:.1f}/10")
    
    # Nếu điểm dưới 8.5, so sánh 10 câu đầu và 10 câu sau
    if total_score < 8.5:
        first_10 = last_20_sentences[:10]
        last_10 = last_20_sentences[10:]
        
        first_10_score = (sum(1 for item in first_10 if item.get('result', False)) / 10) * 10
        last_10_score = (sum(1 for item in last_10 if item.get('result', False)) / 10) * 10
        
        if last_10_score > first_10_score:
            result_lines.append("Có tiến bộ")
        elif last_10_score < first_10_score:
            result_lines.append("Bị giảm sút")
        else:
            result_lines.append("Ổn định")
    
    # Thu thập thống kê lỗi âm thanh
    ipa_errors = defaultdict(list)
    
    for sentence_data in last_20_sentences:
        if not sentence_data.get('result', True):  # Nếu câu sai
            wrong_words = sentence_data.get('wrong_words', [])
            for wrong_word in wrong_words:
                word = wrong_word.get('word', '')
                wrong_ipa_list = wrong_word.get('wrong_ipa', [])
                for ipa in wrong_ipa_list:
                    ipa_errors[ipa].append(word)
    
    # Đưa ra lời khuyên
    if ipa_errors:
        result_lines.append("\n=== LỜI KHUYÊN LUYỆN TẬP ===")
        result_lines.append("Bạn nên rèn luyện:")
        
        # Sắp xếp theo tần suất lỗi (nhiều nhất trước)
        sorted_ipa_errors = sorted(ipa_errors.items(), key=lambda x: len(x[1]), reverse=True)
        
        for ipa, words in sorted_ipa_errors:
            # Lấy tối đa 5 từ ví dụ và loại bỏ trùng lặp
            unique_words = list(dict.fromkeys(words))[:5]
            words_str = ", ".join(unique_words)
            result_lines.append(f"Âm {ipa} của các từ: {words_str}")
    else:
        result_lines.append("\nChúc mừng! Không có lỗi phát âm nào được phát hiện trong 20 câu gần nhất.")
    
    return "\n".join(result_lines)


def main():
    """Hàm main để chạy script từ command line"""
    parser = argparse.ArgumentParser(description='Phân tích dữ liệu phát âm từ user-data.yaml')
    parser.add_argument('--file', '-f', default='user-data.yaml', 
                       help='Đường dẫn đến file YAML (mặc định: user-data.yaml)')
    parser.add_argument('--no-delete', action='store_true',
                       help='Không xóa các node cũ, chỉ phân tích')
    
    args = parser.parse_args()
    
    result = analyze_pronunciation_data(args.file, keep_only_last_20=not args.no_delete)
    print(result)


if __name__ == "__main__":
    main()