import requests

# This one includes full proper data that leads to successful call
mock_data_1 = {
  "event_id": "01JVYWWWTT94QKGBXZVFZDBH7T",
  "event_type": "form_response",
  "form_response": {
    "form_id": "XWpEy83H",
    "token": "1vz4hzafpwf1jubdl1vz40vsffri7a48",
    "landed_at": "2025-05-23T15:37:54Z",
    "submitted_at": "2025-05-23T15:41:27Z",
    "definition": {
      "id": "XWpEy83H",
      "title": "My branded typeform",
      "fields": [
        {
          "id": "WkY0qjrlB4rV",
          "ref": "ddd56591-9dfa-4675-bae5-3866c6747493",
          "type": "short_text",
          "title": "Which areas of your business are you looking to apply AI in?",
          "properties": {}
        },
        {
          "id": "Dj2CjNSgeBNW",
          "ref": "44d1f884-422d-4288-8c60-96d92f433827",
          "type": "short_text",
          "title": "Company Website URL",
          "properties": {}
        },
        {
          "id": "ykv0e8GKUSEK",
          "ref": "7c81696f-7a29-479f-90b2-0a430723a79a",
          "type": "website",
          "title": "Your LinkedIn Profile URL",
          "properties": {}
        },
        {
          "id": "0WkL1GvPhkWG",
          "ref": "7a592946-bf21-478e-a135-3e8344c97ff4",
          "type": "short_text",
          "title": "First name",
          "properties": {}
        },
        {
          "id": "eI0bGlmzOGmk",
          "ref": "c5eae38b-f053-47ea-b248-31b0ec7998c7",
          "type": "short_text",
          "title": "Last name",
          "properties": {}
        },
        {
          "id": "Uh6UTKzDhQ4E",
          "ref": "a9de5a49-7f0e-4ade-accd-ffd88c7aaf55",
          "type": "phone_number",
          "title": "Phone number",
          "properties": {}
        },
        {
          "id": "djcKwtbeF8iu",
          "ref": "b43f4696-aaed-48fb-be44-165543dd9384",
          "type": "email",
          "title": "Email",
          "properties": {}
        },
        {
          "id": "9Fms4C4vLX8T",
          "ref": "78965f9a-d70b-4549-a68f-7d957842355b",
          "type": "short_text",
          "title": "Company",
          "properties": {}
        }
      ],
      "endings": [
        {
          "id": "Pg6ODmKDtRA8",
          "ref": "f5fa5381-bc5a-4997-9d9f-506d11faec12",
          "title": "Thank you for filling out the form!",
          "type": "thankyou_screen",
          "properties": {
            "description": "I will reach out to you shortly to book a call.",
            "button_text": "again",
            "show_button": False,
            "share_icons": False,
            "button_mode": "default_redirect"
          }
        }
      ],
      "settings": {
        "partial_responses_to_all_integrations": True
      }
    },
    "answers": [
      {
        "type": "text",
        "text": "Inbound Lead Qualification Agent",
        "field": {
          "id": "WkY0qjrlB4rV",
          "type": "short_text",
          "ref": "ddd56591-9dfa-4675-bae5-3866c6747493"
        }
      },
      {
        "type": "text",
        "text": "Chairman VaynerX and Vayner Media",
        "field": {
          "id": "Dj2CjNSgeBNW",
          "type": "short_text",
          "ref": "44d1f884-422d-4288-8c60-96d92f433827"
        }
      },
      {
        "type": "url",
        "url": "https://www.linkedin.com/in/garyvaynerchuk/",
        "field": {
          "id": "ykv0e8GKUSEK",
          "type": "website",
          "ref": "7c81696f-7a29-479f-90b2-0a430723a79a"
        }
      },
      {
        "type": "text",
        "text": "Gary",
        "field": {
          "id": "0WkL1GvPhkWG",
          "type": "short_text",
          "ref": "7a592946-bf21-478e-a135-3e8344c97ff4"
        }
      },
      {
        "type": "text",
        "text": "Vaynerchuk",
        "field": {
          "id": "eI0bGlmzOGmk",
          "type": "short_text",
          "ref": "c5eae38b-f053-47ea-b248-31b0ec7998c7"
        }
      },
      {
        "type": "phone_number",
        "phone_number": "+923008224731",
        "field": {
          "id": "Uh6UTKzDhQ4E",
          "type": "phone_number",
          "ref": "a9de5a49-7f0e-4ade-accd-ffd88c7aaf55"
        }
      },
      {
        "type": "email",
        "email": "kma.data.may2018@gmail.com",
        "field": {
          "id": "djcKwtbeF8iu",
          "type": "email",
          "ref": "b43f4696-aaed-48fb-be44-165543dd9384"
        }
      },
      {
        "type": "text",
        "text": "VaynerX and Vayner Media",
        "field": {
          "id": "9Fms4C4vLX8T",
          "type": "short_text",
          "ref": "78965f9a-d70b-4549-a68f-7d957842355b"
        }
      }
    ],
    "ending": {
      "id": "Pg6ODmKDtRA8",
      "ref": "f5fa5381-bc5a-4997-9d9f-506d11faec12"
    }
  }
}

