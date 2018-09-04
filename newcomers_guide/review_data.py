import re
import itertools


def compare_data(target_text, reference_text):
    differences = [compare_headings(target_text, reference_text),
                   compare_line_breaks(target_text, reference_text),
                   compare_paragraph_breaks(target_text, reference_text),
                   compare_bullets(target_text, reference_text),
                   compare_numbered_list_items(target_text, reference_text),
                   compare_urls(target_text, reference_text),
                   compare_emails(target_text, reference_text),
                   compare_phone_numbers(target_text, reference_text)]
    return '\n'.join(flatten(differences))


def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]


def compare_headings(target_text, reference_text):
    pattern = r'(^#)|(\n#)'
    data_type = 'headings'
    return compare_pattern_counts(pattern, data_type, target_text, reference_text)


def compare_line_breaks(target_text, reference_text):
    pattern = r'[ \t]{2,}\n[^\n]'
    data_type = 'line breaks'
    return compare_pattern_counts(pattern, data_type, target_text, reference_text)


def compare_paragraph_breaks(target_text, reference_text):
    pattern = r'\n{2,}'
    data_type = 'paragraph breaks'
    return compare_pattern_counts(pattern, data_type, target_text, reference_text)


def compare_bullets(target_text, reference_text):
    pattern = r'(^[*+-])|(\n[*+-])'
    data_type = 'bullets'
    return compare_pattern_counts(pattern, data_type, target_text, reference_text)


def compare_numbered_list_items(target_text, reference_text):
    pattern = r'(^\d+[\.\)])|(\n\d+[\.\)])'
    data_type = 'numbered list items'
    return compare_pattern_counts(pattern, data_type, target_text, reference_text)


def compare_pattern_counts(pattern, data_type, target_text, reference_text):
    target_count = count_instances(pattern, target_text)
    reference_count = count_instances(pattern, reference_text)
    if target_count != reference_count:
        message = 'contains {0} {1}, reference has {2}'
        return [message.format(target_count, data_type, reference_count)]
    return []


def count_instances(pattern, text):
    return len(re.findall(pattern, text))


def compare_urls(target_text, reference_text):
    pattern = r'https?[^ ]+'
    return compare_pattern_content(pattern, 'link', target_text, reference_text)


def compare_emails(target_text, reference_text):
    pattern = r'[^ \n]+@[^ \n]+'
    return compare_pattern_content(pattern, 'email address', target_text, reference_text)


def compare_phone_numbers(target_text, reference_text):
    pattern = r'\d[\d\- ]{5,}\d'
    return compare_pattern_content(pattern, 'phone number', target_text, reference_text)


def compare_pattern_content(pattern, data_type, target_text, reference_text):
    target_matches = re.findall(pattern, target_text)
    reference_matches = re.findall(pattern, reference_text)
    zipped_matches = itertools.zip_longest(target_matches, reference_matches)
    return [difference_message(data_type, target, reference) for target, reference in zipped_matches]


def difference_message(data_type, target, reference):
    if not reference:
        return 'extra {0} {1} is not there in the reference'.format(data_type, target)
    elif not target:
        return 'missing {0} {1}, it\'s there in the reference'.format(data_type, reference)
    elif target != reference:
        return 'contains {0} {1}, the reference has {2}'.format(data_type, target, reference)
    return ''
