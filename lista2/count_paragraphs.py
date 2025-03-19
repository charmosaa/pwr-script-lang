import utils

def count_paragraphs(_, previous_line_empty):
    if previous_line_empty:
        return 1
    return 0

if __name__ == "__main__":
    total = utils.count(count_paragraphs)
    print(f'Paragraphs: {total}')
