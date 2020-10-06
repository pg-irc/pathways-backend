import csv


def parse(lines):
    reader = csv.reader(lines.split('\n'))
    header = reader.__next__()
    result = [{}]
    for row in reader:
        if not len(row):
            break
        for column, value in zip(header, row):
            name = name_map.get(column, None)
            if name:
                result[-1][name] = value
        result.append({})
    return result


name_map = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
}
