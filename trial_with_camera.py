import cv2
from ultralytics import YOLO
import torch

# Load the YOLOv8 model
model = YOLO('runs/detect/yolov8_new_bottle/weights/best.pt')

# Initialize the webcamq
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Define a function to process each frame
def process_frame(frame):
    results = model(frame)

    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls.item())
                conf = box.conf.item()
                xyxy = box.xyxy if isinstance(box.xyxy, torch.Tensor) else torch.tensor(box.xyxy)
                xyxy = xyxy.view(-1).numpy().astype(int)  # Flatten the array and ensure it's a numpy array of integers

                # Debugging print statements
                print(f"Class: {result.names[cls]}, Confidence: {conf:.2f}, BBox: {xyxy}")

                # Draw the bounding box on the frame
                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                label = f"{result.names[cls]}: {conf:.2f}"
                cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    processed_frame = process_frame(frame)

    cv2.imshow('YOLOv8 Object Detection', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
