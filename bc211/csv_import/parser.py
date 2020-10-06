import csv


def parse(lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    result = [{}]
    for values in reader:
        if not values:
            break
        for header, value in zip(headers, values):
            output_header = header_map.get(header, None)
            if output_header:
                result[-1][output_header] = value
        result.append({})
    return result


header_map = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
}
