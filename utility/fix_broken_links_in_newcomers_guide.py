#!/home/rasmus/git/pathways-backend/.venv/bin/python

import os
import csv


def is_topic_file(path):
    sep = os.sep
    is_under_topics_folder = path.find(sep + 'topics' + sep) > 0
    is_mark_down = path.endswith('.md')
    return is_under_topics_folder and is_mark_down


def read_file_content(path):
    with open(path, 'r') as file:
        return file.read()


def write_file_content(path, content):
    with open(path, 'w') as file:
        return file.write(content)


def read_csv_data_from_file(csv_path):
    result = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            result.append(row)
    return result


fixed_links = read_csv_data_from_file('../content/Fix broken links in AA - urls.csv')


def fix_links_in_file(path):
    dirty = False
    content = read_file_content(path)
    for line in fixed_links:
        bad_link = line[0].strip()

        bad_link_with_http = bad_link.replace('https', 'http')
        bad_link_with_https = bad_link.replace('http', 'https')
        contains_bad_link = content.find(bad_link_with_http) or content.find(bad_link_with_https)

        good_link = line[2].strip()
        if contains_bad_link and good_link != 'OK':
            content = content.replace(bad_link_with_http, good_link)
            content = content.replace(bad_link_with_https, good_link)
            dirty = True
    if dirty:
        print(path)
        write_file_content(path, content)


def main():
    for root, _, filenames in os.walk('../content/NewcomersGuide/', topdown=False):
        for filename in filenames:
            path = os.path.join(root, filename)
            if is_topic_file(path):
                fix_links_in_file(path)


main()
