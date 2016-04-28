import gspread
import logging
import oauth2client

from pandas import DataFrame

class DataSource(object):

    def __init__(self, source_type, uri):
        self.source_type = source_type
        self.URI = uri
        self._data = None
        self.logger = logging.getLogger(__name__)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        assert isinstance(value, DataFrame), "value is not a DataFrame: %r" % value
        self._data = value

    def get_value(self, key, value):
        ''' Simple wrapper to fetch a column value based on a key (dataset name).

        The key is hardcoded to "name", so whatever data source is needed it needs to have a column called "name" that
        uniquely identifies the dataset. If several matches are found, only the first is used.

        :param key: String dataset name.
        :param value: String column name of which value is returned.
        :return: String value
        '''
        # Check that the key and value are actually found
        if key not in list(self.data["name"]):
            self.logger.error("Key '{0}' not found in column 'name'".format(key))
            return None
        elif value not in list(self.data.columns):
            self.logger.error("Value '{0}' not found in column names".format(value))
            return None
        else:
            return self.data.loc[self.data.name == key, value].values[0]


class GspreadDataSource(DataSource):

    def __init__(self, uri, credentials_file, spreadsheet_name=None, sheet_no=None):
        DataSource.__init__(self, source_type="Google Spreadsheet", uri=uri)
        self.logger = logging.getLogger(__name__)
        try:
            # Set up the Google Drive API credeantials but don't get the data yet
            from oauth2client.service_account import ServiceAccountCredentials
            scope = ['https://spreadsheets.google.com/feeds']
            self.credentials_file = credentials_file
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            self.gc = gspread.authorize(credentials)
            self.logger.debug('Set up credentials for Google Sheets API')
            # Load the data straight away if enough information is provided
            self.load_data(spreadsheet_name, sheet_no)
        except gspread.exceptions.SpreadsheetNotFound as e:
            raise

    def load_data(self, spreadsheet_name, sheet_no):
        ''' Load data from a Google Spreadsheet once it has been set up.
        :param spreadsheet_name: String name of the spreadsheet.
        :param sheet_no: Index number of the worksheet to be loaded. Named loading not supported yet.
        :return: Methods is used for it's side effects only, no value is returned.
        '''
        try:
            # Get the actual data from the worksheet
            dat = self.gc.open(spreadsheet_name).get_worksheet(sheet_no).get_all_values()
            # Convert to DataFrame for easier access. dat[0] is the header row
            self._data = DataFrame(data=dat[1:len(dat)], columns=dat[0])
            self.logger.info('Loaded data from {0}'.format(self.URI))

        except:
            raise
