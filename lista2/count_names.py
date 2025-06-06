import sys

def count_names():
    sentences_with_names = 0
    current_names = 0
    all_sentences = 0
    in_sentence = False

    try:
        for line in sys.stdin:
            line = line.strip()

            if not line:
                if in_sentence:
                    all_sentences += 1
                    if current_names > 1:
                        sentences_with_names += 1
                    current_names = 0
                    in_sentence = False
                continue

            for word in line.split():
                in_sentence = True
                if(word[0].isupper()):
                    current_names += 1

                if word[-1] in ".!?":
                    all_sentences += 1
                    if current_names > 1:
                        sentences_with_names += 1
                    current_names = 0
                    in_sentence = False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return sentences_with_names, all_sentences


if __name__ == "__main__":
    name_sentences, sentences_all = count_names()
    print(f'Sentences with names: {name_sentences}')
    print(f'Sentences total: {sentences_all}')
    print(f'Percent: {name_sentences*100/sentences_all:.2f}%')

