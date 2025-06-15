from fastapi import FastAPI, Request, BackgroundTasks
import json
from my_agent.utilis.schemas import TypeformFormData, AgentState, LANGGRAPH_URL, CallDetails
from my_agent.agent import graph
from langgraph_sdk import get_client
import uuid
from my_agent.modules.outreach.email_outreach import send_email_general
import logging # Import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_lead_in_background(form_data: TypeformFormData):

    # Can use later for thread id (state management)
    id = str(
        uuid.uuid4()
    )
    ### If Debugging with Langgraph Studio (UI thing) then use the following code:

        # if LANGGRAPH_URL is None:
        #     client = get_client(url="http://localhost:2024")
        # else:
        #     client = get_client(url=LANGGRAPH_URL)

        # agent_output = await client.runs.create(
        #             assistant_id="main", # Assistant id as specified in langgraph.json
        #             on_completion="keep", # Show stateless runs in UI Langgraph Studio 
        #             input={"form_data": form_data, "research_data": {}} 
        #         )


    ### Otherwise in production, it would be better to call the graph directly(Langsmith can be used for debugging):
    try:
        agent_output = await graph.ainvoke(
            input={"form_data": form_data, "research_data": {}, "call_details": {}}
        )
        print(f"Agent was 'succcessfully' executed. \nAgent Output:\n{agent_output}")
        logger.info("Agent execution successful.", extra={'final_agent_state': agent_output})
    except Exception as e:
        print(f"🚨 An unexpected error occurred during agent execution: {e}")
        logger.error("Agent execution failed.", exc_info=True, extra={'error': str(e), 'input_form_data': form_data})
        
        # Send general email with calendly link
        lead_name = f"{form_data.get('first_name', '')} {form_data.get('last_name', '')}".strip() or "Valued Lead"
        lead_email = form_data.get('email', '')
        # If for some reason the agent does not work, atleast the email with the calendly link gets sent
        if lead_email:
            send_email_general(
                name=lead_name, 
                email=lead_email
            )

@app.post("/typeform-webhook")
async def typeform_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    
    # Extract answers and map to fields
    answers = {a['field']['id']: a for a in data['form_response']['answers']}
    fields = {f['id']: f for f in data['form_response']['definition']['fields']}

    def get_answer(field_id, key='text'):
        a = answers.get(field_id)
        if not a:
            return None
        return a.get(key) or a.get('url') or a.get('email') or a.get('phone_number')

    form_data: TypeformFormData = {
        'event_id': data.get('event_id', ''),
        'form_id': data['form_response'].get('form_id', ''),
        'submitted_at': data['form_response'].get('submitted_at', ''),
        'first_name': get_answer('0WkL1GvPhkWG'),
        'last_name': get_answer('eI0bGlmzOGmk'),
        'email': get_answer('djcKwtbeF8iu', key='email'),
        'phone_number': get_answer('Uh6UTKzDhQ4E', key='phone_number'),
        'company': get_answer('9Fms4C4vLX8T'),
        'company_website': get_answer('Dj2CjNSgeBNW'),
        'linkedin_url': get_answer('ykv0e8GKUSEK', key='url'),
        'business_area': get_answer('WkY0qjrlB4rV'),
    }

    print("📥 Received data from Typeform:")
    print(json.dumps(data, indent=2))
    print("\nExtracted form data:")
    print(json.dumps(form_data, indent=2))

    logger.info("Webhook received. Processing lead.", extra={'form_data': form_data})


    background_tasks.add_task(process_lead_in_background, form_data)
    return {"status": "received"}
