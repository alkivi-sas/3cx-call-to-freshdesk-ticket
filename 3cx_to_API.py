import logging
import os
import sys
from freshdesk.api import API
import configparser

config_file = os.path.dirname(os.path.realpath(__file__))+'/freshdesk.conf'
config = configparser.RawConfigParser()
config.read(config_file)
api_key = config.get('freshdesk', 'api_key')
agent_id = config.get('freshdesk', 'agent_id')
domain = config.get('freshdesk', 'domain')
agent_name = config.get('freshdesk', 'name')
group_id = config.get('freshdesk', 'group_id')


def main(phone_number: str) -> None:
    logging.basicConfig(filename='/var/log/3cx-v2-freshdesk-macos.log',
            level=logging.DEBUG)

    if not check_phone_format(phone_number):
        sys.exit()
    api = API(domain, api_key, version=2)

    contact = get_contact(phone_number, api)
    if contact is None:
        new_contact_ticket(phone_number, api)
    else:
        response = new_ticket(api, contact)
        """gerer la reponse de la creation de ticket"""
        """pas forcement un bool, ca peut être le status (201, 400, 502) de la reponse"""


def get_contact(phone_number: str, api: API):
    contacts = api.contacts.list_contacts(phone=phone_number)

    if len(contacts) < 1:
        logging.info("no phone known")

        logging.info("trying mobile")
        contacts = api.contacts.list_contacts(mobile=phone_number)
        if len(contacts) < 1:
            logging.info("no mobile known")
            return None
    
    logging.info("contact found")
    return contacts[0]


def new_ticket(api: API, contact) -> bool:
    description = 'Support call between {0} and {1}'.format(contact.name, agent_name)

    ticket = api.tickets.create_ticket(
            subject=description,
            description=description,
            requester_id=contact.id,
            group_id=int(group_id),
            name=contact.name,
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket created")
    logging.info(ticket)


def new_contact_ticket(phone_number: str, api: API) -> None:
    description = 'Support call between {0} and {1}'.format(phone_number, agent_name)

    ticket = api.tickets.create_ticket(
            isubject=description,
            description=description,
            phone=phone_number,
            group_id=int(group_id),
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket with new contact created")
    logging.info(ticket)


def check_phone_format(phone_number: str) -> bool:
    caller_number = None
    if type(phone_number) == str and len(phone_number) < 13 and len(phone_number) > 10:
        caller_number = phone_number

        """removing the +"""
        if caller_number[0] == '+':
            caller_number = caller_number.replace('+', '')
        else:
            logging.warning("wrong format, should be +00000000000")
            logging.warning("entry is " + phone_number)
            return False

        """checking if it is all numbers"""
        for number in range(len(caller_number)):
            if not caller_number[number].isdigit():
                logging.warning("wrong format, should be +00000000000")
                logging.warning("entry is " + phone_number)
                return False
    return True

main(sys.argv[1])
