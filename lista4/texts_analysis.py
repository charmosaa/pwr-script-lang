import sys
import os
import json
import subprocess
import argparse
from collections import Counter

def analyze_file(file_path):
    result = subprocess.run(
        ["python", "text_stats.py", file_path], 
        text=True, 
        capture_output=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    else: 
        print(f"Error processing {file_path}: {result.stderr}")
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
        stats = analyze_file(file_path)
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
    parser = argparse.ArgumentParser(description="Directory statistics command")
    parser.add_argument("directory", help="Path to the directory with txt files to analyze")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        sys.stderr.write(f"Error: Directory '{args.directory}' does not exist or is not a valid directory.\n")
        sys.exit(1)
    
    summary = analyze_directory(args.directory)
    print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    main()
