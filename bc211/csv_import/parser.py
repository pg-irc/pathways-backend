import csv
import re


def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    for row in reader:
        organization_or_service = {}
        location = {}
        is_organization = False
        phone_numbers = [{}]
        if not row:
            continue
        for header, value in zip(headers, row):
            output_header = organization_header_map.get(header, None)
            output_location_header = location_header_map.get(header, None)
            output_phone_header = phone_header_map.get(phone_header_with_index_one(header), None)
            phone_index = get_zero_based_phone_index(header)
            while phone_index and len(phone_numbers) <= phone_index:
                phone_numbers.append({})
            if header == 'ParentAgencyNum':
                is_organization = value == '0'
            if output_header:
                organization_or_service[output_header] = value
            if output_location_header:
                if output_location_header in ['latitude']:
                    value = float(value)
                location[output_location_header] = value
            if output_phone_header:
                phone_numbers[phone_index][output_phone_header] = value
        if is_organization:
            sink.write_organization(organization_or_service)
        else:
            sink.write_service(organization_or_service)
        sink.write_location(location)
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


location_header_map = {
    'ResourceAgencyNum': 'organization_id',
    'PublicName': 'name',
    'Latitude': 'latitude',
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
