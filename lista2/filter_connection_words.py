import utils

def connection_words(sentence):
    connection_words = ["i", "oraz", "że", "lub", "ale"]        # words that we are looking for
    current_connection_words = 0

    for word in sentence.split():
        if word.lower() in connection_words:
            current_connection_words += 1

    return current_connection_words > 1                         # if at least 2 it fulfills the conditions

if __name__ == "__main__":
    sentences = utils.filter_sentences(connection_words)
    print(sentences)