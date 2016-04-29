import gspread
import logging
import os
import rasterio

from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame

class DataSource(object):

    def __init__(self, source_type, uri):
        self.source_type = source_type
        self.uri = uri
        self._data = None
        self.logger = logging.getLogger(__name__)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        assert isinstance(value, dict), "value is not a dict: %r" % value
        self._data = value

    def get_value(self, key, value):
        ''' Simple wrapper to fetch a column value based on a key (dataset name).

        Look for a (data row) value with a specified key.

        :param key: String dataset name.
        :param value: String column name of which value is returned.
        :return: String value
        '''
        # Check that the key and value are actually found
        if key not in self.data.keys():
            self.logger.error("Key '{0}' not found in data keys".format(key))
            return None
        elif value not in self.data[key].keys():
            self.logger.error("Value '{0}' not found in data with key {1}".format(value, key))
            return None
        else:
            return self.data[key][value]


class RasterDataSource(DataSource):

    def __init__(self, uri):
        DataSource.__init__(self, source_type="raster", uri=os.path.abspath(uri))
        self.logger = logging.getLogger(__name__)
        # Load the data straight away
        self.load_data()


    def load_data(self):
        ''' Load basic metadata from a geospatial raster file.

        The data is converted into a nested dictionary, where the name of the dataset is used as a top-level key.

        :param raster_file: String name of the raster file.
        :return: Methods is used for it's side effects only, no value is returned.
        '''
        try:
            # Register GDAL format drivers and configuration options with a
            # context manager.
            self.logger.debug('Registering GDAL drivers')
            with rasterio.drivers():
                with rasterio.open(self.uri) as src:
                    self._data = src.profile

            self.logger.info('Loaded metadata from {0}'.format(self.uri))

        except:
            raise


class GspreadDataSource(DataSource):

    def __init__(self, uri, credentials_file, spreadsheet_name=None, sheet=None):
        DataSource.__init__(self, source_type="Google Spreadsheet", uri=uri)
        self.logger = logging.getLogger(__name__)
        try:
            # Set up the Google Drive API credentials but don't get the data yet
            scope = ['https://spreadsheets.google.com/feeds']
            self.credentials_file = credentials_file
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            self.gc = gspread.authorize(credentials)
            self.logger.debug('Set up credentials for Google Sheets API')
            # Load the data straight away if enough information is provided
            self.load_data(spreadsheet_name, sheet)
        except gspread.exceptions.SpreadsheetNotFound as e:
            raise

    def load_data(self, spreadsheet_name, sheet):
        ''' Load data from a Google Spreadsheet once it has been set up.

        The data is converted into a nested dictionary, where the name of the dataset is used as a top-level key.

        :param spreadsheet_name: String name of the spreadsheet.
        :param sheet: Index number or name of the worksheet to be loaded. Named loading not supported yet.
        :return: Methods is used for it's side effects only, no value is returned.
        '''
        try:
            # Get the actual data from the worksheet
            if isinstance(sheet, int):
                dat = self.gc.open(spreadsheet_name).get_worksheet(sheet).get_all_values()
            elif isinstance(sheet, str):
                dat = self.gc.open(spreadsheet_name).worksheet(sheet).get_all_values()
            else:
                raise TypeError("'sheet' must be a valid int index or str sheet name")
            # Convert to dict, use dat[0] as the header row
            header = dat[0]
            dat_dict = {}
            for row in dat[1:len(dat)]:
                # Dataset name is the 5th column
                dataset_name = row[4]
                # Create an empty dict for the row items
                row_dict = {}
                # Loop over the columns
                for col_name in header:
                    row_dict[col_name] = row[header.index(col_name)]
                dat_dict[dataset_name] = row_dict

            self._data = dat_dict
            self.logger.info('Loaded data from {0}'.format(self.uri))

        except:
            raise
