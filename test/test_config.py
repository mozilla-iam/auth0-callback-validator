import os
import unittest
from unittest import mock
from unittest.mock import patch

import sys
sys.path.append('./validator')

from config import Config

class TestConfig(unittest.TestCase):

    @patch('config.load_dotenv')
    def test_config_from_os_env(self, mock_load_dotenv):
        # Mock environment variables set
        with patch.dict(os.environ, {
            'AUTH0_DOMAIN': 'os-domain',
            'AUTH0_CLIENT_ID': 'os-client-id',
            'AUTH0_CLIENT_SECRET': 'os-client-secret',
        }):

            # Initialize the configuration
            config_vars = Config()

            # Assert the values are as expected
            self.assertEqual(config_vars.domain, 'os-domain')
            self.assertEqual(config_vars.client_id, 'os-client-id')
            self.assertEqual(config_vars.client_secret, 'os-client-secret')

            # Assert load_dotenv was called
            mock_load_dotenv.assert_called_once()
