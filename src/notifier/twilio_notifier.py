from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
SID = os.getenv('TWILIO_ACCOUNT_SID')
TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
FROM = os.getenv('TWILIO_FROM_NUMBER')
TO = os.getenv('TEST_PHONE')

def send_sms(body):
    if not SID or 'your_sid' in SID:
        print("Twilio not configured. SMS content:", body)
        return {'status':'test-mode','body':body}
    client = Client(SID, TOKEN)
    msg = client.messages.create(body=body, from_=FROM, to=TO)
    return {'status':'sent','sid': msg.sid}
