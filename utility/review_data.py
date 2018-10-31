import re
import os
from itertools import zip_longest


class ReviewPair:
    def __init__(self, reference_file, target_file):
        self.reference_file = reference_file
        self.target_file = target_file


def partition_files(reference_language, target_language, file_map):
    result = []
    for path in file_map:
        reference_file = None
        target_file = None
        for filename in file_map[path]:
            if filename.startswith(reference_language + '.'):
                reference_file = path + os.sep + filename
            if filename.startswith(target_language + '.'):
                target_file = path + os.sep + filename
        if reference_file and target_file:
            result.append(ReviewPair(reference_file, target_file))
    return result


def compare_data(target_text, reference_text):
    differences = [compare_headings(target_text, reference_text),
                   compare_line_breaks(target_text, reference_text),
                   compare_paragraph_breaks(target_text, reference_text),
                   compare_bullets(target_text, reference_text),
                   compare_numbered_list_items(target_text, reference_text),
                   compare_urls(target_text, reference_text),
                   compare_emails(target_text, reference_text),
                   compare_phone_numbers(target_text, reference_text)]
    return '\n'.join(flatten(differences)).strip()


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
    pattern = r'https?[^\s]+[a-zA-Z]'
    return compare_pattern_content(pattern, 'link', target_text, reference_text)


def compare_emails(target_text, reference_text):
    pattern = r'[^ \n]+@[^ \n]+'
    return compare_pattern_content(pattern, 'email address', target_text, reference_text)


PHONE_NUMBER_PATTERN = r'\d[\d\- ]{5,}\d'


def compare_phone_numbers(target_text, reference_text):
    return compare_pattern_content(PHONE_NUMBER_PATTERN, 'phone number',
                                   target_text, reference_text)


def compare_pattern_content(pattern, data_type, target_text, reference_text):
    zipped_matches = compute_pattern_mismatches(pattern, target_text, reference_text)
    return [difference_message(data_type, target, reference) for target, reference in zipped_matches]


def compute_pattern_mismatches(pattern, target_text, reference_text):
    target_matches = re.findall(pattern, target_text)
    reference_matches = re.findall(pattern, reference_text)
    return zip_longest(target_matches, reference_matches)


def compute_phone_number_mismatches(target_text, reference_text):
    return compute_pattern_mismatches(PHONE_NUMBER_PATTERN, target_text, reference_text)


def difference_message(data_type, target, reference):
    if not reference:
        return 'extra {0} {1} is not there in the reference'.format(data_type, target)

    if not target:
        return 'missing {0} {1}, it\'s there in the reference'.format(data_type, reference)

    https = re.compile('^https')
    target = https.sub('http', target)
    reference = https.sub('http', reference)

    if target != reference:
        target_line = 'contains {} '.format(data_type)
        reference_line = 'the reference has '
        longest = max(len(target_line), len(reference_line))
        target_line = target_line.ljust(longest) + target
        reference_line = reference_line.ljust(longest) + reference
        return target_line + '\n' + reference_line + '\n'

    return ''
