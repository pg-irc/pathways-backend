import re


def clean_up_newlines(text):
    text = remove_carriage_returns(text)
    text = remove_whitespace_between_newlines(text)
    text = remove_whitespace_before_newline(text)
    text = protect_newlines_around_indentend_lines(text)
    text = protect_newlines_around_markup(text)
    text = protect_newlines_around_numbered_list_items(text)
    text = protect_multiple_newlines(text)
    text = replace_newlines_with_space(text)
    text = unprotect_newlines(text)
    return text


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
    text = re.sub(r'(\n){5}', r'NEWLINE_MARKERNEWLINE_MARKER', text)
    text = re.sub(r'(\n){4}', r'NEWLINE_MARKERNEWLINE_MARKER', text)
    text = re.sub(r'(\n){3}', r'NEWLINE_MARKERNEWLINE_MARKER', text)
    text = re.sub(r'(\n){2}', r'NEWLINE_MARKER', text)
    return text


def protect_newlines_around_indentend_lines(text):
    at_text_start = r'^([\t ][^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n([\t ][^\n]+\n)'
    text = re.sub(at_line_start, r'NEWLINE_MARKER\1', text)

    at_line_end = r'(NEWLINE_MARKER[\t ][^\n]+)\n'
    text = re.sub(at_line_end, r'\1NEWLINE_MARKER', text)

    return text


def protect_newlines_around_markup(text):
    at_line_end = r'(\n[#\*\+\-][^\n]+)\n'
    text = re.sub(at_line_end, r'\1NEWLINE_MARKER', text)

    at_text_start = r'^([#\*\+\-][^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n([#\*\+\-][^\n]+\n)'
    text = re.sub(at_line_start, r'NEWLINE_MARKER\1', text)

    return text


def protect_newlines_around_numbered_list_items(text):
    at_line_end = r'(\n\d+[\)\.][^\n]+)\n'
    text = re.sub(at_line_end, r'\1NEWLINE_MARKER', text)

    at_text_start = r'^(\d+[\)\.][^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n(\d+[\)\.])'
    text = re.sub(at_line_start, r'NEWLINE_MARKER\1', text)

    return text


def replace_newlines_with_space(text):
    # TODO protect all newlines so that this can be simplified
    single_newline_not_before_markup = r'([^\n])\n([^\n#\*\+\-\s])'
    return re.sub(single_newline_not_before_markup, r'\1 \2', text)


def unprotect_newlines(text):
    return re.sub(r'NEWLINE_MARKER', r'\n', text)


def clean_up_links(text):
    return re.sub(r'(https?://([a-zA-Z0-9\.\:]+)(/\S*)?)', r'[\2](\1)', text)


def clean_text(text):
    text = clean_up_newlines(text)
    text = clean_up_links(text)
    return text
