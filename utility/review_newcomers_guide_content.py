#!/usr/bin/python3

import argparse
import os
import review_data


def main():
    args = parse_command_line()
    files = find_files(args.path)
    files = review_data.partition_files(args.reference_language, args.target_language, files)
    for pair in files:
        diff = review_data.compare_data(read_file_content(pair.reference_file),
                                        read_file_content(pair.target_file))
        if diff != '':
            print(
                '\ntarget =    {0}\nreference = {1}:\n\nThe target {2}'.format(
                    pair.target_file, pair.reference_file, diff
                )
            )


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
    return parser.parse_args()


main()
