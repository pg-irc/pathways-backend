class Bc211CsvDataBuilder:
    def __init__(self):
        self.data = {}
        self.data['ResourceAgencyNum'] = ''
        self.data['PublicName'] = ''

    def with_organization_id(self, id):
        self.data['ResourceAgencyNum'] = id
        return self

    def with_organization_name(self, name):
        self.data['PublicName'] = name
        return self

    def build(self):
        result = ''
        keys = self.data.keys()
        for key in keys:
            result += key + ','
        result += '\n'
        for key in keys:
            result += self.data.get(key) + ','
        result += '\n'
        return result
