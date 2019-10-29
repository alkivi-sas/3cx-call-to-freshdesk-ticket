import requests
import logging
import os
import sys

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
    
    URLPhone = config.get('freshdesk', 'urlPhone')+callerNumber
    URLMoblie = config.get('freshdesk', 'urlMobile')+callerNumber

    HEADERS = {"Content-Type": "application/json"}
    logging.warning("requesting " + URLPhone)
    response = requests.get(url=URLPhone, auth=(api_key,''), headers=HEADERS)
    logging.warning(response.content)
    """ if no contact try with mobile"""

    """if no contact with mobile create a contact"""

    """create a ticket with the contact"""

main(sys.argv[1])
