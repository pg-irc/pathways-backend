import csv


def parse(lines):
    reader = csv.reader(lines.split('\n'))
    header = reader.__next__()
    result = {}
    for row in reader:
        if not len(row):
            break
        result['organization_id'] = row[0]
        result['organization_name'] = row[1]
    return result
