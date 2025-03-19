import sys

def get_just_content():
    in_preamble = True
    in_content = False
    in_info = False
    empty_lines = 0

    for line in sys.stdin:

        current_line = line.strip()

        if in_info:
            continue

        if in_preamble:
            if current_line == "":
                empty_lines += 1
                if empty_lines == 2:
                    in_preamble = False
                    in_content = True
            else:
                empty_lines = 0

        elif in_content:
            if current_line == "-----":
                in_content = False
                in_info = True
            else:
                print(" ".join(current_line.split()))
                if current_line == "":
                    print()

if __name__ == "__main__":
    get_just_content()
            