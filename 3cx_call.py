#!/Users/anthony/3cx-call-to-freshdesk-ticket/.venv/bin/python
# Please update the hashbang to match your python venv

import logging
import click
import os
from freshdesk.api import API
import configparser


logging.basicConfig(filename="/var/log/3cx-freshdesk.log", level=logging.DEBUG)


def validate_number(ctx, param, value):
    if not check_phone_format(value):
        raise click.BadParameter(f"Wrong number {value}")
    else:
        return value


def _get_config():
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/freshdesk.conf"
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config


class CallHandler:
    def __init__(self):
        self.config = _get_config()
        self.api = None
        self.init_api()

    def init_api(self):
        api_key = self.config.get("freshdesk", "api_key")
        self.agent_id = self.config.get("freshdesk", "agent_id")
        domain = self.config.get("freshdesk", "domain")
        self.agent_name = self.config.get("freshdesk", "name")
        self.group_id = self.config.get("freshdesk", "group_id")
        self.priority = self.config.get("freshdesk", "priority")

        if not check_conf(api_key, self.agent_id, domain, self.group_id):
            raise click.BadParameter("Wrong conf")

        api = API(domain, api_key, version=2)
        self.api = api

    def get_contact(self, number):
        contacts = self.api.contacts.list_contacts(phone=number)

        if len(contacts) < 1:
            logging.info("no phone known")

            logging.info("trying mobile")
            contacts = self.api.contacts.list_contacts(mobile=number)
            if len(contacts) < 1:
                logging.info("no mobile known")
                return None

        logging.info("contact found")
        return contacts[0]

    def new_contact_ticket(self, number):
        description = "Support call between {0} and {1}".format(number, self.agent_name)

        ticket = self.api.tickets.create_ticket(
            subject=description,
            description=description,
            phone=number,
            group_id=int(self.group_id),
            name="Fusionne moi",
            responder_id=int(self.agent_id),
            priority=self.priorty,
            status=2,
        )
        logging.info("ticket with new contact created")
        logging.info(ticket)
        return True

    def new_ticket(self, contact):
        description = "Support call between {0} and {1}".format(
            contact.name, self.agent_name
        )

        ticket = self.api.tickets.create_ticket(
            subject=description,
            description=description,
            requester_id=contact.id,
            group_id=int(self.group_id),
            name=contact.name,
            responder_id=int(self.agent_id),
            priority=int(self.priority),
            status=2,
        )
        logging.info("ticket created")
        logging.info(ticket)
        return True


@click.command()
@click.option("--number", callback=validate_number)
def handle_call(number):
    handler = CallHandler()
    contact = handler.get_contact(number)
    if contact is None:
        logging.info("no contact found, creating a new one")
        handler.new_contact_ticket(number)
    else:
        if not handler.new_ticket(contact):
            logging.warning("error creating the ticket")


def check_phone_format(number):
    caller_number = None
    if isinstance(number, str) and len(number) < 13 and len(number) > 10:
        caller_number = number

        """removing the +"""
        if caller_number[0] == "+":
            caller_number = caller_number.replace("+", "")
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


def check_conf(api_key, agent_id, domain, group_id):
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


if __name__ == "__main__":
    handle_call()
