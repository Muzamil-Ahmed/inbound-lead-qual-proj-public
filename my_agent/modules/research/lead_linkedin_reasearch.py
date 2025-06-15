import requests
import json
import os
from my_agent.utilis.schemas import AgentState
from my_agent.utilis.prompts import LEAD_SUMMARY_GENERATOR_PROMPT, LEAD_COMPANY_RESEARCH_PROMPT
from my_agent.utilis.helpers import is_valid_url
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel, Field

# API endpoints for lead and company research tools.
LINKEDIN_RESEARCH_API_URL = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/c38fb70e-ed5a-4c7e-9a4d-53f4b5c04482/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0'
COMPANY_RESEARCH_API_URL = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/b0fd3c1a-71d0-4073-9999-88c5f45c795c/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0'

# Loading API key from environment variables.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RELEVANCEAI_API_KEY = os.getenv("RELEVANCEAI_API_KEY")

# Headers for API requests.
headers = {
    "Content-Type": "application/json",
    "Authorization": RELEVANCEAI_API_KEY,
}

# Initializing the LLM for summarization tasks.
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Structured output schema
class LinkedInResearch(BaseModel):
    """Structured output format for LinkedIn research results."""
    lead_summary: Optional[str] = Field(description="A summary of the lead's profile.", default=None)
    primary_company_linkedin_url: Optional[str] = Field(description="The LinkedIn URL of the lead's primary company.", default=None)

structured_linkedin_llm = llm.with_structured_output(LinkedInResearch)



def lead_research_node(state: AgentState):
    # Extracting data from the current state for lead and company research.
    linkedin_url = state.get('form_data', {}).get('linkedin_url')
    research_data = state.get('research_data', {})
    company_website_url = state.get('form_data', {}).get('company_website', None)

    linkedin_data = None
    # --- Performing LinkedIn Research for the Lead ---
    if linkedin_url:
        try:
            # Calling the LinkedIn research API.
            response_linkedin = requests.post(
                LINKEDIN_RESEARCH_API_URL,
                headers=headers,
                data=json.dumps({"linkedin_url": linkedin_url})
            )
            if response_linkedin.status_code == 200:
                linkedin_data = response_linkedin.json()
                print(f"Successfully fetched LinkedIn data for {linkedin_url}.")
            else:
                print(f"Failed to fetch LinkedIn data for {linkedin_url}. Status code: {response_linkedin.status_code}")
                research_data['lead_summary'] = None
                research_data['company_linkedin_url'] = None
        except Exception as e:
            print(f"Error during LinkedIn API call for {linkedin_url}: {e}")
            research_data['lead_summary'] = None
            research_data['company_linkedin_url'] = None

        # Summarizing the LinkedIn data using the LLM.
        if linkedin_data:
            try:
                profile_str = json.dumps(linkedin_data.get('data', {}), indent=2)
                prompt = LEAD_SUMMARY_GENERATOR_PROMPT.format(linkedin_profile=profile_str)

                print(f"\n##### Invoking LLM for Lead Summary with the following prompt: #####\n\n{prompt}\n")
                response_struct = structured_linkedin_llm.invoke(prompt)
                
                research_data['lead_summary'] = response_struct.lead_summary if response_struct.lead_summary else None
                research_data['company_linkedin_url'] = response_struct.primary_company_linkedin_url if response_struct.primary_company_linkedin_url else None
                print(f"Lead summary generated: {research_data['lead_summary'][:100]}...")
                print(f"Primary company LinkedIn URL extracted: {research_data['company_linkedin_url']}")
            except Exception as e:
                print(f"Error summarizing LinkedIn data with LLM: {e}")
                research_data['lead_summary'] = None
                research_data['company_linkedin_url'] = None
        else:
            print("No LinkedIn data to summarize.")
    else:
        print("No LinkedIn URL provided in form data.")
        research_data['lead_summary'] = None
        research_data['company_linkedin_url'] = None

    # --- Performing Company Research ---

    # Validating company URLs before proceeding with company research.
    company_linkedin_url = research_data.get('company_linkedin_url')
    valid_company_linkedin_url = company_linkedin_url if is_valid_url(company_linkedin_url) else None
    valid_company_website_url = company_website_url if is_valid_url(company_website_url) else None

    # If neither company LinkedIn nor website URL is valid, skip company research.
    if not valid_company_linkedin_url and not valid_company_website_url:
        research_data['company_summary'] = None
        print("No valid company LinkedIn or website URL available for company research.")
        return {'research_data': research_data}

    # Calling the Company Research API. (This reseraches both the LinkedIn company profile and the company website)
    try:

        company_headers = {
            "Content-Type": "application/json",
            "Authorization": RELEVANCEAI_API_KEY
        }
        company_payload = {
            "company_linkedin_url": valid_company_linkedin_url or "None",
            "company_website_url": valid_company_website_url or "None"
        }
        response_company = requests.post(
            COMPANY_RESEARCH_API_URL,
            headers=company_headers,
            data=json.dumps(company_payload)
        )
        if response_company.status_code != 200:
            print(f"Failed to fetch company data. Status code: {response_company.status_code}")
            research_data['company_summary'] = None
            return {'research_data': research_data}
        company_data = response_company.json()
        print(f"Successfully fetched company data for {valid_company_linkedin_url or valid_company_website_url}.")
    except Exception as e:
        print(f"Error during Company API call: {e}")
        research_data['company_summary'] = None
        return {'research_data': research_data}

    # Preparing the lead's current experience string for the company research prompt.
    experiences = linkedin_data.get('data', {}).get('experiences', []) if linkedin_data else []
    current_experiences = []
    for exp in experiences:
        if exp.get('is_current', False):
            lines = [f"##### {exp.get('company', '')}"]
            for key, value in exp.items():
                if isinstance(value, str) and len(value) > 50:
                    lines.append(f"{key} -\n    {value}")
                else:
                    lines.append(f"{key} - {value}")
            current_experiences.append("\n".join(lines))
    experience_str = "\n\n".join(current_experiences) if current_experiences else "Not Available"

    # Summarizing the company profile using the LLM.
    try:
        prompt = LEAD_COMPANY_RESEARCH_PROMPT.format(
            linkedin_profile_experience=experience_str or "Not Available",
            company_linkedin_profile=json.dumps(company_data.get('linkedin_profile', {}) or "Not Available", indent=2),
            company_website=json.dumps(company_data.get('website', {}) or "Not Available", indent=2)
        )
        print(f"\n##### Invoking LLM for Company Summary with the following prompt: #####\n\n{prompt}\n")
        company_summary_response = llm.invoke(prompt)
        research_data['company_summary'] = str(company_summary_response)
        print(f"Company summary generated: {research_data['company_summary'][:100]}...")
    except Exception as e:
        print(f"Error summarizing company data with LLM: {e}")
        research_data['company_summary'] = None

    print(f"Final research data for state: {research_data}")
    return {'research_data': research_data}
