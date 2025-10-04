import cv2

def open_video(path=0):
    cap = cv2.VideoCapture(path)
    assert cap.isOpened()
    return cap

def read_frame(cap):
    ret, frame = cap.read()
    return (ret, frame)