import csv
import re
import hashlib

def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    for row in reader:
        organization_or_service = {}
        is_organization = False
        parent_organization_id = None
        location = {}
        addresses = [{}, {}]
        phone_numbers = [{}]
        if not row:
            continue
        for header, value in zip(headers, row):
            output_header = organization_header_map.get(header, None)
            output_location_header = location_header_map.get(header, None)
            output_address_header = address_header_map.get(get_normalized_address_header(header), None)
            is_physical_address_type = header.startswith('Physical')
            output_phone_header = phone_header_map.get(phone_header_with_index_one(header), None)
            phone_index = get_zero_based_phone_index(header)
            while phone_index and len(phone_numbers) <= phone_index:
                phone_numbers.append({})
            if header == 'ParentAgencyNum':
                is_organization = value == '0'
                parent_organization_id = None if is_organization else value
            if output_header:
                organization_or_service[output_header] = value
            if output_location_header:
                if output_location_header in ['latitude', 'longitude']:
                    try:
                        value = float(value)
                    except:
                        value = None
                location[output_location_header] = value
            if output_address_header:
                index = 1 if is_physical_address_type else 0
                addresses[index]['type'] = 'physical_address' if is_physical_address_type else 'postal_address'
                addresses[index][output_address_header] = value
            if output_phone_header:
                phone_numbers[phone_index][output_phone_header] = value
        if is_organization:
            sink.write_organization(organization_or_service)
        else:
            organization_or_service['organization_id'] = parent_organization_id
            sink.write_service(organization_or_service)
        location['id'] = compute_hash(location['name'])
        location['organization_id'] = organization_or_service['id'] if is_organization else parent_organization_id
        sink.write_location(location)
        for i, item in enumerate(addresses):
            addresses[i]['location_id'] = location['id']
        sink.write_addresses(addresses)
        phone_numbers = [n for n in phone_numbers if n['number']]
        for i, item in enumerate(phone_numbers):
            if is_organization:
                phone_numbers[i]['organization_id'] = organization_or_service['id']
            else:
                phone_numbers[i]['service_id'] = organization_or_service['id']
        sink.write_phone_numbers(phone_numbers)
    return sink


def compute_hash(*args):
    hasher = hashlib.sha1()
    for arg in args:
        hasher.update(arg.encode('utf-8'))
    return hasher.hexdigest()


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
    'AlternateName': 'alternate_name',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
}


address_header_map = {
    'MailingAddress1': 'address_1',
    'MailingAddress2': 'address_2',
    'MailingAddress3': 'address_3',
    'MailingAddress4': 'address_4',
    'MailingCity': 'city',
    'MailingStateProvince': 'state_province',
    'MailingPostalCode': 'postal_code',
    'MailingCountry': 'country',
}


def get_normalized_address_header(fff):
    return re.sub(r'^Physical', 'Mailing', fff)


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
