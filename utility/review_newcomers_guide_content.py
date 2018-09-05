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
            if reply == 't' or reply == 'T':
                print('==== Reference file start ====')
                print(read_file_content(pair.reference_file))
                print('==== Reference file end ====\n\n')
                command = '{0} "{1}"'.format(args.editor, pair.target_file)
                os.system(command)

            elif reply == 'r' or reply == 'R':
                print('==== Target file start ====')
                print(read_file_content(pair.target_file))
                print('==== Target file end ====\n\n')
                command = '{0} "{1}"'.format(args.editor, pair.reference_file)
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
