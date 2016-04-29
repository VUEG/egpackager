import logging

from collections import OrderedDict
from egpackager.datasources import GspreadDataSource


class DataManager(object):

    def __init__(self, debug=False):
        # Set up logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing new registry manager")
        self._data = OrderedDict()

    def add_datasource(self, *args, **kwargs):
        if 'type' not in kwargs:
            raise TypeError("Missing require keyword argument: 'type")
        if kwargs['type'] == 'gspread':
            # Remove keyword argument 'type' as it us not needed anymore
            del kwargs['type']
            self.logger.debug('Adding Google Sheets data source')
            self._data[kwargs['uri']] = GspreadDataSource(*args, **kwargs)
        elif kwargs['type'] == 'raster':
            pass

    @property
    def data(self):
        return self._data