# This one includes broken/missing data which is deemed inssufficient for call in evaluation node
mock_data_2 = {
  "event_id": "01JVYWWWTT94QKGBXZVFZDBH7T",
  "event_type": "form_response",
  "form_response": {
    "form_id": "XWpEy83H",
    "token": "1vz4hzafpwf1jubdl1vz40vsffri7a48",
    "landed_at": "2025-05-23T15:37:54Z",
    "submitted_at": "2025-05-23T15:41:27Z",
    "definition": {
      "id": "XWpEy83H",
      "title": "My branded typeform",
      "fields": [
        {
          "id": "WkY0qjrlB4rV",
          "ref": "ddd56591-9dfa-4675-bae5-3866c6747493",
          "type": "short_text",
          "title": "Which areas of your business are you looking to apply AI in?",
          "properties": {}
        },
        {
          "id": "Dj2CjNSgeBNW",
          "ref": "44d1f884-422d-4288-8c60-96d92f433827",
          "type": "short_text",
          "title": "Company Website URL",
          "properties": {}
        },
        {
          "id": "ykv0e8GKUSEK",
          "ref": "7c81696f-7a29-479f-90b2-0a430723a79a",
          "type": "website",
          "title": "Your LinkedIn Profile URL",
          "properties": {}
        },
        {
          "id": "0WkL1GvPhkWG",
          "ref": "7a592946-bf21-478e-a135-3e8344c97ff4",
          "type": "short_text",
          "title": "First name",
          "properties": {}
        },
        {
          "id": "eI0bGlmzOGmk",
          "ref": "c5eae38b-f053-47ea-b248-31b0ec7998c7",
          "type": "short_text",
          "title": "Last name",
          "properties": {}
        },
        {
          "id": "Uh6UTKzDhQ4E",
          "ref": "a9de5a49-7f0e-4ade-accd-ffd88c7aaf55",
          "type": "phone_number",
          "title": "Phone number",
          "properties": {}
        },
        {
          "id": "djcKwtbeF8iu",
          "ref": "b43f4696-aaed-48fb-be44-165543dd9384",
          "type": "email",
          "title": "Email",
          "properties": {}
        },
        {
          "id": "9Fms4C4vLX8T",
          "ref": "78965f9a-d70b-4549-a68f-7d957842355b",
          "type": "short_text",
          "title": "Company",
          "properties": {}
        }
      ],
      "endings": [
        {
          "id": "Pg6ODmKDtRA8",
          "ref": "f5fa5381-bc5a-4997-9d9f-506d11faec12",
          "title": "Thank you for filling out the form!",
          "type": "thankyou_screen",
          "properties": {
            "description": "I will reach out to you shortly to book a call.",
            "button_text": "again",
            "show_button": False,
            "share_icons": False,
            "button_mode": "default_redirect"
          }
        }
      ],
      "settings": {
        "partial_responses_to_all_integrations": True
      }
    },
    "answers": [
      {
        "type": "text",
        "text": "Exploring AI",
        "field": {
          "id": "WkY0qjrlB4rV",
          "type": "short_text",
          "ref": "ddd56591-9dfa-4675-bae5-3866c6747493"
        }
      },
      {
        "type": "text",
        "text": "Chairman VaynerX and Vayner Media",
        "field": {
          "id": "Dj2CjNSgeBNW",
          "type": "short_text",
          "ref": "44d1f884-422d-4288-8c60-96d92f433827"
        }
      },
      {
        "type": "url",
        "url": "Do  not have",
        "field": {
          "id": "ykv0e8GKUSEK",
          "type": "website",
          "ref": "7c81696f-7a29-479f-90b2-0a430723a79a"
        }
      },
      {
        "type": "text",
        "text": "Gary",
        "field": {
          "id": "0WkL1GvPhkWG",
          "type": "short_text",
          "ref": "7a592946-bf21-478e-a135-3e8344c97ff4"
        }
      },
      {
        "type": "text",
        "text": "Vaynerchuk",
        "field": {
          "id": "eI0bGlmzOGmk",
          "type": "short_text",
          "ref": "c5eae38b-f053-47ea-b248-31b0ec7998c7"
        }
      },
      {
        "type": "phone_number",
        "phone_number": "+923008224731",
        "field": {
          "id": "Uh6UTKzDhQ4E",
          "type": "phone_number",
          "ref": "a9de5a49-7f0e-4ade-accd-ffd88c7aaf55"
        }
      },
      {
        "type": "email",
        "email": "kma.data.may2018@gmail.com",
        "field": {
          "id": "djcKwtbeF8iu",
          "type": "email",
          "ref": "b43f4696-aaed-48fb-be44-165543dd9384"
        }
      },
      {
        "type": "text",
        "text": "VaynerX and Vayner Media",
        "field": {
          "id": "9Fms4C4vLX8T",
          "type": "short_text",
          "ref": "78965f9a-d70b-4549-a68f-7d957842355b"
        }
      }
    ],
    "ending": {
      "id": "Pg6ODmKDtRA8",
      "ref": "f5fa5381-bc5a-4997-9d9f-506d11faec12"
    }
  }
}

url = "http://localhost:8000/typeform-webhook"

res = requests.post(url, json=mock_data_1)
