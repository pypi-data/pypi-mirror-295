import pytest

from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import epoch_micro, random_ip


@pytest.mark.coherence
class TestJob(BaseTest):

    def setup_class(self):
        self.sdk, self.username = BaseTest.setup_chariot(self)
        self.asset_dns = f'contoso-{epoch_micro()}.com'
        self.asset_name = random_ip()

    def test_add_job(self):
        result = self.sdk.assets.add(self.asset_dns, self.asset_name)
        asset_key = result['key']
        self.sdk.jobs.add(asset_key, 'subfinder')
        jobs, _ = self.sdk.jobs.list(self.asset_dns)
        assert len(jobs) == 1
        assert jobs[0]['source'] == 'subfinder'
        assert jobs[0]['dns'] == self.asset_dns
