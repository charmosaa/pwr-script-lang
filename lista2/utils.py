import sys

def filter_text(filter_func, text):
    sentences = ""
    current_sentence = ""

    for line in text:
        line = line.strip()

        for word in line.split():
            current_sentence += word + " "

            if word[-1] in ".!?":                               # check if end of sentence
                if filter_func(current_sentence.rstrip()):      # check if current sentence fullfils filter conditions  
                    sentences += current_sentence
                
                current_sentence = ""                           # reset values for next sentence

    return sentences

def filter_sentences(filter_func):
    sentences = ""
    current_sentence = ""

    for line in sys.stdin:
        line = line.strip()

        for word in line.split():
            current_sentence += word + " "

            if word[-1] in ".!?":                               # check if end of sentence
                if filter_func(current_sentence.rstrip()):      # check if current sentence fullfils filter conditions  
                    sentences += current_sentence
                
                current_sentence = ""                           # reset values for next sentence

    return sentences

def count(paradigm):
    count = 0
    is_empty = True
    current_names = [0]
    for line in sys.stdin:
        line = line.strip()
        if line:
            count += paradigm(line, is_empty)
        else:
            is_empty = True
    return count

def get_first_x(max_num, text):
    sentences = ""
    current_sentence = ""
    num_sentences = 0

    for line in text:
        line = line.strip()
        for word in line.split():
            current_sentence += word + " "

            if word[-1] in ".!?":                               # check if end of sentence
                if num_sentences < max_num: 
                    sentences += current_sentence

                current_sentence = ""                           # reset values for next sentence
                num_sentences += 1

    return sentences

def get_longest(text):
    longest = ""
    current_sentence = ""

    for line in text:
        line = line.strip()
        for word in line.split():
            current_sentence += word + " "

            if word[-1] in ".!?":                               # check if end of sentence
                if len(current_sentence) > len(longest):        # if current is longer it's new solution
                    longest = current_sentence

                current_sentence = ""                           # reset values for next sentence

    return longest


def count_sentences():
    sentences = 0

    for line in sys.stdin:
        line = line.strip()

        if line == "":
            continue

        for word in line.split():
            if word[-1] == "." or word[-1] == "?" or word[-1] == "!":
                sentences += 1

    return sentences


