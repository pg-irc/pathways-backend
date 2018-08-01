import re


def clean_up_newlines(text):
    find_heading_at_the_start = r'^(\#[^\n]+)'
    text = re.sub(find_heading_at_the_start, r'\g<1>\n\n', text)

    find_heading_after_newline = r'(\n[ \t\r]*\#[^\n]+)'
    text = re.sub(find_heading_after_newline, r'\g<1>\n\n', text)

    find_bullet_character = r'\•'
    text = re.sub(find_bullet_character, '*', text)

    find_bullet = r'(\n[ \r\t]*\*)'
    text = re.sub(find_bullet, '\n\n*', text)

    line_break_marker = 'XXX_linebreak_XXX'

    find_multiple_newlines = r'[ \t\r]*\n([ \t\r]*\n)+[ \t\r]*'
    text = re.sub(find_multiple_newlines, line_break_marker, text)

    find_single_newline = r'[ \t\r]*\n[ \t\r]*'
    text = re.sub(find_single_newline, ' ', text)

    text = re.sub(line_break_marker, '\n\n', text)

    return text


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    text = clean_up_links(text)
    return text
