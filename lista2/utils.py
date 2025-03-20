import sys


# FILTERING
def filter_sentences(paradigm):
    sentences = ""
    current_sentence = ""

    try: 
        for line in sys.stdin:
            line = line.strip()

            if not line:                                            # check if end of paragraph - end of sentence
                if current_sentence:
                    if paradigm(current_sentence):                  # check conditions  
                        sentences += current_sentence + "\n"
                    current_sentence = ""
                continue

            for word in line.split():
                current_sentence += word + " "

                if word[-1] in ".!?":                               # check if end of sentence
                    if paradigm(current_sentence):                  # check conditions  
                        sentences += current_sentence + "\n"
                    current_sentence = ""                           # reset values for next sentence
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return sentences


# COUNTIG 
def count(paradigm):
    count = 0                   # result
    is_prev_empty = True        # previous line empty - for counting paragraphs

    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                try:
                    count += paradigm(line, is_prev_empty)          # increasing the count - depends on the paradigm
                except Exception as e:
                    print(f"Error processing line '{line}': {e}", file=sys.stderr)
                is_prev_empty = False                               # line not empty
            else:
                is_prev_empty = True                                # line empty
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return count

# SELECTING FIRST X SENTENCES
def get_first_x(max_num):
    current_sentence = ""
    num_sentences = 0
    result = ""                                                     # String to store the selected sentences

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                if num_sentences < max_num:                         # Check conditions
                    result += current_sentence + "\n"               # Store sentence

                if current_sentence:
                    num_sentences += 1                              # Increase sentence count
                    current_sentence = ""                           # Reset for next sentence
                continue

            for word in line.split():
                current_sentence += word + " "

                if word[-1] in ".!?":                               # Check if end of sentence
                    if num_sentences < max_num:                     # Check conditions
                        result += current_sentence + "\n"           # Store sentence

                    current_sentence = ""                           # Reset for next sentence
                    num_sentences += 1                              # Increase sentence count

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return result


# SELECT LONGEST SENTENCE
def get_longest():
    longest = ""
    current_sentence = ""

    try:
        for line in sys.stdin:
            line = line.strip()

            if not line:
                if len(current_sentence) > len(longest):        # if current is longer it's new solution
                    longest = current_sentence
                current_sentence = ""                           # reset values for next sentence
                continue
            for word in line.split():
                current_sentence += word + " "

                if word[-1] in ".!?":                               # check if end of sentence
                    if len(current_sentence) > len(longest):        # if current is longer it's new solution
                        longest = current_sentence
                    current_sentence = ""                           # reset values for next sentence

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return longest
