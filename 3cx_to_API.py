import requests
import logging
import os
import sys
import json
from freshdesk.api import API

config_file = os.path.dirname(os.path.realpath(__file__))+'/freshdesk.conf'
import configparser
config = configparser.RawConfigParser()
config.read(config_file)
api_key = config.get('freshdesk', 'api_key')
agent_id = config.get('freshdesk', 'agent_id')
domain = config.get('freshdesk', 'domain')
agent_name = config.get('freshdesk', 'name')
group_id = config.get('freshdesk', 'group_id')

def main(argv):
    logging.basicConfig(filename='/var/log/3cx-v2-freshdesk-macos.log',level=logging.DEBUG)
    
    checkPhoneFormat(argv)
    api = API(domain, api_key, version=2)

    getContact(argv, api)


def getContact(argv, api):
    contacts = api.contacts.list_contacts(phone=argv)

    if len(contacts) < 1:
        logging.info("no phone known for " + argv)
        
        logging.info("trying mobile")
        contacts = api.contacts.list_contacts(mobile=argv)
        if len(contacts) < 1:
            logging.info("no mobile known for " + argv)

            logging.info("creating new contact")
            
            newContactTicket(argv, api)
        else:
            logging.info("creating ticket for " + contacts[0].name)
            
            newTicket(argv, api, contacts[0])
    else:
        logging.info("creating ticket for " + contacts[0].name)

        newTicket(argv, api, contacts[0])


def newTicket(argv, api, contact):
    ticket = api.tickets.create_ticket("Support call between " + contact.name + " and " + agent_name,
            description="Support call between " + contact.name + " and " + agent_name,
            requester_id=contact.id,
            group_id=int(group_id),
            name=contact.name,
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket created")
    logging.info(ticket)


def newContactTicket(argv, api):
    ticket = api.tickets.create_ticket("Support call between " + argv + " and " + agent_name,
            description="Support call between " + argv + " and " + agent_name,
            phone=argv,
            group_id=int(group_id),
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket with new contact created")
    logging.info(ticket)


def checkPhoneFormat(argv):
    callerNumber = None
    if type(argv) == str and len(argv) == 12:
        callerNumber = argv

        """removing the +"""
        if argv[0] == '+':
            callerNumber = callerNumber.replace('+', '')
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
