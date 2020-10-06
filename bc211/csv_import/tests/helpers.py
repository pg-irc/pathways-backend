class Bc211CsvDataBuilder:
    def __init__(self):
        self.data = {}

    def with_organization_id(self, name):
        self.data['ResourceAgencyNum'] = name
        return self

    def build(self):
        for key in self.data.keys():
            return f'{key},\n{self.data[key]},\n'
