# These functions handle sending follow-up emails based on call outcomes.

import os
import requests
import json
from dotenv import load_dotenv

def send_email_after_call(name, email):
    load_dotenv()
    API_KEY = os.getenv("RELEVANCEAI_API_KEY")
    url = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/d7bb04d5-3580-48de-9989-df6bc9dd5f4c/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0'
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY
    }
    payload = {
        "name": name,
        "email": email
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"Email after successful call sent to {name} ({email}). Response: {response.text}")
    except Exception as e:
        print(f"Failed to send email after successful call to {name} ({email}): {e}")

def send_email_general(name, email):
    load_dotenv()
    API_KEY = os.getenv("RELEVANCEAI_API_KEY")
    url = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/5236f061-da1a-431c-8c65-7192a80a9d3f/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0'
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY
    }
    payload = {
        "name": name,
        "email": email
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"General email sent to {name} ({email}). Response: {response.text}")
    except Exception as e:
        print(f"Failed to send general email to {name} ({email}): {e}")
    
