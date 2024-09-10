import os

import pytest

from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import epoch_micro, random_ip


@pytest.mark.coherence
class TestDefinition(BaseTest):

    def setup_class(self):
        self.sdk, self.username = BaseTest.setup_chariot(self)
        self.definition_name = f'test-definition-{epoch_micro()}'
        self.local_filepath = f'./{self.definition_name}.md'
        self.content = random_ip()
        with open(self.local_filepath, 'w') as file:
            file.write(self.content)

    def test_add_definition(self):
        self.sdk.definitions.add(self.local_filepath, self.definition_name)
        definitions, _ = self.sdk.definitions.list(self.definition_name)
        assert definitions[0] == self.definition_name

    def test_get_definition(self):
        self.sdk.definitions.get(self.definition_name, os.getcwd())
        with open(self.definition_name, 'r') as f:
            assert f.read() == self.content

    def teardown_class(self):
        os.remove(self.definition_name)
        os.remove(self.local_filepath)
