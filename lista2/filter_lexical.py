import utils 

def lexical_order(sentence):
    words = sentence.lower().split()
    return words == sorted(words)


if __name__ == "__main__":
    sentences = utils.filter_sentences(lexical_order)
    print(sentences)