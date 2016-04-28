import logging

from collections import OrderedDict
from egpackager.datasources import GspreadDataSource

class RegistryManager(object):

    def __init__(self, debug=False):
        # Set up logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing new registry manager")
        self.registry = OrderedDict()

    def add_gpsread_datasource(self, uri, credentials_file):
        self.logger.debug('Adding Google Sheets data source')
        self.registry[uri] = GspreadDataSource(uri, credentials_file)

    def registry(self):
        return self.registry

