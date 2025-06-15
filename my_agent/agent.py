from langgraph.graph import StateGraph, START, END
from my_agent.utilis.schemas import AgentState, CallDecisionEvaluation
from my_agent.modules.research.lead_linkedin_reasearch import lead_research_node
from my_agent.modules.crm.update_crm import update_crm_node
from my_agent.modules.phone_call.vapi_call import vapi_call_node
from my_agent.modules.phone_call.personalized_script import personalized_call_intro_node
from my_agent.modules.phone_call.call_details_updater import update_call_details_insufficient_info_node
from my_agent.utilis.prompts import EVALUATE_SUMMARY_QUALITY_PROMPT
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import Literal

# Initializing the StateGraph with the AgentState schema to define the agent's workflow.
graph_builder = StateGraph(AgentState)

# Setting up the LLM for evaluating call readiness.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
structured_llm = llm.with_structured_output(CallDecisionEvaluation)


def evaluate_lead_info_sufficiency(state: AgentState) -> Literal["generate_personalized_line", "update_call_details_insufficient_info"]:
    # Extracting summaries from the current state to evaluate.
    lead_summary = state.get('research_data', {}).get('lead_summary', '')
    company_summary = state.get('research_data', {}).get('company_summary', '')
    
    # Formatting the prompt for the LLM to assess summary quality.
    prompt = EVALUATE_SUMMARY_QUALITY_PROMPT.format(
        lead_summary=lead_summary or "Not Available",
        company_summary=company_summary or "Not Available"
    )
    # Invoking the LLM to get a structured evaluation.
    response = structured_llm.invoke(prompt)
    
    print(response)
    # Store the evaluation result in the state for later use.
    state['call_decision_evaluation'] = response.dict()

    # Based on the evaluation, decide whether to proceed with a personalized line or update CRM.
    if response.result == 'insufficient':
        print("Conditional edge reult: Insufficient data for call")
        # If information is insufficient, route to the node that updates call details and then CRM.
        return "update_call_details_insufficient_info"
    else:
        print("Conditional edge reult: Sufficient data, proceeding to call")
        # If information is sufficient, proceed to generate a personalized line.
        return "generate_personalized_line"



# Defining the nodes for the LangGraph agent.
graph_builder.add_node("lead_linkedin_research", lead_research_node)
graph_builder.add_node("generate_personalized_line", personalized_call_intro_node)
graph_builder.add_node("call", vapi_call_node)
graph_builder.add_node("update_crm", update_crm_node)
graph_builder.add_node("update_call_details_insufficient_info", update_call_details_insufficient_info_node)

# Setting the entry point for the graph.
graph_builder.set_entry_point("lead_linkedin_research")

# Adding a conditional edge from the lead research node based on summary sufficiency.
graph_builder.add_conditional_edges(
    "lead_linkedin_research",
    evaluate_lead_info_sufficiency,
    {
        "generate_personalized_line": "generate_personalized_line",
        "update_call_details_insufficient_info": "update_call_details_insufficient_info"
    }
)

# Defining the linear flow for successful paths.
graph_builder.add_edge("generate_personalized_line", "call")
graph_builder.add_edge("call", "update_crm")
graph_builder.add_edge("update_call_details_insufficient_info", "update_crm")
graph_builder.add_edge("update_crm", END)


# Compiling the graph to create the runnable agent.
graph = graph_builder.compile()

