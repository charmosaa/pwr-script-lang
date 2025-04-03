from collections import Counter
import re
import argparse
import json
import sys
import os

def get_stats(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    lines = content.splitlines()
    lines_total = len(lines)

    words = content.lower().split()
    word_counter = Counter(words)
    words_total = len(words)

    clean_content = re.sub(r"\s+", "", content)
    char_counter = Counter(clean_content)
    chars_total = len(clean_content)

    most_common_char = char_counter.most_common(1)[0] if char_counter else (None, 0)
    most_common_word = word_counter.most_common(1)[0] if word_counter else (None, 0)

    stats = {
        "file_path": file_path,
        "total_characters": chars_total,
        "total_words": words_total,
        "total_lines": lines_total,
        "most_common_character": most_common_char[0],
        "most_common_character_appearances": most_common_char[1],
        "most_common_word": most_common_word[0],
        "most_common_word_appearances": most_common_word[1]
    }
    
    return json.dumps(stats, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Text statistics command")
    parser.add_argument("path", help="Path to the txt file")

    args = parser.parse_args()

    # file not existing 
    if not os.path.isfile(args.path):
        sys.stderr.write(f"Error: File '{args.path}' does not exist or is not a valid file.\n")
        sys.exit(1)

    # correct file - print statistics
    sys.stdout.write(get_stats(args.path))

if __name__ == "__main__":
    main()
