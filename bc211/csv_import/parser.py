import csv
import re


def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    for row in reader:
        organization = {}
        phone_numbers = [{}]
        last_phone_index = 0
        if not row:
            break
        for header, value in zip(headers, row):
            output_header = organization_header_map.get(header, None)
            output_phone_header = phone_header_map.get(phone_header_with_index_one(header), None)
            current_phone_index = get_zero_based_phone_index(header)
            if current_phone_index and last_phone_index != current_phone_index:
                last_phone_index = current_phone_index
                while len(phone_numbers) <= current_phone_index:
                    phone_numbers.append({})
            if header == 'ParentAgencyNum':
                is_organization = value == '0'
                the_type = 'organization' if is_organization else 'service'
                organization['type'] = the_type
            elif output_header:
                organization[output_header] = value
            elif output_phone_header:
                phone_numbers[current_phone_index][output_phone_header] = value
        sink.write_organization(organization)
        for i, item in enumerate(phone_numbers):
            phone_numbers[i]['organization_id'] = organization['id']
        sink.write_phone_numbers(phone_numbers)
    return sink


organization_header_map = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
    'AlternateName': 'alternate_name',
    'EmailAddressMain': 'email',
    'WebsiteAddress': 'url',
}


def phone_header_with_index_one(phone_field_with_any_index):
    return re.sub(r'^Phone\d', 'Phone1', phone_field_with_any_index)


def get_zero_based_phone_index(phone):
    r = re.match(r'^Phone(\d)', phone)
    return int(r[1]) - 1 if r else None


phone_header_map = {
    'Phone1Number': 'number',
    'Phone1Type': 'type',
    'Phone1Name': 'description',  # there is also a field Phone1Description but BC211 does not appear to use it
}
