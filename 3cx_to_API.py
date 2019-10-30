import requests
import logging
import os
import sys
import json

def main(argv):
    checkPhoneFormat(argv)
    config_file = os.path.dirname(os.path.realpath(__file__))+'/freshdesk.conf'
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    api_key = config.get('freshdesk', 'api_key')
    agent_id = config.get('freshdesk', 'agent_id')
    URL = config.get('freshdesk', 'url')
    HEADERS = {"Content-Type": "application/json"}

    newTicket(argv, api_key, agent_id, URL, HEADERS)

"""    response = requests.get(url=URLPhone, auth=(api_key,''), headers=HEADERS)
    logging.warning(response.content)"""



def newTicket(argv, api_key, agent_id, URL, HEADERS):
    URLTickets = URL+'tickets'
    logging.warning("requesting POST " + URLTickets)
    DATA = {
            "description": "support call from " argv,
            "subject": "Support call from " + argv,
            "phone": argv,
            "group_id": 5000251101,
            "name": argv,
            "responder_id": int(agent_id),
            "priority": 1,
            "status": 2
            }
    DATA = json.dumps(DATA)

    print(DATA)

    response = requests.post(url=URLTickets, data=DATA, auth=(api_key,''), headers=HEADERS)
    logging.warning(response.status_code)
    logging.warning(response.content)
    logging.warning(response.history)
    logging.warning(response.reason)

def checkPhoneFormat(argv):
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


main(sys.argv[1])
