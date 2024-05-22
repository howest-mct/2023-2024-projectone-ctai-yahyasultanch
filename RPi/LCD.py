from smbus import SMBus
import time


class LCD:
    I2C_ADDR = 0x27  # I2C device address
    LCD_WIDTH = 16    # Maximum characters per line
    LCD_CHR = 1       # Character mode
    LCD_CMD = 0       # Command mode
    LCD_LINE_1 = 0x80 # Instruction to go to beginning of line 1
    LCD_LINE_2 = 0xC0 # Instruction to go to beginning of line 2
    LCD_BACKLIGHT = 0x08  # Data bit value to turn backlight on
    ENABLE = 0b00000100    # Enable bit value
    E_PULSE = 0.0005       # Pulse delay
    E_DELAY = 0.0005       # Delay between pulses

    def __init__(self):
        self.bus = SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        self.send_byte(0x33, self.LCD_CMD)
        self.send_byte(0x32, self.LCD_CMD)
        self.send_byte(0x06, self.LCD_CMD)
        self.send_byte(0x0C, self.LCD_CMD)
        self.send_byte(0x28, self.LCD_CMD)
        self.send_byte(0x01, self.LCD_CMD)
        time.sleep(0.05)

    def send_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def send_instruction(self, instruction):
        self.send_byte(instruction, self.LCD_CMD)

    def send_character(self, char):
        self.send_byte(ord(char), self.LCD_CHR)

    def send_string(self, message, line=LCD_LINE_1):
        self.send_instruction(line)
        for char in message:
            self.send_character(char)

    def clear(self):
        self.send_instruction(0x01)  

    def display_on(self):
        self.send_instruction(0x0C)  

    def display_off(self):
        self.send_instruction(0x08) 

    def cursor_on(self):
        self.send_instruction(0x0E) 

    def cursor_off(self):
        self.send_instruction(0x0C) 

    def display_ip_addresses(self):
        self.clear()
        wlan_ip = self.get_ipv4_addresses('wlan0')
        eth_ip = self.get_ipv4_addresses('eth0')

        self.send_string(wlan_ip, LCD.LCD_LINE_1)
        self.send_string(eth_ip, LCD.LCD_LINE_2)

    def display_led_bar_graph_x(self, analog_value):
        num_leds_lit = int((analog_value / 255.0) * 16)  # because LCD_width is 16
        bar_graph = "|" * num_leds_lit + " " * (16 - num_leds_lit)
        self.send_string(bar_graph, LCD.LCD_LINE_1)

    def display_led_bar_graph_y(self, analog_value):
        num_leds_lit = int((analog_value / 255.0) * 16) 
        bar_graph = "#" * num_leds_lit + " " * (16 - num_leds_lit)
        self.send_string(bar_graph, LCD.LCD_LINE_1)

    def display_initial_message(self):
        self.clear()
        self.send_string("Send a message", LCD.LCD_LINE_1)
        self.send_string("via BLE UART", LCD.LCD_LINE_2)

    # def display_message(self, message):
    #     self.clear()
    #     if len(message) <= self.LCD_WIDTH:
    #         self.send_string(message)
    #     else:
    #         message += " " * (self.LCD_WIDTH - 1) 
    #         for i in range(len(message) - self.LCD_WIDTH + 1):
    #             self.send_string(message[i:i + self.LCD_WIDTH])
    #             time.sleep(0.5)

    def display_message(self, message):
        self.clear()
        if len(message) <= self.LCD_WIDTH:
            self.send_string(message)
        else:
            # Show first 16 characters on the first line
            self.send_string(message[:self.LCD_WIDTH], LCD.LCD_LINE_1)
            # Show next 16 characters on the second line
            self.send_string(message[self.LCD_WIDTH:self.LCD_WIDTH*2], LCD.LCD_LINE_2)
            time.sleep(1)  # Wait for 1 second before starting the scrolling
            # Scroll the message if it's longer than 32 characters
            for i in range(len(message) - self.LCD_WIDTH*2 + 1):
                self.send_string(message[i+self.LCD_WIDTH*2:i+self.LCD_WIDTH*3], LCD.LCD_LINE_1)
                self.send_string(message[i+self.LCD_WIDTH*3:i+self.LCD_WIDTH*4], LCD.LCD_LINE_2)
                time.sleep(0.5)


