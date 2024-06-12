# import threading
# import queue
# from bluetooth_uart_server.bluetooth_uart_server import ble_gatt_uart_loop
# from LCD import LCD  # Import the LCD class

# def main():
#     rx_q = queue.Queue()
#     tx_q = queue.Queue()
#     device_name = "yahya-pi-gatt-uart"
    
#     # Initialize the LCD
#     lcd = LCD()
    
#     # Start the Bluetooth UART server loop in a separate thread
#     threading.Thread(target=ble_gatt_uart_loop, args=(rx_q, tx_q, device_name), daemon=True).start()
    
#     while True:
#         try:
#             # Wait for up to 1 second for incoming data
#             incoming = rx_q.get(timeout=1)
#             if incoming:
#                 # Print the received data to the console
#                 print("In main loop: {}".format(incoming))
                
#                 # Display the received data on the LCD along with the device name
#                 lcd_message = f"{device_name} = {incoming}"
#                 lcd.display_message(lcd_message)
#         except queue.Empty:
#             # No data received, continue the loop
#             pass

# if __name__ == '__main__':
#     main()

# ----------------------------------------------------------------------------------------
# import threading
# import queue
# import time
# import RPi.GPIO as GPIO
# from bluetooth_uart_server.bluetooth_uart_server import ble_gatt_uart_loop
# from LCD import LCD  # Ensure this is the module handling the LCD

# # Servo motor setup
# GPIO.setmode(GPIO.BCM)  # Set GPIO numbering mode to BCM
# servopin = 18  # Define the GPIO pin connected to the servo
# buttonpin = 16  # Define the GPIO pin connected to the button

# GPIO.setup(servopin, GPIO.OUT)  # Set the servo pin to OUTPUT mode
# GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set the button pin to INPUT mode with a pull-up resistor

# servo_pwm = GPIO.PWM(servopin, 50)  # Create a PWM object for the servo with a frequency of 50Hz
# servo_pwm.start(0)  # Start the PWM signal with a 0% duty cycle

# def reset_system():
#     servo_pwm.ChangeDutyCycle(0)
#     lcd.clear()
#     lcd.display_message("Welcome")  # Show "Welcome" when system is off

# def move_servo_and_reset():
#     # Turn the servo to 90 degrees
#     servo_pwm.ChangeDutyCycle(7.5)
#     time.sleep(5)  # Keep the servo turned and the message displayed for 5 seconds
#     # Return the servo to the initial position
#     servo_pwm.ChangeDutyCycle(2)
#     time.sleep(1)  # Wait for the servo to move back
#     reset_system()

# def clear_queue(q):
#     try:
#         while True:
#             q.get_nowait()
#     except queue.Empty:
#         pass

# def handle_incoming_message(work_active, detection_event):
#     while True:
#         if not work_active.is_set():
#             time.sleep(0.1)
#             continue
#         try:
#             incoming = rx_q.get(timeout=1)
#             if incoming:
#                 incoming = incoming.strip()
#                 print("Received in main loop: {}".format(incoming))
#                 if incoming == "accepted":
#                     clear_queue(rx_q)  # Clear the queue to discard saved states
#                     work_active.clear()  # Stop further work until button is pressed
#                     detection_event.set()  # Signal that an accepted state was detected
#                 elif incoming == "rejected":
#                     pass
#         except queue.Empty:
#             pass
# def button_callback(channel):
#     global work_active, detection_event, rx_q  # Ensure these are global so they can be accessed and modified
#     if not work_active.is_set():
#         print("Button pressed, starting detection.")
#         lcd.clear()
#         lcd.display_message("Processing") 
#         # Show "Processing" when the button is pressed
#         clear_queue(rx_q)  # Clear the queue before restarting
#         work_active.set()  # Allow work to start again
#         detection_event.clear()  # Clear the detection event

# def main():
#     global lcd, work_active, detection_event, rx_q
#     rx_q = queue.Queue()
#     tx_q = queue.Queue()
#     device_name = "yahya-pi-gatt-uart"
#     lcd = LCD()  # Initialize the LCD
#     work_active = threading.Event()
#     detection_event = threading.Event()

#     # Display the welcome message
#     lcd.display_message("Welcome")

#     # Set up button interrupt
#     GPIO.add_event_detect(buttonpin, GPIO.FALLING, callback=button_callback, bouncetime=300)

#     # Start the BLE thread
#     threading.Thread(target=ble_gatt_uart_loop, args=(rx_q, tx_q, device_name), daemon=True).start()

#     # Start the incoming message handler thread
#     threading.Thread(target=handle_incoming_message, args=(work_active, detection_event), daemon=True).start()

#     while True:
#         try:
#             # Wait for work to be active
#             work_active.wait()
#             # Wait for either 5 seconds or until an accepted state is detected
#             if not detection_event.wait(timeout=5):
#                 # No accepted state detected within 5 seconds
#                 lcd.send_string("Try again!")
#                 time.sleep(3)  # Show the "Try Again" message for 3 seconds
#                 reset_system()  # Reset the system and show "Welcome"
#                 work_active.clear()  # Stop further work until button is pressed
#                 detection_event.clear()
#             else:
#                 # An accepted state was detected, system will have already been reset
#                 lcd.clear()
#                 lcd.send_string("ACCEPTED!")
#                 move_servo_and_reset()
#                 continue

