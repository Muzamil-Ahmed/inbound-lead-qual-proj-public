# This module is responsible for generating a personalized introduction line for the outbound phone call.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from my_agent.utilis.prompts import GENERATE_PERSONALIZED_LINE_FOR_CALL_INTRO
from my_agent.utilis.schemas import AgentState

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

def personalized_call_intro_node(state: AgentState):
    # Extracting necessary information from the agent's state to craft the personalized intro.
    form_data = state.get('form_data', {})
    research_data = state.get('research_data', {})
    name = form_data.get('first_name', '')
    lead_summary = research_data.get('lead_summary', '')
    company_summary = research_data.get('company_summary', '')
    automation_needs = form_data.get('business_area', '')

    # Formatting the prompt for the LLM to generate the personalized line.
    prompt = GENERATE_PERSONALIZED_LINE_FOR_CALL_INTRO.format(
        name=name or "Not Available",
        lead_summary=lead_summary or "Not Available",
        company_summary=company_summary or "Not Available",
        automation_needs=automation_needs or "Not Available"
    )

    # Invoking the LLM and saving the generated personalized line to the research data.
    response = llm.invoke(prompt)
    personalized_line_content = getattr(response, 'content', str(response))
    research_data['personalized_call_intro'] = personalized_line_content
    print(f"Generated personalized call intro: {personalized_line_content[:50]}...")
    
    return {'research_data': research_data}
