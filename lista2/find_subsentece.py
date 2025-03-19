import utils

def with_subsentences(sentence):
    return sentence.count(',') > 2

if __name__ == "__main__":
    sentences = utils.filter_sentences(with_subsentences)
    print(sentences)
    