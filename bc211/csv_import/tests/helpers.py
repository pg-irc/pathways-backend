class Bc211CsvDataBuilder:
    def __init__(self):
        self.data = [self.a_row()]

    def a_row(self):
        row = {}
        row['ResourceAgencyNum'] = ''
        row['PublicName'] = ''
        row['AgencyDescription'] = ''
        return row

    def next_row(self):
        self.data.append(self.a_row())
        return self

    def with_field(self, key, value):
        self.data[-1][key] = value
        return self

    def build(self):
        result = ''
        keys = self.data[0].keys()
        for key in keys:
            result += key + ','
        result += '\n'
        for row in self.data:
            for key in keys:
                value = row.get(key)
                result += value + ','
            result += '\n'
        return result
