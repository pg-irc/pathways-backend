import re


def clean_up_newlines(text):
    text = remove_carriage_returns(text)
    text = remove_whitespace_before_newline(text)
    text = protect_newlines_around_markup(text)
    text = protect_newlines_around_numbered_list_items(text)
    text = replace_newlines_with_space(text)
    text = unprotect_newlines(text)
    return text


def remove_carriage_returns(text):
    carriage_return = r'\r'
    return re.sub(carriage_return, r'', text)


def remove_whitespace_before_newline(text):
    space_before_newline = r'[ \t\r]+\n'
    return re.sub(space_before_newline, r'\n', text)


def protect_newlines_around_markup(text):
    at_line_end = r'(\n[#\*\+\-\t ][^\n]+)\n'
    text = re.sub(at_line_end, r'\1NEWLINE_MARKER', text)

    at_text_start = r'^([#\*\+\-\t ][^\n]+)\n'
    text = re.sub(at_text_start, r'\1NEWLINE_MARKER', text)

    at_line_start = r'\n([#\*\+\-\t ][^\n]+\n)'
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
