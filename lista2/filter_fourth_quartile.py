import sys
import numpy as np

def get_threshold():
    sentence = ""
    sentences = []
    lengths = []

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence.strip())      # strip trailing spaces
                    lengths.append(len(sentence.strip()))   # add length to the length list
                    sentence = ""
                continue                                    # skip empty lines

            for word in line.split():
                sentence += word + " "
                if word[-1] in ".!?":                       # find end of sentence
                    sentences.append(sentence.strip())      # strip trailing spaces
                    lengths.append(len(sentence.strip()))   # add length to the length list
                    sentence = ""

        if not lengths:  # if there are no sentences
            print("No valid sentences found.")
            return

        threshold = np.percentile(lengths, 75)

        for sentence in sentences:
            if len(sentence) >= threshold:
                print(sentence)

    except ValueError as e:
        print(f"Error processing input: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    get_threshold()
