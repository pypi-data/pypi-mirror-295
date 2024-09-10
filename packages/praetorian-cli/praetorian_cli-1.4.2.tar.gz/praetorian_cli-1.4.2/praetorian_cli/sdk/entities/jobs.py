class Jobs:
    """ The methods in this class are to be assessed from sdk.jobs, where sdk is an instance
    of Chariot. """

    def __init__(self, api):
        self.api = api

    def add(self, asset_key, capability):
        """ Add a job for an asset for a specific capability """
        return self.api.force_add('job', dict(key=asset_key, name=capability))

    def get(self, key):
        """ Get details of a job """
        return self.api.search.by_exact_key(key)

    def list(self, prefix_filter='', offset=None, pages=1000):
        """ List jobs, optionally prefix-filtered by the portion of the key after
            '#job#' """
        return self.api.search.by_key_prefix(f'#job#{prefix_filter}', offset, pages)
