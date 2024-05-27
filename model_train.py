from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Load a pretrained model

# Train the model
model.train(data='C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\labelled_dataset(2)\\data.yaml', epochs=10, imgsz=640, batch=16 , name='yolov8_bottle_cap')

# Validate the model
model.val()