import pytest

from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import epoch_micro


@pytest.mark.coherence
class TestAccount(BaseTest):

    def setup_class(self):
        self.sdk, self.username = BaseTest.setup_chariot(self)
        self.collaborator_email = f'chariot_cli_test_{epoch_micro()}@example-{epoch_micro()}.com'

    def test_add_collaborator(self):
        account = self.sdk.accounts.add_collaborator(self.collaborator_email)
        assert account['member'] == self.collaborator_email
        accounts, _ = self.sdk.accounts.list()
        assert len(accounts) > 0
        assert any(a['member'] == self.collaborator_email for a in accounts)

    def test_delete_collaborator(self):
        account = self.sdk.accounts.delete_collaborator(self.collaborator_email)
        assert account['member'] == self.collaborator_email
        accounts, _ = self.sdk.accounts.list()
        assert all(a['member'] != self.collaborator_email for a in accounts)
