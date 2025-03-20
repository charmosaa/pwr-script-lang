import sys

def get_just_content():
    in_preamble = True
    in_content = False
    in_info = False
    empty_lines = 0

    try:
        for line in sys.stdin:

            current_line = line.strip()

            if in_info:                                         # ignore everything in the last section
                continue

            if in_preamble:                                     # processing the preamble section
                if current_line == "":
                    empty_lines += 1
                else:
                    if empty_lines > 1:                         # two or more empty lines indicate content start
                        in_preamble = False
                        in_content = True
                    empty_lines = 0                             # reset empty line count

            if in_content:                                      # processing content 
                if current_line == "-----":                     # info section starts
                    in_content = False
                    in_info = True
                else:
                    print(" ".join(current_line.split()))       # remove extra spaces
                    if current_line == "":
                        print()                                 # paragraph breaks as it was

    # potential errors handling 
    except EOFError:
        print("Error: Unexpected end of input.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_just_content()
