class DataSource(object):

    def __init__(self, type):
        self.type = type

class GspreadDataSource(DataSource):

    def __init__(self):
        DataSource.__init__(self, type="Google Spreadsheet")
