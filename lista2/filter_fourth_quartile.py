import sys
import numpy as np

def get_threshold():
    sentence = ""
    sentences = []
    lengths = []
    for line in sys.stdin:
        line = line.strip()
        for word in line.split():
            sentence += word + " "
            if word[-1] in ".!?":
                sentences.append(sentence)
                lengths.append(len(sentence))
                sentence = ""

    threshold = np.percentile(lengths, 75)
    
    for sentence in sentences:
        if len(sentence) >= threshold:
            print(sentence)


if __name__ == "__main__":
    get_threshold()