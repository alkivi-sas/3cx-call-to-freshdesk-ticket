# 3cx-call-to-freshdesk
## Installation

The easiest way to install is inside a virtualenv and with our python-freshdesk fork (https://github.com/alkivi-sas/python-freshdesk)

1. If you don't have its already, Install Brew, Python3 and Pipenv

First, Install X-Code from the app store

    ```
    $ xcode-select --install
    $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    $ export PATH=/usr/local/bin:$PATH
    ```
Restart your Terminal

    ```
    $ brew install python3
    $ brew install pipenv
    ```

2. Clone and pipenv:

    ```
    $ git clone https://github.com/alkivi-sas/3cx-call-to-freshdesk-ticket
    $ cd 3cx-call-to-freshdesk-ticket
    $ pipenv install
    $ pipenv shell
    $ which python #result of this command will help you to config 3CX
    ```

3. Change the conf file :

    ```
    $ cp freshdesk-example.conf freshdesk.conf
    $ vim freshdesk.conf
    ```
Change values with your platform, you can have your caller ID going to a ticket you resolved and you put '.json' at the end of the URL
Example :  https://domain.freshdesk.com/helpdesk/tickets/62.json , you will see responder_id. It is your agent ID.

For the API Key :
- Login to your Support Portal
- Click on your profile picture on the top right corner of your portal
- Go to Profile settings Page
- Your API key will be available below the change password section to your right

For the agent ID and group ID

    ```
    $ curl -v -u api_key:test -X GET 'https://company.freshdesk.com/api/v2/groups'
    $ curl -v -u api_key:test -X GET 'https://company.freshdesk.com/api/v2/agents'
    ```
4. Create the log file :

    ```
    $ sudo touch /var/log/3cx-freshdesk.log
    $ sudo chmod 660 /var/log/3cx-freshdesk.log
    $ sudo chown $(whoami):staff /var/log/3cx-freshdesk.log
    ```
## Usage
1. From a terminal :

   ```
   $ python 3cx_call.py --help
   $ python 3cx_call.py --number +33836656565
   ```
2. from 3CX softphone on macOS :
Go to parameter --> Advanced --> Enable execute program on inbound calls and put

Path :
   ```
   /Users/myuser/.local/share/virtualenvs/3cx-call-to-freshdesk-ticket-rz7dl8z3/bin/python #you can know this dir using which python in the pipenv shell
   ```     
Parameters :
   ```
   --args /Users/myuser/path_of_3cx-call-to-freshdesk-ticket/3cx_call.py --number %CallerNumber%
   ```

## Configuration
1. Config file
The configuration file needs to be here
```
/Users/myuser/path_of_3cx-call-to-freshdesk-ticket/
```
It needs to be this format
```
[freshdesk]
domain = company.freshdesk.com
api_key = your_api_key
agent_id = your_agent_id
name = the name that will be displayed in the subject
group_id = your_group_id
```
