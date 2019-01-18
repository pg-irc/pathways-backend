#!/usr/bin/python3

import argparse
import os
import sys
import review_data


def main():
    args = parse_command_line()
    files = find_files(args.path)
    files = review_data.partition_files(args.reference_language, args.target_language, files)

    current_pair_index = 0
    history = []
    while current_pair_index < len(files):
        pair = files[current_pair_index]
        current_pair_index += 1
        diff = review_data.compare_data(read_file_content(pair.target_file),
                                        read_file_content(pair.reference_file))
        if diff == '':
            print('.', end='')
        else:
            history.append(current_pair_index - 1)
            print(
                (
                    '\n'
                    'Reviewing file ({3}/{4}) {0}\nReference is   {1}:\n\nDifferences:\n{2}\n\n'
                    'T: Edit target file; '
                    'R: Edit reference file; '
                    'P: Fix phone numbers; '
                    'B: Go to back to previous file; '
                    'N: Go to next file (t/r/p/b/N): '
                ).format(
                    pair.target_file, pair.reference_file, diff, current_pair_index-1, len(files)
                )
            )
            reply = sys.stdin.readline().strip()
            if reply in ('t', 'T'):
                edit_target_file(args, pair)

            elif reply in ('r', 'R'):
                edit_reference_file(args, pair)

            elif reply in ('p', 'P'):
                fix_phone_numbers_in_target_file(pair)

            elif reply in ('b', 'B'):
                current_pair_index = pop_from(history)


def pop_from(history):
    if len(history) < 2:
        return 0
    history.pop()
    return history.pop()


def edit_target_file(args, pair):
    edit_file(args.editor, pair.target_file, pair.reference_file, 'Reference')


def edit_reference_file(args, pair):
    edit_file(args.editor, pair.reference_file, pair.target_file, 'Target')


def edit_file(editor, file_to_edit, file_to_compare, file_to_compare_label):
    print('==== {} file start ===='.format(file_to_compare_label))
    print(read_file_content(file_to_compare))
    print('==== {} file end ====\n\n'.format(file_to_compare_label))
    command = '{0} "{1}"'.format(editor, file_to_edit)
    os.system(command)


def fix_phone_numbers_in_target_file(pair):
    reference_text = read_file_content(pair.reference_file)
    target_text = read_file_content(pair.target_file)
    phone_mismatches = review_data.compute_phone_number_mismatches(target_text, reference_text)
    dirty = False
    for target_phone, reference_phone in phone_mismatches:
        print('Target has        "{}",'.format(target_phone))
        print('but reference has "{}",'.format(reference_phone))
        print('replace phone number in target text with phone number from reference? (y/N):')
        reply = sys.stdin.readline().strip()
        if reply in ('y', 'Y'):
            target_text = target_text.replace(target_phone, reference_phone)
            dirty = True
    if dirty:
        print('==== Updated file start ====')
        print(target_text)
        print('==== Updated file end ====\n')
        print('Update the file on disk? (y/N):')
        reply = sys.stdin.readline().strip()
        if reply in ('y', 'Y'):
            write_file_content(pair.target_file, target_text)


def read_file_content(path):
    with open(path, 'r') as file:
        return file.read()


def write_file_content(path, content):
    with open(path, 'w') as file:
        file.write(content)


def find_files(root_dir):
    files = {}
    for root, _, filenames in os.walk(root_dir, topdown=False):
        files[root] = []
        for filename in filenames:
            files[root].append(filename)
    return files


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the files to review')
    parser.add_argument('-r', '--reference_language', default='en', help='the reference language')
    parser.add_argument('-t', '--target_language', help='the target language')
    parser.add_argument('-e', '--editor', default='gedit', help='the editor to use to fix issues in content files')
    return parser.parse_args()


main()
