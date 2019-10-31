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

    check_phone_format(phone_number)
    api = API(domain, api_key, version=2)

    get_contact(phone_number, api)


def get_contact(phone_number: str, api: API) -> None:
    contacts = api.contacts.list_contacts(phone=phone_number)

    if len(contacts) < 1:
        logging.info("no phone known for " + phone_number)

        logging.info("trying mobile")
        contacts = api.contacts.list_contacts(mobile=phone_number)
        if len(contacts) < 1:
            logging.info("no mobile known for " + phone_number)

            logging.info("creating new contact")

            new_contact_ticket(phone_number, api)
        else:
            logging.info("creating ticket for " + contacts[0].name)

            new_ticket(api, contacts[0])
    else:
        logging.info("creating ticket for " + contacts[0].name)

        new_ticket(api, contacts[0])


def new_ticket(api: API, contact: Contact) -> None:
    ticket = api.tickets.create_ticket(
            "Support call between " + contact.name + " and " + agent_name,
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


def new_contact_ticket(phone_number: str, api: API) -> None:
    ticket = api.tickets.create_ticket(
            "Support call between " + phone_number + " and " + agent_name,
            description="Support call between " + phone_number + " and " + agent_name,
            phone=phone_number,
            group_id=int(group_id),
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket with new contact created")
    logging.info(ticket)


def check_phone_format(phone_number: str) -> None:
    caller_number = None
    if type(phone_number) == str and len(phone_number) < 13 and len(phone_number) > 10:
        caller_number = phone_number

        """removing the +"""
        if caller_number[0] == '+':
            caller_number = caller_number.replace('+', '')
        else:
            logging.warning("wrong format, should be +00000000000")
            logging.warning("entry is " + phone_number)
            sys.exit()

        """checking if it is all numbers"""
        for number in range(len(caller_number)):
            if not caller_number[number].isdigit():
                logging.warning("wrong format, should be +00000000000")
                logging.warning("entry is " + phone_number)
                sys.exit()


main(sys.argv[1])
