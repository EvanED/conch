from __future__ import print_function

def _divide(string):
    return _divide_into_paragraphs(string.split("\n"))

def _divide_into_paragraphs(lines):
    # Odd indices are whitespace
    # Even indices are non-whitespace
    seen_paragraph_end = True
    paragraphs = [[]]
    for line in lines:
        if line != "" and seen_paragraph_end:
            # start a new paragraph
            paragraphs.append([])
            seen_paragraph_end = False
        if line == "":
            seen_paragraph_end = True
        paragraphs[-1].append(line)
    
    if len(paragraphs[0]) > 0:
        return paragraphs
    return paragraphs[1:]
