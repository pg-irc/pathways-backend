import re


def clean_up_newlines(text):
    line_break = 'XXX_replace_this_with_single_newline_XXX'

    find_multiple_newline = r'[ \t\r]*\n([ \t\r]*\n)+[ \t\r]*'
    text = re.sub(find_multiple_newline, line_break, text)

    find_single_newline = r'[ \t\r]*\n[ \t\r]*'
    text = re.sub(find_single_newline, ' ', text)

    text = re.sub(line_break, '\n', text)

    return text


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    text = clean_up_links(text)
    return text
