import sys
import os
import json
import subprocess
from collections import Counter

def run_analysis(file_path):
    result = subprocess.run(
        ["python", "text_stats.py",file_path], 
        text=True, 
        capture_output=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    else: 
        print(f"Error processing {file_path}: {e}")
        return None

def analyze_directory(directory):
    total_files = 0
    total_chars = 0
    total_words = 0
    total_lines = 0
    char_counter = Counter()
    word_counter = Counter()
    
    files = os.listdir(directory)

    for file in files:
        file_path = f"{directory}/{file}"
        stats = run_analysis(file_path)
        if stats:
            total_files += 1
            total_chars += stats["total_characters"]
            total_words += stats["total_words"]
            total_lines += stats["total_lines"]
            char_counter.update({stats["most_common_character"]: stats["most_common_character_appearances"]})
            word_counter.update({stats["most_common_word"]: stats["most_common_word_appearances"]})

    most_common_char = char_counter.most_common(1)[0] if char_counter else (None, 0)
    most_common_word = word_counter.most_common(1)[0] if word_counter else (None, 0)
    
    summary = {
        "total_files": total_files,
        "total_characters": total_chars,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_common_character": most_common_char[0],
        "most_common_character_appearances": most_common_char[1],
        "most_common_word": most_common_word[0],
        "most_common_word_appearances": most_common_word[1]
    }
    
    return summary

def main():
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Provided path is not a directory.")
        return
    
    summary = analyze_directory(directory)
    print(json.dumps(summary, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
