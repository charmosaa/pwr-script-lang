import utils

def not_same(sentence):
    previous_first_letter = ''
    for word in sentence.lower().split():
        if previous_first_letter and previous_first_letter == word[0]:
            return 0
        previous_first_letter = word[0]
    return 1


if __name__ == "__main__":
    sentences = utils.filter_sentences(not_same)
    print(sentences)