import sys

def get_just_content():
    in_preamble = True
    in_content = True
    in_info = False
    empty_lines = 0
    lines_total = 0
    result = ""  # Store processed content

    try:
        for line in sys.stdin:
            current_line = line.strip()
            lines_total += 1
            
            if in_info:  # Ignore everything in the last section
                continue

            if in_preamble: # Processing the preamble section
                if lines_total > 10:
                    in_preamble = False

                if current_line == "":
                    empty_lines += 1
                else:
                    if empty_lines > 1:             # 2 or more empty lines indicate content start
                        in_preamble = False
                        result = ""                 # we were in preamble so we ignore what we read so far
                    empty_lines = 0                 # reset empty line count

            if in_content:  # Processing content
                if current_line == "-----":  # Info section starts
                    in_content = False
                    in_info = True
                else:
                    if current_line == "":  # Only add a newline if it's a non-consecutive empty line
                        result += "\n"
                    else:
                        result += " ".join(current_line.split()) + "\n"  # Store cleaned line


    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    return result.strip()  # Return the final processed content

if __name__ == "__main__":
    content = get_just_content()  # Store the result
    print(content)  # Print all at once
