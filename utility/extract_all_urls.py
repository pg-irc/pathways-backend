# PYTHONPATH=. python ./utility/extract_all_urls.py | sort | uniq > urls.txt

import re
import os
from newcomers_guide.read_data import is_topic_file, read_file_content
from newcomers_guide.link_regular_expression import url_regular_expression


def extract_urls(path):
    content = read_file_content(path)
    pattern = re.compile(url_regular_expression)
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
