import logging

from collections import OrderedDict
from egpackager.datasources import GspreadDataSource, RasterDataSource


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
            self._data['metadata'] = GspreadDataSource(*args, **kwargs)
        elif kwargs['type'] == 'raster':
            del kwargs['type']
            self.logger.debug('Adding raster data source')
            self._data['resource'] = RasterDataSource(*args, **kwargs)
        else:
            raise TypeError("Unknown data source type: {0}".format(kwargs['type']))
        self._data['uri'] = kwargs['uri']

    @property
    def data(self):
        return self._data

    def get_metadata_value(self, key, value):
        return self.data['metadata'].get_value(key, value)

    def get_resource_value(self, key, value):
        return self.data['resource'].get_value(key, value)

    @property
    def metadata(self):
        return self.data['metadata'].data

    @property
    def resource_metadata(self):
        return self.data['resource'].data
