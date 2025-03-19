import utils as utils

def questions_and_exclamations(sentence):
    return sentence[-1] in "?!"

if __name__ == "__main__":
    sentences = utils.filter_sentences(questions_and_exclamations)
    print(sentences)