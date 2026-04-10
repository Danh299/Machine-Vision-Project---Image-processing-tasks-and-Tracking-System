from ultralytics import YOLO
import cv2

# Detect objects in images using YOLO model
def Detect_Obj(imgin, yolo_model_path):
    model = YOLO(yolo_model_path)
    imgout = imgin.copy()
    names = model.names

    results = model.predict(imgin, conf=0.6, verbose=False)
    boxes = results[0].boxes.xyxy.cpu()
    clss = results[0].boxes.cls.cpu().tolist()
    confs = results[0].boxes.conf.tolist()
    
    for box, cls, conf in zip(boxes, clss, confs):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(imgout, (x1, y1), (x2, y2), (255, 255, 0), 2)
        label = f"{names[int(cls)]} {conf:.2f}"
        cv2.putText(imgout, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return imgout
