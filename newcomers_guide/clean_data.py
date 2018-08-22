import re


def clean_up_newlines(text):

    find_carriage_return = r'\r'
    text = re.sub(find_carriage_return, r'', text)

    find_space_before_newline = r'[ \t\r]+\n'
    text = re.sub(find_space_before_newline, r'\n', text)

    find_newline_not_before_markup = r'([^\n])\n([^#\*\+\-\s\n])'
    text = re.sub(find_newline_not_before_markup, r'\1 \2', text)

    return text


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    text = clean_up_links(text)
    return text
