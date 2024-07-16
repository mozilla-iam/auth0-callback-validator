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

    def get_auth0_domain(self):
      #  print(f"AUTH0_DOMAIN: {os.environ.get('AUTH0_DOMAIN')}")
        return os.environ.get("AUTH0_DOMAIN")

    def get_auth0_client_id(self):
     #   print(f"AUTH0_CLIENT_ID: {os.environ.get('AUTH0_CLIENT_ID')}")
        return os.environ.get("AUTH0_CLIENT_ID")

    def get_auth0_client_secret(self):
     #   print(f"AUTH0_CLIENT_SECRET: {os.environ.get('AUTH0_CLIENT_SECRET')}")
        return os.environ.get("AUTH0_CLIENT_SECRET")

