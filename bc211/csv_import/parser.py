import csv


def parse(sink, lines):
    reader = csv.reader(lines.split('\n'))
    fields = reader.__next__()
    for values in reader:
        organization = {}
        phone = {}
        if not values:
            break
        for field, value in zip(fields, values):
            output_field = map_to_output_field.get(field, None)
            phone_field = map_to_phone_field.get(field, None)
            if field == 'ParentAgencyNum':
                is_organization = value == '0'
                the_type = 'organization' if is_organization else 'service'
                organization['type'] = the_type
            if output_field:
                organization[output_field] = value
            if phone_field:
                phone[phone_field] = value
        sink.write_organization(organization)
        phone['organization_id'] = organization['id']
        sink.write_phone(phone)
    return sink


map_to_output_field = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
    'AlternateName': 'alternate_name',
    'EmailAddressMain': 'email',
    'WebsiteAddress': 'url',
}

map_to_phone_field = {
    'Phone1Number': 'number',
    'Phone1Type': 'type',
}
