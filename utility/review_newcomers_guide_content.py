#!/usr/bin/python3

import argparse
import os
import sys
import review_data


def main():
    args = parse_command_line()
    files = find_files(args.path)
    files = review_data.partition_files(args.reference_language, args.target_language, files)
    for pair in files:
        diff = review_data.compare_data(read_file_content(pair.target_file),
                                        read_file_content(pair.reference_file))
        if diff != '':
            print(
                (
                    'Reviewing file {0}\nReference is   {1}:\n\nDifferences:\n{2}\n\n'
                    'T: Edit target file; R: Edit reference file; N: Go to next file (T/R/N): '
                ).format(
                    pair.target_file, pair.reference_file, diff
                )
            )
            reply = sys.stdin.readline().strip()
            if reply in ('t', 'T'):
                edit_target_file(args, pair)

            elif reply in ('r', 'R'):
                edit_reference_file(args, pair)


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


def read_file_content(path):
    with open(path, 'r') as file:
        return file.read()


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
