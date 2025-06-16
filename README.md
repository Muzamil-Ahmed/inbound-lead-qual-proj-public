[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/muzammil-kma/)

#### **What is this Project?**
LeadSense, is a production ready project that helps you know all you need to know to close your leads more. Essentially it calls your leads to engage, nurture and qualify them. 
It brings various benefits depending on your needs. It can help you either close easier on first call, engage the lead so they dont ghost you, give a great first impression etc. #BuildWithVapi

**Watch The Demo:** https://www.linkedin.com/feed/update/urn:li:activity:7339917729220440064/
**My LinkedIn:** https://www.linkedin.com/in/muzammil-kma/


---

#### **How it works?**
![langgraph dia](https://github.com/user-attachments/assets/55a8593a-5af5-43ed-a219-cc32206deb5f)


This project is composed of 5 core modules (located in the `my_agent/modules` folder):

1. **Trigger**
2. **Lead Research**
3. **Phone Call**
4. **Email Outreach**
5. **CRM Update**

These core modules help create a scalable and easily manageable project


#### **Project Flow**

1. **Trigger Module**  
    A webhook is triggered when a new Typeform submission is received, starting the agent workflow.
2. **Research Module**  
    The agent conducts research on the lead’s **LinkedIn profile** and **company website** using AI tools.  
    
    It then evaluates whether there’s enough personalized context to proceed with a phone call.
    - If **insufficient data** is found:  
        → The agent ends early and sends a **generic outreach email** with a meeting link.
    - If **sufficient data** is available:  
        → The agent proceeds to the phone call step.
	
3. **Call Module**  
    A personalized call is initiated using **Vapi**, powered by the earlier research.  
    The call qualifies the lead further or gathers relevant project details.
4. **Outreach Module**  
    After the call, a **follow-up email** is automatically sent with a meeting link and relevant context.
5. **CRM Module**  
    The entire interaction—including research, call outcome, and lead status—is logged into a **Google Sheets-based CRM**.    


###### **Technical Breakdown**

- **Vapi** – Used to create and manage real-time AI voice calls.
- **LangGraph** – Agent framework used to build the step-by-step workflow logic.
- **OpenAI:** This is the LLM provider, can easily be switched
- **FastAPI** – Lightweight web server that handles incoming Typeform webhooks.
- **Relevance AI Tools** – Used for LinkedIn research, web scraping, and Google Sheets updates — all through unified APIs with a generous free tier.

**Why this stack?**
- Minimal setup time
- Strong ecosystem support
- Easy debugging and modularity
- Scales well for multiple lead sources


---

## **How to setup and run locally:**

Prerequisites:
You should be familiar with tech like Langgraph, Vapi, FastAPI and general things like git, docker etc...

#### **1. Project Setup**

**1.1. Clone the Repository**

First, clone the project repository to your local machine:

```bash
git clone https://github.com/Muzamil-Ahmed/inbound-lead-qual-proj-public
```

**1.3. Install Dependencies**

Install all required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

**1.3. Configure Environment Variables**

Create a `.env` file in the root directory of your project (same level as `requirements.txt`).
For now, just fill in the OpenAI API key and Langsmith API Key (Langsmith is optional as it is just a free tracing, logging and debugging platform)

```
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
OPENAI_API_KEY=
RELEVANCEAI_API_KEY=
TWILIO_PHONE_NUMBER_ID_FROM_VAPI=
VAPI_ASSISTANT_ID=
VAPI_PRIV_API_KEY=
```

---
#### **2. Typeform Setup:**

Typeform is the trigger for this agent, you may make a custom trigger as well depending on your needs

**2.1. Create Your Typeform Form**

1.  Go to [Typeform](https://www.typeform.com/) and create a new form.
2.  Ensure your form includes the following fields as they are required by this agent:
	- First Name
	- Last Name
	- Email Address
	- Phone Number
	- Company Name
	- Company Website
	- LinkedIn URL
	- Business Area (where lead wants to apply AI)

**2.2. Configure Typeform Webhook**

1.  In your Typeform form editor, go to **Connect > Webhooks**.
2.  Click **Add a webhook**.
3.  For the **URL**, you will use the public URL of your FastAPI application's webhook endpoint. You will get this URL after starting `ngrok` (we will set this up at the end). The expected path for the webhook is usually `/webhook` or `/typeform-webhook`. For example: `https://your-ngrok-url.ngrok.io/webhook`.
4.  Set the **Method** to `POST`.

**2.3. Update webhook Code

In `webhook.py`, you have to make sure the field ids are entered for the respective variables meaning that for each fieldd in typeform, get the field id(from typeform) and paste it with it's corresponding key in FormData.

The keys in get_answer() function need to be replaced with your typeform field keys:

```py
	'first_name': get_answer('0WkL1GvPhkWG'),
	'last_name': get_answer('eI0bGlmzOGmk'),
	'email': get_answer('djcKwtbeF8iu', key='email'),
	'phone_number': get_answer('Uh6UTKzDhQ4E', key='phone_number'),
	'company': get_answer('9Fms4C4vLX8T'),
	'company_website': get_answer('Dj2CjNSgeBNW'),
	'linkedin_url': get_answer('ykv0e8GKUSEK', key='url'),
	'business_area': get_answer('WkY0qjrlB4rV'),
```

---
#### **3. Vapi Setup**

**5.1. Create a Vapi Account**

1. Go to [Vapi](https://vapi.ai/) and sign up for an account. (You receive 10 free credits ($10))
2. Go to Vapi API Keys, copy your Private API Key and update `VAPI_PRIV_API_KEY` in `.env`

**5.2. Create and Configure a Vapi Assistant**

1. In your Vapi dashboard, navigate to **Assistants**.
2. Click **Create Assistant**. You can keep most settings the same, just update the following
3. Update the assistant prompt with the prompt available in [prompts.py](./my_agent/utilis/prompts.py)
4. Set first message as "Hi, is this {{ full_name }}?"
5. Update summary prompt with the summary prompt available in [prompts.py](./my_agent/utilis/prompts.py)
6. After creating your assistant, you will see its **Assistant ID** in the Vapi dashboard. Copy this ID and update it to your `.env` file as `VAPI_ASSISTANT_ID`. 

**5.3. Set up phone number**

If you're located **outside the US**, you won't be able to use Vapi's default free number, as it only supports US-based calling.

To make it work globally, you’ll need to integrate **Twilio** with Vapi. Here’s how:

1. **Create a Twilio account**: You’ll get free credits and a phone number upon signing up.
2. **Get basic credentials from Twilio:** This includes Phone Number, Token and SID
3. **Import your Twilio number into Vapi** – Vapi has a simple integration flow for this.
4. **Update `.env` with Vapi Phone Number ID:** After importing Twilio number you will get a Phone number id (top right), copy it and paste it into `.env`
![Twilio phone number id](https://github.com/user-attachments/assets/b12e4169-a684-4a3f-9abe-58ba5c47c237)


> **Important Notes:**
- On Twilio’s free plan, you can **only call verified numbers** (i.e., numbers you physically have access to and confirmed in your Twilio console).
- You must **enable your country** in Twilio's [Geographic Permissions settings](https://console.twilio.com/us1/develop/voice/settings/geo-permissions).  
    For example, if your number is from Pakistan, make sure to enable Pakistan in the list otherwise you wont be able to call your number


---
#### **4. Relevance AI Setup**

**4.1: Import tools into Relevance AI**

In this [google drive](https://drive.google.com/drive/folders/1qvepRSjbA3eZylDarVk_R3kyZN1O-Cfx?usp=sharing) link there are .rai files present, download them and then import them in Relevance AI in the tools section

![image](https://github.com/user-attachments/assets/996efe19-f676-4e16-9cfb-df128f0ee891)

**4.2: Get API Key and URL for each Tool:**

(NOTE: The more efficient and better way is to just use Relevance AI Python SDK but this way works as well)

1. Generate API Key: First go to any tool, then click USE, then click API and then scroll down and generate API key and update it in `.env`
2. For each tool there is a unique URL, copy it and at every place in the code where the tool is used, paste that URL there. This includes Research, Outreach and CRM module.

**4.3: Update Tools:**

Some tools need to be updated with specific values or changes

1. **Email Tools:** Update the text so that it matches you as the sender
2. **Google Sheet:** Create your spreadsheet and paste the spreadsheet id in the given place in POST request URL

NOTE: Also make sure for Email and Google Sheets to connect to your google account first in RelevanceAI

---
#### **5. Run the Agent:**


**5.1. Run FastAPI**

In your terminal in root directory of the project, start up FastAPI using uvicorn with the following command:

```shell
uvicorn my_agent.modules.trigger.webhook:app --reload --port 8000
```

Now your webhook is up and running, but it is only running locally yet.


**5.2. Testing application locally:**

Before going to Typeform to send requests, you should first test it locally, to do so, you can send a test request to the FastAPI webhook using the following script.

However before doing so, edit the JSON data in (test.py) with your email address and phone number. 

Then run the following command at root of the folder to send test request and ensure if the whole agent and every module is working:

```shell
python .\my_agent\modules\trigger\test.py
```


**5.3. Testing with Typeform:**

Since Typeform needs to send data to your local machine, you'll use `ngrok` to create a public URL for your FastAPI application.

1.  If you don't have `ngrok`, download and install it from [ngrok.com](https://ngrok.com/).
2.  Open a new terminal window.
3.  Start `ngrok` to expose your FastAPI server's port (default is 8000):

    ```bash
    ngrok http 8000
    ```
    `ngrok` will provide you with a public URL (e.g., `https://abcdef123456.ngrok.io`). This is the URL you will use in your Typeform webhook configuration.


Now the link you get, input that link into Typeform webhook section in the following structure: https://your-ngrok-url.ngrok.io/typeform-webhook


Now simply fill up the Typeform and see the agent in action


---
#### **6. (Optional) Deploying the Agent:**

You may also deploy the agent on any cloud platform.

Simply use the Dockerfile which is already in the project and build and deploy a Docker image to any cloud platform, I personally used used Google Cloud Run but you may choose any.
