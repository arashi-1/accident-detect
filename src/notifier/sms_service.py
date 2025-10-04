import os
from twilio.rest import Client
from dotenv import load_dotenv
from src.db.utils import update_event_status

load_dotenv()

SID = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM = os.getenv("TWILIO_FROM_NUMBER")
ALERT_NUMBERS = [os.getenv("ALERT_PHONE_1"), os.getenv("ALERT_PHONE_2")]

def send_sms_alert(event):
    """
    Sends SMS alerts to all configured numbers.
    Falls back to console print if Twilio creds missing.
    """
    msg = (
        f"🚨 Accident Detected!\n"
        f"Time: {event.timestamp}\n"
        f"Location: ({event.location_lat}, {event.location_lng})\n"
        f"Severity: {event.severity}\n"
        f"Score: {event.score:.2f}\n"
        f"Video Clip: {event.clip_path or 'N/A'}"
    )

    # --- test-mode fallback ---
    if not SID or "your_auth" in (SID or ""):
        print("\n[TEST-MODE SMS] -----------------------")
        print(msg)
        print("--------------------------------------\n")
        update_event_status(event.id, "test-sent")
        return {"status": "test-mode", "msg": msg}

    # --- real Twilio send ---
    client = Client(SID, TOKEN)
    results = []
    for number in filter(None, ALERT_NUMBERS):
        try:
            tw_msg = client.messages.create(body=msg, from_=FROM, to=number)
            results.append({"to": number, "sid": tw_msg.sid})
        except Exception as e:
            print(f"Failed to send SMS to {number}: {e}")
            results.append({"to": number, "error": str(e)})

    if any("sid" in r for r in results):
        update_event_status(event.id, "sent")
    else:
        update_event_status(event.id, "failed")
    return results
