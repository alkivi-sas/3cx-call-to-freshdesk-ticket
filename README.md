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