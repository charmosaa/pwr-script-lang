import utils

def count_sentences(line, *_):
    sentences_count = 0
    for word in line.split():
        if word[-1] in ".!?":
            sentences_count += 1
    return sentences_count

if __name__ == "__main__":
    total = utils.count(count_sentences)
    print(f'Total sentences: {total}')

