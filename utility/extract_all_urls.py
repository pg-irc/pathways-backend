#!/home/rasmus/git/pathways-backend/.venv/bin/python

# ./utility/extract_all_urls.py | sort | uniq > urls.txt

import os
import re


def is_topic_file(path):
    sep = os.sep
    is_under_topics_folder = path.find(sep + 'topics' + sep) > 0
    is_mark_down = path.endswith('.md')
    return is_under_topics_folder and is_mark_down


def read_file_content(path):
    with open(path, 'r') as file:
        return file.read()


def extract_urls(path):
    content = read_file_content(path)
    # TODO ensure the same pattern is used in /pathways-backend/newcomers_guide/clean_data.py
    pattern = re.compile(r'(https?://[a-zA-Z][a-zA-Z0-9\.\-\_\?\&\$\#\/]+[a-zA-Z0-9\-\_\?\&\$\#\/])')
    for match in re.finditer(pattern, content):
        print(match.group(1))


def main():
    folder = '../content/NewcomersGuide/'
    for root, _, filenames in os.walk(folder, topdown=False):
        for filename in filenames:
            path = os.path.join(root, filename)
            if is_topic_file(path):
                extract_urls(path)


main()
