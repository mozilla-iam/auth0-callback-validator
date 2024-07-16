from auth0.authentication import GetToken
from auth0.management import Auth0

import logging
import sys

'''
Auth0 methods to perform operations using auth0-python library
'''

class Auth():

    logging.basicConfig(level=logging.INFO, filemode="a", filename="validator.log", format="%(asctime)s %(levelname)s %(message)s")

    #constructor
    def __init__(self, config_vars):
        self.config_vars = config_vars
        self.get_auth0_vars()
        self.mgmt_api_token = None
        self.auth_client = None
        self.auth0_connect()


    def get_auth0_vars(self):
        #get client id to be search from command line
        self.mgmt_domain = self.config_vars.get_auth0_domain()
        self.mgmt_client_id = self.config_vars.get_auth0_client_id()
        self.mgmt_client_secret = self.config_vars.get_auth0_client_secret()

        if (self.mgmt_domain == None or self.mgmt_client_id == None or self.mgmt_client_secret == None):
            print("Usage: You have to define environment variables named:\n \n \t* AUTH0_DOMAIN\n \t* AUTH0_CLIENT_ID\n \t* AUTH0_CLIENT_SECRET\n Or define the variables in a file named .env\nThis will allow the tool to generate a token to access the Auth0 api")
            sys.exit(1)

    #get auth0 token
    def auth0_connect(self):
        try:
            if self.mgmt_api_token is None:
                get_token = GetToken(self.mgmt_domain, self.mgmt_client_id, self.mgmt_client_secret)
                token = get_token.client_credentials('https://{}/api/v2/'.format(self.mgmt_domain))
                mgmt_api_token = token['access_token']
                self.mgmt_api_token = mgmt_api_token

            if self.auth_client == None:
                self.auth_client = Auth0(self.mgmt_domain, self.mgmt_api_token)

        except Exception as e:
            logging.error(f"Call to get token for Auth0 domain: {self.mgmt_domain} failed due to error: {e}")
            print(f"Call to get token for Auth0 domain: {self.mgmt_domain} failed due to error: {e}")
            sys.exit(1)

    #get callbacks for specific client id
    def auth0_get_client_callbacks(self, client_id):
        try:
            client_data = self.auth_client.clients.get(client_id, fields=["client_id", "callbacks"], include_fields=True)
            return client_data
        except Exception as e:
            logging.error(f"Error retrieving client data: {client_id} for domain: {self.mgmt_domain}, error given: {e}")

    #get callbacks for all clients
    def auth0_get_all_clients_callbacks(self):
        try:
            client_data = self.auth_client.clients.all(fields=["client_id", "callbacks"], include_fields=True)
            return client_data
        except Exception as e:
            logging.error(f"Error retrieving all clients {e}")