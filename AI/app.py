# from IPython.display import Video
import sys
import asyncio

from queue import Queue
import threading
import time
from BLE_client import run
import cv2  # Importing the OpenCV library for computer vision tasks.
import supervision as sv  # Importing a module named supervision as sv.
# Importing YOLO object detection model from ultralytics library.
from ultralytics import YOLO
import gradio as gr  # Importing Gradio library for creating web interfaces.

# print("start")

# model = YOLO("AI/runs/detect/train5/weights/best.pt")
# bounding_box_annotator = sv.BoundingBoxAnnotator()
# label_annotator = sv.LabelAnnotator()

# # Creating two Queues for communication between threads.
# tx_q = Queue()
# rx_q = Queue()

# targetDeviceName=None
# targetDeviceMac="D8:3A:DD:DE:0B:D9"

# def init_ble_thread():
#     # Creating a new thread for running a function 'run' with specified arguments.
#     ble_client_thread = threading.Thread(target=run, args=(
#         rx_q, tx_q, targetDeviceName, targetDeviceMac), daemon=True)
#     # Starting the thread execution.
#     ble_client_thread.start()


# # Defining a function named show_preds_video, which takes a video file path as input.
# def show_preds_video(video_path, conf_threshold):
#     # Opening the video file specified by the video_path.
#     cap = cv2.VideoCapture(video_path)  # Change to 0 for webcam...
#     # Extracting video properties: width, height, and frames per second (fps).
#     w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH,
#                  cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
#     # Creating a VideoWriter object for writing the processed frames to an output video file.
#     out = cv2.VideoWriter('output_video.mp4',
#                           cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))






#     # Looping through each frame of the video until it is opened.
#     while (cap.isOpened()):
#         # Reading the next frame from the video.
#         ret, img = cap.read()
#         # If frame is successfully read.
#         if not ret:
#             break

#         # Making predictions on the frame using the model.
#         # 'model' object should be defined somewhere.
#         result = model.predict(img)
#         result = result[0] if isinstance(result, list) else result
#         # Converting predictions to a format compatible with supervision module.
#         detections = sv.Detections.from_ultralytics(result)
#         # Filtering out detections based on confidence threshold.
#         detections = detections[detections.confidence > conf_threshold]

#         # Counting the number of drones detected.
#         ndrones = len(detections[detections.class_id == 0])

#         # Extracting labels for detected objects.
#         labels = [
#             model.model.names[class_id]
#             for class_id
#             in detections.class_id
#         ]

#         # Annotating bounding boxes on the frame.
#         annotated_frame = bounding_box_annotator.annotate(
#             scene=img.copy(), detections=detections)
#         # Annotating labels on the frame.
#         annotated_frame = label_annotator.annotate(
#             scene=annotated_frame, detections=detections, labels=labels)

#         # Writing the annotated frame to the output video.
#         out.write(annotated_frame)
#         # Displaying the annotated frame.

#         # Sending data to the Bluetooth device.
#         tx_q.put(str(ndrones))
#         print("ndrones: ", ndrones)

#         yield annotated_frame, ndrones

#     # Releasing the output video writer.
#     out.release()

#     interface_video.close()
    
# ------------------------------------------------------------------------------------------------

# # Defining inputs and outputs for the Gradio interface.
# inputs_video = [
#     gr.components.Video(label="Input video"),
#     gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold")
# ]
# outputs_video = [
#     gr.components.Image(type="numpy", label="Analysed video"),
#     gr.Textbox(label="Amount of drones"),
# ]
# # Creating a Gradio interface with specified inputs, outputs, and other settings.
# interface_video = gr.Interface(
#     fn=show_preds_video,
#     inputs=inputs_video,
#     outputs=outputs_video,
#     title="Bee detector",
#     cache_examples=False,
# )


# # Launching the Gradio interface.
# if __name__ == '__main__':
#     print("launching BLE thread")
#     init_ble_thread()
#     time.sleep(1) # little breathing room for BLE to start
#     print("launching GradIO interface")
#     interface_video.launch()
    

# import sys
# import asyncio
# from queue import Queue
# import threading
# import time
# import cv2
# import torch
# from ultralytics import YOLO
# from BLE_client import run  # Import the BLE client run function

# print("start")

# # Load the YOLO model
# model = YOLO("C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\runs\\detect\\yolov8_bottle_cap\\weights\\best.pt")

