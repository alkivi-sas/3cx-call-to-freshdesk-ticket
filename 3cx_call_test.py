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

logging.basicConfig(filename='/var/log/3cx-freshdesk.log', level=logging.DEBUG)


def handle_call(number):
    if not check_conf():
        sys.exit()

    if not check_phone_format(number):
        sys.exit()
    api = API(domain, api_key, version=2)

    contact = get_contact(number, api)
    if contact is None:
        logging.info("no contact found, creating a new one")
        new_contact_ticket(number, api)
    else:
        if not new_ticket(api, contact):
            logging.warning("error creating the ticket")


def get_contact(number, api):
    contacts = api.contacts.list_contacts(phone=number)

    if len(contacts) < 1:
        logging.info("no phone known")

        logging.info("trying mobile")
        contacts = api.contacts.list_contacts(mobile=number)
        if len(contacts) < 1:
            logging.info("no mobile known")
            return None

    logging.info("contact found")
    return contacts[0]


def new_ticket(api, contact):
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
    return True
    """add a try catch"""


def new_contact_ticket(number, api):
    description = 'Support call between {0} and {1}'.format(number, agent_name)

    ticket = api.tickets.create_ticket(
            subject=description,
            description=description,
            phone=number,
            group_id=int(group_id),
            name='Fusionne moi',
            responder_id=int(agent_id),
            priority=1,
            status=2
            )
    logging.info("ticket with new contact created")
    logging.info(ticket)
    return True


def check_phone_format(number):
    caller_number = None
    if type(number) == str and len(number) < 13 and len(number) > 10:
        caller_number = number

        """removing the +"""
        if caller_number[0] == '+':
            caller_number = caller_number.replace('+', '')
        else:
            logging.info("wrong format, should be +00000000000")
            logging.info("entry is " + number)
            return False

        """checking if it is all numbers"""
        for number in caller_number:
            if not number.isdigit():
                logging.info("wrong format, should be +00000000000")
                logging.info("entry is " + number)
                return False
        return True
    else:
        logging.warning("wrong format, should be +00000000000")
        logging.warning("entry is " + number)
        return False


def check_conf():
    if len(api_key) == 20 or len(api_key) == 19:
        if len(agent_id) > 9:
            if domain != "":
                if len(group_id) > 8:
                    return True
                else:
                    logging.warning("group ID format not accepted")
            else:
                logging.warning("domain not provided")
        else:
            logging.warning("agent ID format not accepted")
    else:
        logging.warning("api key format not accepted")
    return False


if __name__ == '__main__':
    handle_call(sys.argv[1])


