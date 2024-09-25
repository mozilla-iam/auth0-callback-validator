"""
    OIDC/SAML Callback URL Validator - this application is used to help audit
"""

import json
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
    # Note: This should use a proper cli library but hacking around it
    #   because this is supposed to be a unimportant script - Eric

    client_id = None
    arguments = []

    try:
        for argument in sys.argv[1:]:
            if argument[0] == '-':
                if argument not in ['-a', '-h', '--include-valid', '--json']:
                    usage()
                    logging.error("Error: invalid argument {}".format(argument))
                    print("Error: invalid argument {}".format(argument))
                    sys.exit(1)
                arguments.append(argument)
            else:
                if not client_id:
                    client_id = argument
                else:
                    logging.error("Error: only one client_id expected")
                    print("Error: only one client_id expected")
                    sys.exit(1)

        if not client_id and ('-a' not in arguments) and ('-h' not in arguments):
            logging.error("Error: either `-h` must be specified or one of client_id or `-a`")
            print("Error: either `-h` must be specified or one of client_id or `-a`")
            sys.exit(1)
        return client_id, arguments
    except IndexError:
        usage()
        logging.error("Error: no arguments were passed into application")
        sys.exit(1)

def get_client_callbacks(app_auth, client_id, json_output=False):
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
                        if json_output:
                            table_data.append({'url': url, 'valid': True})
                        else:
                            table_data.append([url, "True"])

                except Exception as e:
                    if json_output:
                        table_data.append({'url': url, 'valid': "False - {}".format(type(e).__name__)})
                    else:
                        table_data.append([url, "False - {}".format(type(e).__name__)])
                    continue

    #format report
    if len(table_data):
        if json_output:
            print(json.dumps({client_id: table_data}))
        else:
            format_table(client_id, table_data)

def get_all_client_callbacks(app_auth, include_valid=False, json_output=False):
    client_data = app_auth.auth0_get_all_clients_callbacks()
    if (client_data is None):
        print("Can not find client data")
        logging.info("INFO: Can not find client data")
    
    json_callbacks = {}

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
                            if include_valid:
                                if json_output:
                                    table_data.append({'url': url, 'valid': True})
                                else:
                                    table_data.append([url, "True"])

                    except Exception as e:
                        logging.error(
                            "Reached exception attempting to validate `{}` for client id `{}`:\n{}\n\n".format(url, client['client_id'], e)
                        )
                        if json_output:
                            table_data.append({'url': url, 'valid': "False - {}".format(type(e).__name__)})
                        else:
                            table_data.append([url, "False - {}".format(type(e).__name__)])
                        continue

            #format report
            if len(table_data):
                if json_output:
                    json_callbacks[client['client_id']] = table_data
                else:
                    format_table(client["client_id"], table_data)

        else:
            logging.info(f"Client {client['client_id']} has 0 callback urls")
        
    if json_output:
        print(json.dumps(json_callbacks))

def usage():
    print(f"\nThis script can be used to retrieve callback urls for a single client id or all clients \n \n -{Colors.bold}{Colors.green}search by client_id:{Colors.reset} python3 validator.py <client_id>\n -{Colors.bold}{Colors.green}retrieve all:{Colors.reset} python3 validator.py -a\n    - {Colors.bold}{Colors.green}Include invalid (only with `-a`):{Colors.reset} python3 validator.py -a --include-valid \n -{Colors.bold}{Colors.green}output as JSON:{Colors.reset} python3 validator.py -a --json\n -{Colors.bold}{Colors.green}h(elp):{Colors.reset} python3 validator.py -h \n \n")

def main():
    #process command line arguments
    client_id, arguments = get_user_inputs()

    #show usage message
    if '-h' in arguments:
        usage()
    else:
        # initialixe Config class
        config_vars = Config()

        # initialize Auth class
        app_auth = Auth(config_vars)

        if '-a' in arguments:
            get_all_client_callbacks(app_auth, '--include-valid' in arguments, '--json' in arguments)
        else:
            get_client_callbacks(app_auth, client_id, '--json' in arguments)

if __name__ == "__main__":
    main()