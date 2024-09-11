import requests
import os
import json

def setup_agent(payload = None):
    url = 'https://promptemplate.booksy.us.boostedchat.com/agentSetup/'
    print(url)
    resp = requests.post(url, data=json.dumps(payload),headers = {'Content-Type': 'application/json'})
    response = resp.json()
    return response

