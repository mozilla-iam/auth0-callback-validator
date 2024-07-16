from dotenv import load_dotenv

import logging
import os

'''
Methods to pull configuration data from environment variables
'''

class Config():

    logging.basicConfig(level=logging.INFO, filemode="a", filename="validator.log", format="%(asctime)s %(levelname)s %(message)s")

    def __init__(self):
        load_dotenv()
        self.domain = os.getenv('AUTH0_DOMAIN')
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')


    def get_auth0_domain(self):
        return self.domain

    def get_auth0_client_id(self):
        return self.client_id

    def get_auth0_client_secret(self):
        return self.client_secret

