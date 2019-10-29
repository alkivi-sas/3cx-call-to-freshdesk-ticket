import requests
import logging
import os
import sys

"""URL = "https://alkivi.freshdesk.com/api/v2/contacts?phone=%2B33145729797"
HEADERS = {"Content-Type": "application/json"}

response = requests.get(url=URL, auth=AUTH, headers=HEADERS)
logging.warning(response)
logging.warning(response.content)
logging.warning(vars(response))"""


def main(argv):
    callerNumber = None
    if type(argv) == str and len(argv) == 12:
        callerNumber = argv

        """removing the +"""
        if argv[0] == '+':
            callerNumber = callerNumber.replace('+', '')
            print("removed +")
        else:
            logging.warning("wrong format, should be +33000000000")
            logging.warning("entry is "+ argv)
            sys.exit()

        """checking if it is all numbers"""
        for number in range(len(callerNumber)):
            if not callerNumber[number].isdigit():
                logging.warning("wrong format, should be +33000000000")
                logging.warning("entry is "+ argv)
                sys.exit()
    
    config_file = os.path.dirname(os.path.realpath(__file__))+'/freshdesk.conf'
    logging.warning(config_file)
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    domain = config.get('freshdesk', 'domain', fallback='missing conf file')
    api_key = config.get('freshdesk', 'api_key')
    URL = config.get('freshdesk', 'url')+callerNumber
    HEADERS = {"Content-Type": "application/json"}
    logging.warning("requesting " + URL)
    response = requests.get(url=URL, auth=(api_key,''), headers=HEADERS)
    logging.warning(response.content)

main(sys.argv[1])