#             # Optional: Send some data every 5 iterations
#             tx_q.put("ping")
#             time.sleep(0.1)
#         except KeyboardInterrupt:
#             break

#     servo_pwm.stop()  # Stop the PWM signal
#     GPIO.cleanup()  # Clean up the GPIO pins

# if __name__ == '__main__':
#     main()


# ------------------------ With NEOPIXEL ---------------------- 

import threading
import queue
import time
import RPi.GPIO as GPIO
from bluetooth_uart_server.bluetooth_uart_server import ble_gatt_uart_loop
from LCD import LCD  # Ensure this is the module handling the LCD
from lib import neopixel_spidev as neopixel

# Servo motor setup
GPIO.setmode(GPIO.BCM)  # Set GPIO numbering mode to BCM
servopin = 18  # Define the GPIO pin connected to the servo
buttonpin = 16  # Define the GPIO pin connected to the button

GPIO.setup(servopin, GPIO.OUT)  # Set the servo pin to OUTPUT mode
GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set the button pin to INPUT mode with a pull-up resistor

servo_pwm = GPIO.PWM(servopin, 50)  # Create a PWM object for the servo with a frequency of 50Hz
servo_pwm.start(0)  # Start the PWM signal with a 0% duty cycle

# Initialize NeoPixels
pixels = neopixel.NeoPixelSpiDev(0, 0, n=8, pixel_order=neopixel.GRB)
pixels.fill(255 << 16 | 255 << 8 | 255)  # Set all pixels to white
pixels.show()

def reset_system():
    servo_pwm.ChangeDutyCycle(0)
    lcd.clear()
    lcd.display_message("Welcome")  # Show "Welcome" when system is off

def move_servo_and_reset():
    # Turn the servo to 90 degrees
    servo_pwm.ChangeDutyCycle(7.5)
    time.sleep(5)  # Keep the servo turned and the message displayed for 5 seconds
    # Return the servo to the initial position
    servo_pwm.ChangeDutyCycle(2)
    time.sleep(1)  # Wait for the servo to move back
    reset_system()

def clear_queue(q):
    try:
        while True:
            q.get_nowait()
    except queue.Empty:
        pass

def handle_incoming_message(work_active, detection_event):
    while True:
        if not work_active.is_set():
            time.sleep(0.1)
            continue
        try:
            incoming = rx_q.get(timeout=1)
            if incoming:
                incoming = incoming.strip()
                print("Received in main loop: {}".format(incoming))
                if incoming == "accepted":
                    clear_queue(rx_q)  # Clear the queue to discard saved states
                    work_active.clear()  # Stop further work until button is pressed
                    detection_event.set()  # Signal that an accepted state was detected
                elif incoming == "rejected":
                    pass
        except queue.Empty:
            pass

def button_callback(channel):
    global work_active, detection_event, rx_q  # Ensure these are global so they can be accessed and modified
    if not work_active.is_set():
        print("Button pressed, starting detection.")
        lcd.clear()
        lcd.display_message("Processing") 
        # Show "Processing" when the button is pressed
        clear_queue(rx_q)  # Clear the queue before restarting
        work_active.set()  # Allow work to start again
        detection_event.clear()  # Clear the detection event

def main():
    global lcd, work_active, detection_event, rx_q
    rx_q = queue.Queue()
    tx_q = queue.Queue()
    device_name = "yahya-pi-gatt-uart"
    lcd = LCD()  # Initialize the LCD
    work_active = threading.Event()
    detection_event = threading.Event()

    # Display the welcome message
    lcd.display_message("Welcome")

    # Set up button interrupt
    GPIO.add_event_detect(buttonpin, GPIO.FALLING, callback=button_callback, bouncetime=300)

    # Start the BLE thread
    threading.Thread(target=ble_gatt_uart_loop, args=(rx_q, tx_q, device_name), daemon=True).start()

    # Start the incoming message handler thread
    threading.Thread(target=handle_incoming_message, args=(work_active, detection_event), daemon=True).start()

    while True:
        try:
            # Wait for work to be active
            work_active.wait()
            # Wait for either 5 seconds or until an accepted state is detected
            if not detection_event.wait(timeout=5):
                # No accepted state detected within 5 seconds
                lcd.send_string("Try again!")
                time.sleep(3)  # Show the "Try Again" message for 3 seconds
                reset_system()  # Reset the system and show "Welcome"
                work_active.clear()  # Stop further work until button is pressed
                detection_event.clear()
            else:
                # An accepted state was detected, system will have already been reset
                lcd.clear()
                lcd.send_string("ACCEPTED!")
                move_servo_and_reset()
                continue

            # Optional: Send some data every 5 iterations
            tx_q.put("ping")
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    # Cleanup
    servo_pwm.stop()  # Stop the PWM signal
    GPIO.cleanup()  # Clean up the GPIO pins
    pixels.fill(0)  # Turn off NeoPixels
    pixels.show()

if __name__ == '__main__':
    main()
