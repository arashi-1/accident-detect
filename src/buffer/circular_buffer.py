import collections, time, cv2, subprocess, os

class CircularBuffer:
    def __init__(self, max_frames):
        self.buf = collections.deque(maxlen=max_frames)
    def push(self, frame, ts):
        self.buf.append((ts, frame.copy()))
    def extract_clip(self, out_path, fps=20):
        # write frames from buffer to file via OpenCV VideoWriter
        if not self.buf: return None
        h, w = self.buf[0][1].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vw = cv2.VideoWriter(out_path, fourcc, fps, (w,h))
        for ts, frame in self.buf:
            vw.write(frame)
        vw.release()
        return out_path
