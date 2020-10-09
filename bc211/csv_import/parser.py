import csv
import re


def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    for row in reader:
        organization_or_service = {}
        is_organization = False
        phone_numbers = [{}]
        if not row:
            break
        for header, value in zip(headers, row):
            output_header = organization_header_map.get(header, None)
            output_phone_header = phone_header_map.get(phone_header_with_index_one(header), None)
            phone_index = get_zero_based_phone_index(header)
            while phone_index and len(phone_numbers) <= phone_index:
                phone_numbers.append({})
            if header == 'ParentAgencyNum':
                is_organization = value == '0'
            elif output_header:
                organization_or_service[output_header] = value
            elif output_phone_header:
                phone_numbers[phone_index][output_phone_header] = value
        if is_organization:
            organization_or_service['type'] = 'organization'
            sink.write_organization(organization_or_service)
        else:
            organization_or_service['type'] = 'service'
            sink.write_service(organization_or_service)
        phone_numbers = [n for n in phone_numbers if n['number']]
        for i, item in enumerate(phone_numbers):
            if is_organization:
                phone_numbers[i]['organization_id'] = organization_or_service['id']
            else:
                phone_numbers[i]['service_id'] = organization_or_service['id']
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
