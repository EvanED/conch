from __future__ import print_function

def _divide(string):
    return _divide_into_paragraphs(string.split("\n"))

def _divide_into_paragraphs(lines):
    # Odd indices are whitespace
    # Even indices are non-whitespace
    paragraphs = []
    for line in lines:
        if line == "" or len(paragraphs) % 2 == 0:
            # start a new paragraph
            paragraphs.append([])
        paragraphs[-1].append(line)
    return paragraphs
