import re


def clean_up_newlines(text):

    carriage_return = r'\r'
    text = re.sub(carriage_return, r'', text)

    space_before_newline = r'[ \t\r]+\n'
    text = re.sub(space_before_newline, r'\n', text)

    line_starting_with_markup = r'(\n[#\*\+\-\t ][^\n]+)\n'
    text = re.sub(line_starting_with_markup, r'\1NEWLINE_MARKER', text)

    first_line_with_markup = r'^([#\*\+\-\t ][^\n]+)\n'
    text = re.sub(first_line_with_markup, r'\1NEWLINE_MARKER', text)

    single_newline_not_before_markup = r'([^\n])\n([^\n#\*\+\-\s])'
    text = re.sub(single_newline_not_before_markup, r'\1 \2', text)

    text = re.sub(r'NEWLINE_MARKER', r'\n', text)

    return text


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    text = clean_up_links(text)
    return text
