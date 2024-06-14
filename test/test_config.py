import os
import unittest
from unittest import mock

from validator import config

class TestConfig(unittest.TestCase):
    @mock.patch.dict(os.environ, clear={"AUTH0_DOMAIN"})
    def test_empty_auth0_domain(self):
        self.assertIsNone(config.get_auth0_domain(), None)

    @mock.patch.dict(os.environ, clear={"AUTH0_CLIENT_ID"})
    def test_empty_auth0_client_id(self):
        self.assertIsNone(config.get_auth0_client_id(), None)

    @mock.patch.dict(os.environ, clear={"AUTH0_CLIENT_SECRET"})
    def test_empty_auth0_client_secret(self):
        self.assertIsNone(config.get_auth0_client_secret(), None)

    @mock.patch.dict(os.environ, {"AUTH0_DOMAIN": "mock.domain.test"})
    def test_get_auth0_domain(self):
        self.assertEqual(config.get_auth0_domain(), "mock.domain.test")

    @mock.patch.dict(os.environ, {"AUTH0_CLIENT_ID": "12abc456"})
    def test_get_auth0_client_id(self):
        self.assertEqual(config.get_auth0_client_id(), "12abc456")

    @mock.patch.dict(os.environ, {"AUTH0_CLIENT_SECRET": "7ueyrgsevwcwerh5y4werfvd"})
    def test_get_auth0_client_secret(self):
        self.assertEqual(config.get_auth0_client_secret(), "7ueyrgsevwcwerh5y4werfvd")
