import time
import cv2
import numpy as np

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0: return 0.0
    boxAArea = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea)

class Analyzer:
    def __init__(self, threshold=0.6, cooldown=300):
        self.threshold = threshold
        self.cooldown = cooldown
        self.last_alert = 0
        self.prev_gray = None   # for optical flow

    def compute_score(self, detections_prev, detections_cur, frame=None):
        score_parts = []

        # 1) IoU overlap check
        for d1 in detections_prev:
            for d2 in detections_cur:
                if d1['class'] in ('car','truck','bus') and d2['class'] in ('car','truck','bus'):
                    overlap = iou(d1['box'], d2['box'])
                    if overlap > 0.2:   # threshold
                        score_parts.append(min(1.0, overlap*2))  # boost overlap

        # 2) Sudden bounding box scale change
        for d1, d2 in zip(detections_prev, detections_cur):
            area1 = (d1['box'][2]-d1['box'][0]) * (d1['box'][3]-d1['box'][1])
            area2 = (d2['box'][2]-d2['box'][0]) * (d2['box'][3]-d2['box'][1])
            if area1 > 0 and area2 > 0:
                scale_change = abs(area2-area1)/area1
                if scale_change > 0.5:  # >50% change
                    score_parts.append(min(1.0, scale_change))

        # 3) Optical flow chaos (motion)
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.prev_gray is not None:
                flow = cv2.calcOpticalFlowFarneback(
                    self.prev_gray, gray,
                    None, 0.5, 3, 15, 3, 5, 1.2, 0
                )
                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                mean_mag = np.mean(mag)
                if mean_mag > 5.0:  # motion spike
                    score_parts.append(min(1.0, mean_mag/10))
            self.prev_gray = gray

        # Combine scores
        if not score_parts:
            return 0.0
        return np.clip(sum(score_parts)/len(score_parts), 0, 1)

    def should_alert(self, score):
        now = time.time()
        if score >= self.threshold and (now - self.last_alert) > self.cooldown:
            self.last_alert = now
            return True
        return False
