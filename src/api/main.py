from fastapi import FastAPI
import threading, time, cv2
from src.utils.video_utils import open_video, read_frame
from src.detector.detector import detect
from src.buffer.circular_buffer import CircularBuffer
from src.analyzer.analyzer import Analyzer
from src.db.utils import log_event
from src.notifier.sms_service import send_sms_alert

app = FastAPI()

# background thread will run capture & detection
def capture_loop(video_source='data/raw_videos/sample.mp4'):  # if video_source = 0 => webcam
    cap = open_video(video_source)
    fps = cap.get(cv2.CAP_PROP_FPS) or 20
    buffer = CircularBuffer(max_frames=int(30 * fps))
    analyzer = Analyzer()
    ret = True
    prev_dets = []

    while ret:
        ret, frame = read_frame(cap)
        if not ret:
            break
        ts = time.time()
        buffer.push(frame, ts)
        dets = detect(frame)
        score = analyzer.compute_score(prev_dets, dets, frame)
        print("Score:", score)

        if analyzer.should_alert(score):
            print("⚠️ Accident detected! Score:", score)
            clip = buffer.extract_clip('data/clip_last.mp4', fps=int(fps))
            event = log_event(score=score, severity="high",
                              location=(26.85, 80.95), clip_path=clip)
            send_sms_alert(event)  # This handles SMS + status update

        prev_dets = dets

    cap.release()

threading.Thread(target=capture_loop, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok"}
