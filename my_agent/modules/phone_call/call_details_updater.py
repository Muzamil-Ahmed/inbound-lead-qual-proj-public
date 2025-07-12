from my_agent.utilis.schemas import AgentState, CallDecisionEvaluation
from typing import Literal, Optional
from langgraph.types import Command
from my_agent.modules.outreach.email_outreach import send_email_general

def update_call_details_insufficient_info_node(state: AgentState) -> dict:
    # This node is specifically for updating call details when information is insufficient (Agent decides to not call).
    call_details = state.get('call_details', {}) or {}
    evaluation_result = state.get('call_decision_evaluation', {})
    
    call_details['call_status'] = 'Not Called'
    call_details['call_successful'] = 'Unsuccessful'
    call_details['reason'] = evaluation_result.get('reason', 'Insufficient information for a personalized call')
    call_details['transcript'] = None
    call_details['call_summary'] = None

    form_data = state.get('form_data', {})
    first_name = form_data.get('first_name', '')
    email = form_data.get('email', '')
    
    if email:
        send_email_general(
            name=first_name,
            email=email
        )

    return {'call_details': call_details} 
