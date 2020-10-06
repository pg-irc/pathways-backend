import csv


def parse(lines):
    reader = csv.reader(lines.split('\n'))
    header = reader.__next__()
    result = [{}]
    for row in reader:
        if not len(row):
            break
        result[-1]['id'] = row[0]
        result[-1]['name'] = row[1]
        result.append({})
    return result
