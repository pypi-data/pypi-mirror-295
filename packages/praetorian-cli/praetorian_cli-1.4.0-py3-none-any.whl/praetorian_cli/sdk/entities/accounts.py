class Accounts:
    """ The methods in this class are to be assessed from sdk.accounts, where sdk is an instance
        of Chariot. """

    def __init__(self, api):
        self.api = api

    def get(self, key):
        """ Get details of an account """
        return self.api.search.by_exact_key(key)

    def list(self, username_filter='', offset=None, pages=1000):
        """ List accounts of collaborators and also list the master accounts that this user
            can access.

            Optionally filtered by username of the collaborators or the master accounts.
        """
        results, next_offset = self.api.search.by_key_prefix(f'#account#', offset, pages)

        # filter out the integrations
        results = [i for i in results if '@' in i['member']]

        # filter for user emails
        if username_filter:
            results = [i for i in results if username_filter == i['name'] or username_filter == i['member']]

        return results, next_offset

    def add_collaborator(self, collaborator_email):
        return self.api.link_account(collaborator_email)

    def delete_collaborator(self, collaborator_email):
        return self.api.unlink(collaborator_email)
