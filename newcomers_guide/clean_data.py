import re


def clean_up_newlines(text):
    text = remove_carriage_returns(text)
    text = remove_whitespace_between_newlines(text)
    text = remove_whitespace_before_newline(text)
    text = protect_newlines_around_indented_lines(text)
    text = protect_newlines_around_headings(text)
    text = protect_newlines_around_bullet_list_items(text)
    text = protect_newlines_around_numbered_list_items(text)
    text = protect_multiple_newlines(text)
    text = replace_newlines_with_space(text)
    return unprotect_newlines(text)


def remove_carriage_returns(text):
    carriage_return = r'\r'
    return re.sub(carriage_return, r'', text)


def remove_whitespace_between_newlines(text):
    whitespace_between_newlines = r'\n[ \t\r]+\n'
    return re.sub(whitespace_between_newlines, r'\n\n', text)


def remove_whitespace_before_newline(text):
    space_before_newline = r'[ \t\r]+\n'
    return re.sub(space_before_newline, r'\n', text)


def protect_multiple_newlines(text):
    three_or_more_newlines = r'(\n){3,}'
    text = re.sub(three_or_more_newlines, r'NEWLINE_MARKERNEWLINE_MARKER', text)

    two_newlines = r'(\n){2}'
    return re.sub(two_newlines, r'NEWLINE_MARKER', text)


def protect_newlines_around_indented_lines(text):
    at_text_start = r'^([\t ][^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n([\t ][^\n])'
    text = re.sub(at_line_start, r'NEWLINE_MARKER\1', text)

    at_line_end = r'(NEWLINE_MARKER[\t ][^\n]+)\n'
    return re.sub(at_line_end, r'\1NEWLINE_MARKER', text)


def protect_newlines_around_headings(text):
    at_text_start = r'^(#[^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n(#[^\n])'
    text = re.sub(at_line_start, r'NEWLINE_MARKER\1', text)

    at_line_end = r'(NEWLINE_MARKER#[^\n]+)\n'
    return re.sub(at_line_end, r'\1NEWLINE_MARKER', text)


def protect_newlines_around_bullet_list_items(text):
    last_bullet_list_item = r'([\*\+\-]([^\n]+\n)+)\n'
    text = re.sub(last_bullet_list_item, r'\1NEWLINE_MARKERNEWLINE_MARKER', text)

    at_line_start = r'\n([\*\+\-][^\n])'
    return re.sub(at_line_start, r'NEWLINE_MARKER\1', text)


def protect_newlines_around_numbered_list_items(text):
    last_bullet_list_item = r'(\d+[\.\)]([^\n]+\n)+)\n'
    text = re.sub(last_bullet_list_item, r'\1NEWLINE_MARKERNEWLINE_MARKER', text)

    at_line_start = r'\n(\d+[\.\)][^\n])'
    return re.sub(at_line_start, r'NEWLINE_MARKER\1', text)


def replace_newlines_with_space(text):
    return re.sub(r'\n', r' ', text)


def unprotect_newlines(text):
    return re.sub(r'NEWLINE_MARKER', r'\n', text)


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    return clean_up_links(text)
