import csv


def parse(lines):
    reader = csv.reader(lines.split('\n'))
    fields = reader.__next__()
    result = [{}]
    for values in reader:
        if not values:
            break
        for field, value in zip(fields, values):
            output_field = map_to_output_field.get(field, None)
            if field == 'ParentAgencyNum':
                is_organization = value == '0'
                the_type = 'organization' if is_organization else 'service'
                result[-1]['type'] = the_type
            if output_field:
                result[-1][output_field] = value
        result.append({})
    return result


map_to_output_field = {
    'ResourceAgencyNum': 'id',
    'PublicName': 'name',
    'AgencyDescription': 'description',
    'AlternateName': 'alternate_name',
    'EmailAddressMain': 'email',
    'WebsiteAddress': 'url',
}
