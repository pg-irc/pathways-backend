import csv
import re
import hashlib
import uuid


def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    headers = reader.__next__()
    unique_location_ids = {}
    unique_phone_ids = {}
    unique_taxonomy_term_ids = {}

    for row in reader:

        organization_or_service = {}
        location = {}
        addresses = [{}, {}]
        phone_numbers = [{}]
        taxonomy_terms = []
        service_taxonomy_terms = []
        parent_id = None

        if not row:
            continue

        for header, value in zip(headers, row):

            parse_organization_and_service_fields(header, value, organization_or_service)
            parse_locations_fields(header, value, location)
            parse_address_fields(header, value, addresses)
            parse_phone_number_fields(header, value, phone_numbers)
            parse_taxonomy_fields(header, value, taxonomy_terms)

            if header == 'ParentAgencyNum':
                parent_id = value

        write_location_to_sink(location, addresses, phone_numbers, organization_or_service['id'],
                               parent_id, unique_location_ids, sink)
        if parent_id == '0':
            sink.write_organization(organization_or_service)
        else:
            write_service_to_sink(organization_or_service, location['id'], parent_id, sink)
            compile_taxonomy_terms(taxonomy_terms, organization_or_service['id'], service_taxonomy_terms)

        write_addresses_to_sink(addresses, location['id'], sink)
        write_phone_numbers_to_sink(phone_numbers, location['id'], unique_phone_ids, sink)
        write_taxonomy_terms_to_sink(taxonomy_terms, service_taxonomy_terms, unique_taxonomy_term_ids, sink)
    return sink


def parse_organization_and_service_fields(header, value, organization_or_service):
    output_header = organization_header_map.get(header, None)
    if output_header:
        organization_or_service[output_header] = value
    return organization_or_service


organization_header_map = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
    'AlternateName': 'alternate_name',
    'EmailAddressMain': 'email',
    'WebsiteAddress': 'url',
}


def parse_address_fields(header, value, addresses):
    output_address_header = address_header_map.get(get_normalized_address_header(header), None)
    is_physical_address_type = header.startswith('Physical')
    if output_address_header:
        index = 1 if is_physical_address_type else 0
        addresses[index][output_address_header] = value
        addresses[index]['type'] = 'physical_address' if is_physical_address_type else 'postal_address'
    return addresses


def get_normalized_address_header(fff):
    return re.sub(r'^Physical', 'Mailing', fff)


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


def parse_locations_fields(header, value, location):
    output_location_header = location_header_map.get(header, None)
    if output_location_header:
        if output_location_header in ['latitude', 'longitude']:
            try:
                value = float(value)
            except:
                value = None
        location[output_location_header] = value
    return location


location_header_map = {
    'ResourceAgencyNum': 'organization_id',
    'PublicName': 'name',
    'AlternateName': 'alternate_name',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
}


def parse_phone_number_fields(header, value, phone_numbers):
    output_phone_header = phone_header_map.get(phone_header_with_index_one(header), None)
    if output_phone_header:
        phone_index = get_zero_based_phone_index(header)
        while phone_index and len(phone_numbers) <= phone_index:
            phone_numbers.append({})
        phone_numbers[phone_index][output_phone_header] = value
    return phone_numbers


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


def parse_taxonomy_fields(header, value, taxonomy_terms):
    if header == 'TaxonomyTerm':
        taxonomy_terms += parse_taxonomy_terms(value)
    return taxonomy_terms


def parse_taxonomy_terms(value):
    names = re.split(r'[;\-\* ]', value)
    return [{'id': compute_hash(name, 'bc211'),
             'name': name,
             'vocabulary': 'bc211',
             'parent_name': '',
             'parent_id': ''} for name in names if name]


def write_service_to_sink(service, location_id, parent_organization_id, sink):
    service['organization_id'] = parent_organization_id
    sink.write_service(service, location_id)


def compile_taxonomy_terms(taxonomy_terms, service_id, service_taxonomy_terms):
    for item in taxonomy_terms:
        the_id = compute_hash(service_id, item['id'])
        service_taxonomy_terms.append({'id': the_id,
                                       'service_id': service_id,
                                       'taxonomy_id': item['id'],
                                       'taxonomy_detail': '',
                                       })
    return service_taxonomy_terms


def write_location_to_sink(location, addresses, phone_numbers, service_or_organization_id, parent_id, location_ids, sink):
    location['id'] = compute_location_id(location, addresses, phone_numbers)
    is_organization = parent_id == '0'
    location['organization_id'] = service_or_organization_id if is_organization else parent_id
    if location['id'] not in location_ids:
        sink.write_location(location)
        location_ids[location['id']] = 1
    return location_ids


def write_addresses_to_sink(addresses, location_id, sink):
    for i, address in enumerate(addresses):
        if not address:
            continue
        address['id'] = str(uuid.uuid4())
        address['location_id'] = location_id
        sink.write_address(address)


def write_phone_numbers_to_sink(phone_numbers, location_id, phone_ids, sink):
    for i, phone_number in enumerate(phone_numbers):
        the_id = compute_hash(phone_number['number'])
        if not phone_number['number'] or the_id in phone_ids:
            continue
        phone_number['id'] = the_id
        phone_number['location_id'] = location_id
        sink.write_phone_number(phone_number)
        phone_ids[the_id] = 1


def write_taxonomy_terms_to_sink(taxonomy_terms, service_taxonomy_terms, taxonomy_term_ids, sink):
    for term in taxonomy_terms:
        if term['id'] not in taxonomy_term_ids:
            sink.write_taxonomy_term(term)
            taxonomy_term_ids[term['id']] = 1
    sink.write_service_taxonomy_terms(service_taxonomy_terms)
    return taxonomy_term_ids


def compute_location_id(location, addresses, phone_numbers):
    return compute_hash(compute_address_id(addresses[0]),
                        compute_address_id(addresses[1]),
                        compute_phone_number_id(phone_numbers[0]),
                        str(location.get('latitude', '')),
                        str(location.get('longitude', ''))
                        )


def compute_address_id(address):
    return compute_hash(
        address.get('address_1', ''),
        address.get('address_2', ''),
        address.get('address_3', ''),
        address.get('address_4', ''),
        address.get('city', ''),
        address.get('state_province', ''),
        address.get('postal_code', ''),
        address.get('country', ''),
        )


def compute_phone_number_id(phone_number):
    if not phone_number:
        return ''
    return compute_hash(phone_number.get('number', ''))


def compute_hash(*args):
    hasher = hashlib.sha1()
    for arg in args:
        hasher.update(arg.encode('utf-8'))
    return hasher.hexdigest()
