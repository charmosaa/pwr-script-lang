import utils

def count_chars(line, *_):
    return len(line.replace(" ", ""))


if __name__ == "__main__":
    total = utils.count(count_chars)
    print(f'Chars: {total}')
