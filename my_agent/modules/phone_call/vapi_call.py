import os
from dotenv import load_dotenv
from my_agent.utilis.schemas import AgentState, CallDetails
from my_agent.modules.outreach.email_outreach import send_email_after_call, send_email_general
import asyncio
from vapi import AsyncVapi
from vapi.core.api_error import ApiError


# This node is the meat of the project, it handles the main Vapi phone call and updates state accordingly
async def vapi_call_node(state: AgentState):
    load_dotenv()
    VAPI_API_KEY = os.getenv("VAPI_PRIV_API_KEY")
    VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
    TWILIO_PHONE_NUMBER_ID = os.getenv("TWILIO_PHONE_NUMBER_ID_MUZAMMIL_FROM_VAPI") 

    # Early exit if essential Vapi credentials are missing
    if not VAPI_API_KEY or not VAPI_ASSISTANT_ID or not TWILIO_PHONE_NUMBER_ID:
        error_message = "Missing Vapi environment variables. Skipping Vapi call."
        print(error_message)
        # Ensure call_details is a CallDetails object
        if not isinstance(state.get('call_details'), CallDetails):
            state['call_details'] = CallDetails()
        
        state['call_details']['call_status'] = 'Not Called'
        state['call_details']['call_successful'] = False
        state['call_details']['reason'] = error_message
        send_email_general(
            name=f"{state.get('form_data', {}).get('first_name', '')} {state.get('form_data', {}).get('last_name', '')}".strip() or "Valued Lead",
            email=state.get('form_data', {}).get('email', '')
        )
        return state

    # Extract necessary variables from the current agent state.
    form_data = state.get('form_data', {})
    research_data = state.get('research_data', {})
    call_details = state.get('call_details', {}) or {}
    name = form_data.get('first_name', '')
    last_name = form_data.get('last_name', '')
    full_name = f"{name} {last_name}".strip()
    email = form_data.get('email', '')
    customer_number = form_data.get('phone_number', '')
    automation_needs = form_data.get('business_area', '')
    personalized_line = research_data.get('personalized_call_intro', '')
    
    # Ensure personalized_line is a string, even if empty
    if not isinstance(personalized_line, str):
        personalized_line = str(personalized_line or "")

    # Early exit if no phone number is found
    if not customer_number:
        warning_message = "No phone number found for lead. Skipping Vapi call."
        print(f"WARNING: {warning_message}") # Use print for immediate feedback
        call_details['call_status'] = 'Not Called'
        call_details['call_successful'] = False # Always boolean
        call_details['reason'] = warning_message
        send_email_general(
            name=full_name,
            email=email
        )
        state['call_details'] = call_details
        return state

    # Set up overrides for the Vapi assistant with dynamic values from the lead data.
    assistant_overrides = {
        "variableValues": {
            "full_name": full_name or "",
            "name": name or "",
            "automation_needs": automation_needs or "",
            "personalized_line": personalized_line or ""
        }
    }

    # Define the customer's phone number for the Vapi call.
    customer = {
        "number": customer_number
    }

    # Initialize local flag for this attempt. Will be updated based on Vapi response.
    call_successful_this_attempt = False 

    try:
        # Initialize the Vapi client with my API key.
        client = AsyncVapi(token=VAPI_API_KEY)

        print(f"Vapi Call Payload:")
        print(f"  Assistant ID: {VAPI_ASSISTANT_ID}")
        print(f"  Phone Number ID: {TWILIO_PHONE_NUMBER_ID}")
        print(f"  Customer: {customer}")
        print(f"  Assistant Overrides: {assistant_overrides}")

        # Initiate the outbound call using Vapi.
        response = await client.calls.create(
            assistant_id=VAPI_ASSISTANT_ID,
            phone_number_id=TWILIO_PHONE_NUMBER_ID,
            customer=customer,
            assistant_overrides=assistant_overrides
        )
        print(f"Vapi SDK call initiated. Response: \n\n{response}\n")

        # Over here we are using polling to get the call_detils after call has ended, surely it is not the most elegant solution however it just works
        call_id = getattr(response, 'id', None)
        poll_attempts = 0
        max_attempts = 60
        call_obj = None

        if call_id:
            while poll_attempts < max_attempts:
                try:
                    call_obj = await client.calls.get(id=call_id)
                    status = getattr(call_obj, 'status', None)
                    ended_reason = getattr(call_obj, 'ended_reason', None)
                    
                    print(f"Polling Vapi call status (attempt {poll_attempts + 1}): status={status}, ended_reason={ended_reason}")
                    
                    if status == 'ended':
                        print(f"Vapi call ended with status: {status}, reason: {ended_reason}")
                        break
                except Exception as poll_exc:
                    print(f"Error while polling Vapi call status for call ID {call_id}: {poll_exc}")
                await asyncio.sleep(6)
                poll_attempts += 1
        else:
            print("Vapi call ID not received. Cannot poll status.")

        # Process the call details once the call has ended or polling timed out.
        if call_obj is not None and getattr(call_obj, 'status', None) == 'ended':
            analysis = getattr(call_obj, 'analysis', None)
            messages = getattr(call_obj, 'messages', None)
            # Prefer ended_reason from analysis if available, otherwise from call_obj
            ended_reason = getattr(analysis, 'ended_reason', None) if analysis else getattr(call_obj, 'ended_reason', None)
            success_eval = getattr(analysis, 'success_evaluation', None) if analysis else None
            summary = getattr(analysis, 'summary', None) if analysis else None
            
            call_details['call_status'] = 'Called'
            # Store boolean success_eval directly, default to False if None
            call_details['call_successful'] = bool(success_eval) if success_eval is not None else False 
            if not call_details['call_successful']:
                call_details['reason'] = ended_reason
            if summary:
                call_details['call_summary'] = summary
            
            # Set the local flag for email sending based on the actual success_eval
            call_successful_this_attempt = call_details['call_successful']

            print("Vapi call details processed.")
        else:
            # If call_obj is None or status is not 'ended', it's an unsuccessful call
            call_details['call_status'] = 'Not Called'
            call_details['call_successful'] = False
            call_details['reason'] = 'Call was unsuccesful (Call polling timed out)'
            print("Vapi call polling timed out or failed to retrieve call object or call did not end successfully.")
        
        # Send a follow-up email based on call success/failure.
        if call_successful_this_attempt:
            send_email_after_call(full_name, email)
            print(f"Sent successful call follow-up email to {full_name} at {email}.")
        else:
            send_email_general(full_name, email)
            print(f"Sent general follow-up email to {full_name} at {email} due to unsuccessful call.")

    except ApiError as e:
        # Handle Vapi API specific errors.
        error_message = f"Vapi SDK call failed (ApiError): Status Code: {e.status_code}, Body: {e.body}"
        print(f"ERROR: {error_message}") # Keep print for immediate feedback
        call_details['call_status'] = 'Not Called'
        call_details['call_successful'] = False # Ensure boolean
        call_details['reason'] = error_message
        send_email_general(full_name, email)
    except Exception as e:
        # Handle any other unexpected errors during the Vapi call.
        error_message = f"Vapi SDK call failed due to an unexpected error: {e}"
        print(f"ERROR: {error_message}") # Keep print for immediate feedback
        call_details['call_status'] = 'Not Called'
        call_details['call_successful'] = False # Ensure boolean
        call_details['reason'] = error_message
        send_email_general(full_name, email)

    return {'call_details': call_details}





