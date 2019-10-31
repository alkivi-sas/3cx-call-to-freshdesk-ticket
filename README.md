##Configuration
1. Config file
The configuration file needs to be here
```
/Users/myuser/path_of_3cx-freshdesk/
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

2. 


## Usage
1. From a terminal :

   ```
   $ ./3cx_to_fresdesk.py -c +33836656565
   ```
2. from 3CX softphone on macOS :
Go to parameter --> Advanced --> Enable execute program on inbound calls and put

Path :
```
/Users/myuser/.local/share/virtualenvs/3cx-freshdesk-rz7dl8z3/bin/python #you can know this dir using which python in the pipenv shell
```     
Parameters :
```
--args /Users/myuser/path_of_3cx-freshdesk/3cx_to_API.py %CallerNumber%
```