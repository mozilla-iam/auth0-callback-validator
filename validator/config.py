import os

'''
Methods to pull configuration data from environment variables
'''

def get_auth0_domain():
    return os.environ.get("AUTH0_DOMAIN")

def get_auth0_client_id():
    return os.environ.get("AUTH0_CLIENT_ID")

def get_auth0_client_secret():
    return os.environ.get("AUTH0_CLIENT_SECRET")

