from ultralytics import YOLO
import cv2

def predict(image):
    bht = YOLO('weight/detector.pt')
    results = bht.predict(image, imgsz=480, conf=0.45)

    return results[0]

