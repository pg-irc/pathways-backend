import random
from common.testhelpers.random_test_values import an_integer


class Bc211CsvDataBuilder:
    def __init__(self):
        self.data = [self.a_row()]

    def a_row(self):
        row = {}
        row['ResourceAgencyNum'] = ''
        row['PublicName'] = ''
        row['AlternateName'] = ''
        row['AgencyDescription'] = ''
        row['EmailAddressMain'] = ''
        row['WebsiteAddress'] = ''
        row['Phone1Number'] = ''
        row['Phone1Type'] = ''
        return row

    def next_row(self):
        self.data.append(self.a_row())
        return self

    def with_field(self, key, value):
        self.data[-1][key] = value
        return self

    def as_organization(self):
        self.data[-1]['ParentAgencyNum'] = '0'
        return self

    def as_service(self):
        self.data[-1]['ParentAgencyNum'] = str(an_integer(min=1))
        return self

    def build(self):
        result = ''
        shuffled_keys = list(self.data[0].keys())
        random.shuffle(shuffled_keys)
        for key in shuffled_keys:
            result += key + ','
        result += '\n'
        for row in self.data:
            for key in shuffled_keys:
                value = row.get(key)
                result += value + ','
            result += '\n'
        return result
