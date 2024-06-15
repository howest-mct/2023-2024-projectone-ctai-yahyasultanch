from ultralytics import YOLO
import os

# Load the trained YOLOv8 model
model = YOLO('C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\runs\\detect\\yolov8_last-bot-cap-model\\weights\\best.pt')  # Path to your trained model

# Path to the test images
test_images_path = 'C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\lat-lab-dataset\\test\\images'

# Get all test images
test_images = [os.path.join(test_images_path, img) for img in os.listdir(test_images_path) if img.endswith(('.png', '.jpg', '.jpeg'))]

# Run inference on the test set
results = model.predict(test_images, save=True, save_txt=True, save_conf=True, save_crop=False)

# Print results
for result in results:
    print(f"Image: {result.path}")
    print(f"Predictions: {result.boxes}")

# Results will be saved in the 'runs' directory
