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

    def add_gpsread_datasource(self, *args, **kwargs):
        self.logger.debug('Adding Google Sheets data source')
        self._data[kwargs['uri']] = GspreadDataSource(*args, **kwargs)

    @property
    def data(self):
        return self._data
