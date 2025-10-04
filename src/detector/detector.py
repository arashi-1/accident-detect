# Minimal wrapper using ultralytics YOLO if installed, else fallback to no-op
try:
    from ultralytics import YOLO
    model = YOLO('yolov8n.pt')  # small model; download automatically
except Exception:
    model = None

def detect(frame):
    """Return list of detections: [{'class': 'car', 'conf': 0.8, 'box': [x1, y1, x2, y2]}, ...]"""
    if model:
        results = model(frame)[0]
        out = []
        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            out.append({'class': model.names[int(cls)], 'conf': float(conf), 'box': [int(v) for v in box]})
        return out
    # fallback: return empty
    return []

