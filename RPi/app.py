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

import threading
import queue
import time
from bluetooth_uart_server.bluetooth_uart_server import ble_gatt_uart_loop
from LCD import LCD  # Ensure this is the module handling the LCD

def main():
    rx_q = queue.Queue()
    tx_q = queue.Queue()
    device_name = "yahya-pi-gatt-uart"
    lcd = LCD()  # Initialize the LCD

    def handle_incoming_message():
        while True:
            try:
                incoming = rx_q.get(timeout=1)
                if incoming:
                    print("Received in main loop: {}".format(incoming))
                    if incoming.strip() == "accepted":
                        lcd.display_message("Accepted")
                    elif incoming.strip() == "rejected":
                        lcd.display_message("Rejected: Remove bottle")
            except Exception as e:
                pass

    threading.Thread(target=ble_gatt_uart_loop, args=(rx_q, tx_q, device_name), daemon=True).start()
    threading.Thread(target=handle_incoming_message, daemon=True).start()

    while True:
        try:
            # Optional: Send some data every 5 iterations
            tx_q.put("ping")
            time.sleep(5)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
