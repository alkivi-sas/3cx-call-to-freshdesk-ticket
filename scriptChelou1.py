import os
import sys
import logging
import subprocess

logging.basicConfig(filename='/var/log/testChelou.log', level=logging.DEBUG)

logging.info(sys.argv[1])
process = subprocess.Popen(["/Users/alexandre/.local/share/virtualenvs/3cx-call-to-freshdesk-ticket-hejKzvKg/bin/python", "/Users/alexandre/3cx-call-to-freshdesk-ticket/3cx_call_test.py", sys.argv[1]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output, error = process.communicate()
logging.info(output)
logging.info(error)
