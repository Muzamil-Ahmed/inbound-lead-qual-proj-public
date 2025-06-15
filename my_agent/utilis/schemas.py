from typing import TypedDict, Optional
from pydantic import BaseModel, Field

LANGGRAPH_URL = "http://localhost:2024"

# Defining the structure for incoming form data from Typeform.
class TypeformFormData(TypedDict):
    event_id: str
    form_id: str
    submitted_at: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    company: str
    company_website: str
    linkedin_url: str
    business_area: str

# Defining the structure for research data collected by the agent.
class ResearchData(TypedDict, total=False):
    lead_summary: Optional[str]
    company_linkedin_url: Optional[str]
    company_summary: Optional[str]
    personalized_call_intro: Optional[str]


# Defining the structure for details related to the phone call.
class CallDetails(TypedDict, total=False):
    call_status: str  # Indicates if a call was 'Called' or 'Not Called'.
    call_successful: Optional[bool]  # Indicates 'Successful', 'Unsuccessful', or None if not evaluated.
    reason: Optional[str] # Provides a reason for call status if applicable.
    call_summary: Optional[str]  # Stores the summary of the call from Vapi analysis.


# Pydantic model for evaluating the sufficiency of information for a call.
class CallDecisionEvaluation(BaseModel):
    """This model evaluates whether I have sufficient information to call the lead."""
    result: str = Field(description="Indicates if information is 'sufficient' or 'insufficient'")
    reason: Optional[str] = Field(default=None, description="Provides a reason if the information is deemed insufficient.")

# Defining the overall state structure for my LangGraph agent.
class AgentState(TypedDict):
    form_data: TypeformFormData
    research_data: ResearchData
    call_details: CallDetails
    call_decision_evaluation: Optional[CallDecisionEvaluation]
