import logging
import json
import requests

payload = {
  "event": "onExternalEventHandler",
  "data": "{ \"number\": \"+33767808727\" }",
  "headers": {
    "Content-Type": "application/json"
  }
  }

url = 'http://localhost:10001/web/events/onExternalEvent'
data = {'phoneNumber': '+33767808727'}
data = {}
x = requests.post(url, params=payload, headers = {"Content-Type": 'application/json'})
logging.warning(x, vars(x))
