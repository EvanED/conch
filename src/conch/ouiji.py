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

_next_paragraph_id = 1
class Paragraph(object):
    def __init__(self, lines, style):
        global _next_paragraph_id
        self._lines = lines
        self._style = style
        self._id_number = _next_paragraph_id
        _next_paragraph_id += 1

    def get_style(self):
        return self._style

    def get_lines(self):
        return self._lines

    def get_id(self):
        return "paragraph{}".format(self._id_number)


def styleize_output(output_string):
    return [Paragraph(lines, "mono")
            for lines in _divide_into_paragraphs(output_string)]
