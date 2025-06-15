# Project Overview
You are building an inbound lead qualification agent where inbound leads will be received through a form. The Agent will research the lead and then Agent will call and engage the leads and qualify them on certain criterias if needed and CRM (Goolge Sheets) will be updated.

You will be using Langgraph to orchestrate and make this agent.

# Special Instruction regarding Project:

This is supposed to be a versatile and scalable project that can be adapted to various use cases such as SaaS Demo Bookings, Home Care Services, Real Estate, "Work With Us" Bookings etc. Every individual component should be as independent as possible and easily swapable. Project structure is very important. Project should be made in a way that in the future I can easily add/swap/remove any feature and I am not constrained.

Current you are building focusing on "Work With Me" use case which is essentially for an individual or company where a lead wants to get the services of that country so the click with "Contact Us" or "Work with Us" button and fill a form. I will refer to this use-case as "Service Booking" usecase from now onwards.

# Key Functionalities
1. System gets triggered when new lead fills the fomr
    1. When the lead fills the form, the system will get triggered
    2. The basic information that will be collected will vary from use-case to use-case but for our current use case following information will be taken: {Full Name, Email, Phone Number, Company Name, Role in the company}
2. Researching the lead
    1. Using the infromation present in the form, the agent will research the lead
    2. For our Service Bokking use-case, this includes the LinkedIn Profile Summary, the Company Website Summary
3. Voice call the lead after reasearch
    1. With the Research done, the Agent will call the lead with personalized intro etc..
4. Sends whatsapp and email to the lead
    1. If lead is qualified for the Service, Agent will send a Message on Whatsapp and Email the Lead with Calendar Invite
5. Update Google Sheet CRM with lead data
    1. Lastly, append each row with Lead Data collected from form along with result of call: {"Call Status"(Successful or not), "Service Needs"(what client wants), "Qualification Score"(From 1-5)}


# Docs

Use MCP to Access Langgraph Docs

## Documentation on How to invoke API for Relevance AI tools that are going to be used in this project
(Includes tools for seraching lead, getting LinkedIn Data, getting Company Data etc..)
Relevance AI API Key: "9f29c56db4a1-4f95-9ff7-61e33a82cfd0:sk-ZjVhNGEyMGEtZTUzZS00MTQyLWJjNjMtNzA1OWJmMTM3NmE2"
URL will be Different for Each tool and will be specified when I tell you

CODE_EXAMPLE:
```
requests.post('https://api-d7b62b.stack.tryrelevance.com/latest/studios/141a525c-9939-46c8-ad60-b2f3a17a1509/trigger_webhook?project=9f29c56db4a1-4f95-9ff7-61e33a82cfd0', 
  headers={"Content-Type":"application/json","Authorization":"YOUR_API_KEY"},
  data=json.dumps({"company_url":"","name":""})
)
```

# Current File Structure

INBOUND-LEAD-QUALIFICATION-LANGGRAPH
├── .env
├── instructions.md
├── langgraph.json
└── my_agent
    ├── agent.py
    └── utilis
        ├── nodes.py
        ├── prompts.py
        ├── schemas.py
        └── tools.py

