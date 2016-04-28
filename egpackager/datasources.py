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


class GspreadDataSource(DataSource):

    def __init__(self, uri, credentials_file):
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
        except gspread.exceptions.SpreadsheetNotFound as e:
            raise

    @property
    def data(self):
        return self._data

    def load_data(self, spreadsheet_name, sheet_no):
        try:
            # Get the actual data from the worksheet
            dat = self.gc.open(spreadsheet_name).get_worksheet(sheet_no).get_all_values()
            # Convert to DataFrame for easier access. dat[0] is the header row
            self._data = DataFrame(data=dat[1:len(dat)], columns=dat[0])
            self.logger.info('Loaded data from {0}'.format(self.URI))

        except:
            raise