# # Create queues for communication between threads
# tx_q = Queue()
# rx_q = Queue()

# targetDeviceName = None
# targetDeviceMac = "D8:3A:DD:DE:0B:D9"  # Update this with your Raspberry Pi's MAC address

# # Initialize and start the BLE client thread
# def init_ble_thread():
#     ble_client_thread = threading.Thread(target=run, args=(rx_q, tx_q, targetDeviceName, targetDeviceMac), daemon=True)
#     ble_client_thread.start()

# def process_frame(frame):
#     results = model(frame)
#     for result in results:
#         boxes = result.boxes
#         if boxes is not None:
#             bottle_detected = False
#             cap_detected = False
#             for box in boxes:
#                 cls = int(box.cls.item())
#                 conf = box.conf.item()
#                 xyxy = box.xyxy if isinstance(box.xyxy, torch.Tensor) else torch.tensor(box.xyxy)
#                 xyxy = xyxy.view(-1).numpy().astype(int)

#                 # Draw the bounding box
#                 color = (0, 255, 0)  # Green for accepted
#                 if result.names[cls] == 'bottle' and conf > 0.3:
#                     bottle_detected = True
#                 if result.names[cls] == 'cap' and conf > 0.3:
#                     cap_detected = True

#                 if not (bottle_detected and cap_detected):
#                     color = (0, 0, 255)  # Red for rejected

#                 cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
#                 label = f"{result.names[cls]}: {conf:.2f}"
#                 cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#             if bottle_detected and cap_detected:
#                 tx_q.put("accepted")
#                 print("Accepted: Bottle and Cap detected")
#             else:
#                 tx_q.put("rejected")
#                 print("Rejected: Bottle or Cap not detected")

# def main():
#     # Initialize the BLE thread
#     print("Launching BLE thread")
#     init_ble_thread()
#     time.sleep(1)  # Give some time for BLE to start

#     # Initialize the webcam
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         exit()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Could not read frame.")
#             break

#         process_frame(frame)

#         # Display the frame with OpenCV
#         cv2.imshow("Camera Feed", frame)

#         # Exit loop when 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()

# ------------------------------------------------------------------------------------------

import sys
import asyncio
from queue import Queue
import threading
import time
import cv2
import torch
from ultralytics import YOLO
from BLE_client import run  # Import the BLE client run function

print("start")

# Load the YOLO model
model = YOLO("C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\runs\\detect\\yolov8_bottle_cap\\weights\\best.pt")

# Create queues for communication between threads
tx_q = Queue()
rx_q = Queue()

targetDeviceName = None
targetDeviceMac = "D8:3A:DD:DE:0B:D9"  # Update this with your Raspberry Pi's MAC address

# Initialize and start the BLE client thread
def init_ble_thread():
    ble_client_thread = threading.Thread(target=run, args=(rx_q, tx_q, targetDeviceName, targetDeviceMac), daemon=True)
    ble_client_thread.start()

def process_frame(frame):
    results = model(frame)
    bottle_detected = False
    cap_detected = False
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls.item())
                conf = box.conf.item()
                xyxy = box.xyxy if isinstance(box.xyxy, torch.Tensor) else torch.tensor(box.xyxy)
                xyxy = xyxy.view(-1).numpy().astype(int)

                # Draw the bounding box
                color = (0, 255, 0)  # Green for accepted
                if result.names[cls] == 'bottle' and conf > 0.3:
                    bottle_detected = True
                if result.names[cls] == 'cap' and conf > 0.3:
                    cap_detected = True

                if not (bottle_detected and cap_detected):
                    color = (0, 0, 255)  # Red for rejected

                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
                label = f"{result.names[cls]}: {conf:.2f}"
                cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if bottle_detected and cap_detected:
        tx_q.put("accepted")
        print("Accepted: Bottle and Cap detected")
    else:
        tx_q.put("rejected")
        print("Rejected: Bottle or Cap not detected")

def main():
    # Initialize the BLE thread
    print("Launching BLE thread")
    init_ble_thread()
    time.sleep(1)  # Give some time for BLE to start

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        # Capture a frame every 5 seconds
        time.sleep(2)
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        process_frame(frame)

        # Display the frame with OpenCV
        cv2.imshow("Captured Image", frame)
        
        # Check if 'q' key is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
