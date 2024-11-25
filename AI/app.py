# ---------------- live video stream ---------------
import sys
import asyncio
from queue import Queue
import threading
import time
import cv2
import torch
from ultralytics import YOLO
from BLE_client import run  # Import the BLE client run function
from bleak import BleakScanner
import supervision as sv  # Importing a module named supervision as sv.
# Importing YOLO object detection model from ultralytics library.
from ultralytics import YOLO
import gradio as gr  # Importing Gradio library for creating web interfaces.

print("start")

# Load the YOLO model
model = YOLO("C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\runs\\detect\\yolov8_last-bot-cap-model\\weights\\best.pt")
tx_q = Queue()
rx_q = Queue()
BLE_DEVICE_MAC = "D8:3A:DD:DE:0B:D9"
connection_event = threading.Event()

def init_ble_thread():
    global ble_client_thread
    try:
        # Creating a new thread for running a function 'run' with specified arguments.
        ble_client_thread = threading.Thread(target=run, args=(
            rx_q, tx_q, None, BLE_DEVICE_MAC, connection_event), daemon=True)
        # Starting the thread execution.
        ble_client_thread.start()
    except Exception as e:
        print(f"Error starting BLE client thread: {e}")

# Initialize the thread variable
ble_client_thread = None

# Repeat the thread initialization until the connection_event is set
while not connection_event.is_set():
    if ble_client_thread is None or not ble_client_thread.is_alive():
        init_ble_thread()
    connection_event.wait(timeout=5)  # Optional timeout to avoid tight looping

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

                # Check if confidence is below 0.4, skip drawing the bounding box
                if conf < 0.4:
                    continue

                # Determine color based on detection confidence
                if conf >= 0.4:
                    color = (0, 255, 0)  # Green for accepted
                else:
                    color = (0, 0, 255)  # Red for rejected

                # Check if bottle and cap are detected with sufficient confidence
                if result.names[cls] == 'bottle' and conf >= 0.4:
                    bottle_detected = True
                if result.names[cls] == 'cap' and conf >= 0.4:
                    cap_detected = True

                # Draw the bounding box and label
                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
                label = f"{result.names[cls]}: {conf:.2f}"
                cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2)

    # Send the result via BLE
    if bottle_detected and cap_detected:
        tx_q.put("accepted")
        print("Accepted: Bottle and Cap detected")
    else:
        tx_q.put("rejected")
        print("Rejected: Bottle or Cap not detected")

def main():
    # Check for the BLE device before starting camera processing
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # device = loop.run_until_complete(find_device(targetDeviceMac))

    # Initialize the BLE thread once the device is found
    print("Launching BLE thread")
    init_ble_thread()
    time.sleep(1)  # Give some time for BLE to start

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        process_frame(frame)

        # Display the frame with OpenCV
        cv2.imshow("Camera Feed", frame)

        # Exit loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



# --------------- 1fps picture capture ------------

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
# model = YOLO("C:\\Users\\yahya\\Documents\\project_one\\2023-2024-projectone-ctai-yahyasultanch\\runs\\detect\\yolov8_new_bottle\\weights\\best.pt")

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
#     bottle_detected = False
#     cap_detected = False
#     for result in results:
#         boxes = result.boxes
#         if boxes is not None:
#             for box in boxes:
#                 cls = int(box.cls.item())
#                 conf = box.conf.item()
#                 xyxy = box.xyxy if isinstance(box.xyxy, torch.Tensor) else torch.tensor(box.xyxy)
#                 xyxy = xyxy.view(-1).numpy().astype(int)

#                 # Draw the bounding box
#                 color = (0, 255, 0)  # Green for accepted
#                 if result.names[cls] == 'bottle' and conf > 0.4:
#                     bottle_detected = True
#                 if result.names[cls] == 'cap' and conf > 0.4:
#                     cap_detected = True

#                 if not (bottle_detected and cap_detected):
#                     color = (0, 0, 255)  # Red for rejected

#                 cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
#                 label = f"{result.names[cls]}: {conf:.2f}"
#                 cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2)

#     if bottle_detected and cap_detected:
#         tx_q.put("accepted")
#         print("Accepted: Bottle and Cap detected")
#     else:
#         tx_q.put("rejected")
#         print("Rejected: Bottle or Cap not detected")

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
#         # Capture a frame every 5 seconds
#         time.sleep(2)
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Could not read frame.")
#             break

#         process_frame(frame)

#         # Display the frame with OpenCV
#         cv2.imshow("Captured Image", frame)
        
#         # Check if 'q' key is pressed to exit the loop
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()
