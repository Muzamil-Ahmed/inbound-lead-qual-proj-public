import os
import requests
import json
from dotenv import load_dotenv
from my_agent.utilis.schemas import AgentState

def update_crm_node(state: AgentState):
    load_dotenv()
    API_URL = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/38199a99-39b4-4aa0-934b-f1092f18b2c3/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0'
    API_KEY = os.getenv("RELEVANCEAI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY,
    }
    
    # Extracting necessary data from the agent's state to prepare for CRM update.
    form_data = state.get('form_data', {})
    research_data = state.get('research_data', {})
    call_details = state.get('call_details', {})

    # Constructing the payload for the CRM update API call.
    payload = {
        "first_name": form_data.get('first_name', ''),
        "last_name": form_data.get('last_name', ''),
        "phone_number": form_data.get('phone_number', ''),
        "email": form_data.get('email', ''),
        "company_name": form_data.get('company', ''),
        "area_of_interest": form_data.get('business_area', ''),
        "linkedin_url": form_data.get('linkedin_url', 'Not available'),
        "company_website": form_data.get('company_website', 'Not available'),
        "lead_summary": research_data.get('lead_summary', 'Not available'),
        "call_status": call_details.get('call_status', ''),
        "call_success": str(call_details.get('call_successful', False)).lower(),
        "reason_unsuccessful": call_details.get('reason', ''),
        "call_summary": call_details.get('call_summary', 'Not available'),
    }

    try:
        # Sending the data to the CRM API.
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"CRM updated successfully for {payload.get('first_name')} {payload.get('last_name')}. Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to update CRM for {payload.get('first_name')} {payload.get('last_name')}: {e}")

    return {}
