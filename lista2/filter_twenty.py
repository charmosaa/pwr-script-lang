import utils
import sys

if __name__ == "__main__":  
    sentences = utils.get_first_x(20, sys.stdin)
    print(sentences)