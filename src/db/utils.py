from .database import SessionLocal
from .models import AccidentEvent

def log_event(score, severity="medium", location=None, clip_path=None):
    db = SessionLocal()
    try:
        lat, lng = (None, None)
        if location:
            lat, lng = location
        event = AccidentEvent(
            score=score,
            severity=severity,
            location_lat=lat,
            location_lng=lng,
            clip_path=clip_path,
            alert_status="pending"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    finally:
        db.close()

def update_event_status(event_id, status):
    db = SessionLocal()
    try:
        event = db.query(AccidentEvent).filter(AccidentEvent.id == event_id).first()
        if event:
            event.alert_status = status
            db.commit()
    finally:
        db.close()
