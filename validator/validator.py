"""
    OIDC/SAML Callback URL Validator - this application is used to help audit
"""

from auth import Auth
from colors import Colors
from config import Config
import logging
import requests

from rich.console import Console
from rich.table import Table

import sys
from tabulate import tabulate
import validators

logging.basicConfig(level=logging.INFO, filemode="w", filename="validator.log", format="%(asctime)s %(levelname)s %(message)s")

def format_table(client_id, table_data):
    table_title = f"\nCallback URLs for {client_id}"
    table = Table(title=table_title)
    columns = ["URL", "Valid?"]

    for column in columns:
        table.add_column(column)

    for row in table_data:
        table.add_row(*row, style='bright_green')

    console = Console()
    console.print(table)

def get_user_inputs():
    # get cli data passed in

    try:
        client_id = sys.argv[1]
        return client_id
    except IndexError:
        usage()
        logging.error("Error: client_id was not passed into application")
        sys.exit(1)

def get_client_callbacks(app_auth, client_id):
    client_data = app_auth.auth0_get_client_callbacks(client_id)
    if (client_data is None):
        print(f"Can not find data for client: {client_id}")
        logging.info(f"INFO: Can not find data for client: {client_id}")
        sys.exit(1)

    table_data = []

    if "callbacks" in client_data.keys():
        logging.info(f"Client: {client_id} has { len(client_data['callbacks']) } callback urls")

        #validate url and ensure it is responding
        for url in client_data["callbacks"]:
            if (validators.url(url)):
                try:
                    response = requests.head(url, timeout=5)
                    if (response.status_code != 404):
                        table_data.append([url, "True"])

                except Exception:
                    table_data.append([url, "False"])
                    continue

    #format report
    if len(table_data):
        format_table(client_id, table_data)

def get_all_client_callbacks(app_auth):
    client_data = app_auth.auth0_get_all_clients_callbacks()
    if (client_data is None):
        print("Can not find client data")
        logging.info("INFO: Can not find client data")

    for client in client_data:
        if "callbacks" in client.keys() and len(client["callbacks"]) > 0:
            logging.info(f"Client {client['client_id']} has {len(client['callbacks'])} callback urls")
            table_data = []

            for url in client["callbacks"]:
                logging.debug(f"testing url: {url}\n")
                if (validators.url(url)):
                    try:
                        response = requests.head(url, timeout=5)
                        if (response.status_code != 404):
                            table_data.append([url, "True"])

                    except Exception:
                        table_data.append([url, "False"])
                        continue

            #format report
            if len(table_data):
                format_table(client["client_id"], table_data)

        else:
            logging.info(f"Client {client['client_id']} has 0 callback urls")

def usage():
    print(f"\nThis script can be used to retrieve callback urls for a single client id or all clients \n \n -{Colors.bold}{Colors.green}search by client_id:{Colors.reset} python3 validator.py <client_id>\n -{Colors.bold}{Colors.green}retrieve all:{Colors.reset} python3 validator.py -a\n {Colors.bold}{Colors.green}-h(elp):{Colors.reset} python3 validator.py -h \n \n")

def main():
    #process command line arguments
    client_id = get_user_inputs()

    #show usage message
    if client_id == "-h":
        usage()
    else:
        # initialixe Config class
        config_vars = Config()

        # initialize Auth class
        app_auth = Auth(config_vars)

        if client_id == "-a":
            get_all_client_callbacks(app_auth)
        else:
            get_client_callbacks(app_auth, client_id)

if __name__ == "__main__":
    main()