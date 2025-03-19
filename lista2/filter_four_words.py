import utils as utils

def max_four_words(sentence):
    return len(sentence.split(" ")) <= 4
    

if __name__ == "__main__":
    sentences = utils.filter_sentences(max_four_words)
    print(sentences)