import unittest
from unittest.mock import patch, Mock
from validator import auth


class TestService(unittest.TestCase):
    #test initialization of the Auth service and setting config vars
    @patch('validator.auth.GetToken')
    def test_auth0_with_mocked_config(self, MockGetToken):
        # Create a mock Config instance
        mock_config = Mock()
        mock_config.get_auth0_domain.return_value = 'mock-domain'
        mock_config.get_auth0_client_id.return_value = 'mock-client-id'
        mock_config.get_auth0_client_secret.return_value = 'mock-client-secret'

        # Create a mock instance of GetToken
        mock_get_token_instance = MockGetToken.return_value
        mock_get_token_instance.oauth_token.return_value = {
            'access_token': 'mock_access_token',
            'token_type': 'Bearer',
            'expires_in': 86400
        }

        # Initialize the Auth service with the mock Config
        auth_test = auth.Auth(mock_config)

        # Get the config from the Service
        config = auth_test.config_vars

        # Assert the values are as expected
        self.assertEqual(config.get_auth0_domain() , 'mock-domain')
        self.assertEqual(config.get_auth0_client_id(), 'mock-client-id')
        self.assertEqual(config.get_auth0_client_secret(), 'mock-client-secret')
