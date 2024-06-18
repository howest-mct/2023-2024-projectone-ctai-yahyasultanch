import time
import RPi.GPIO as GPIO

# Servo motor setup
GPIO.setmode(GPIO.BCM)  # Set GPIO numbering mode to BCM
servopin = 18  # Define the GPIO pin connected to the servo

GPIO.setup(servopin, GPIO.OUT)  # Set the servo pin to OUTPUT mode

servo_pwm = GPIO.PWM(servopin, 50)  # Create a PWM object for the servo with a frequency of 50Hz
servo_pwm.start(0)  # Start the PWM signal with a 0% duty cycle

def reset_system():
    servo_pwm.ChangeDutyCycle(0)

def move_servo_and_reset():
    # Turn the servo to 90 degrees
    servo_pwm.ChangeDutyCycle(13)
    time.sleep(5)  # Keep the servo turned for 5 seconds
    # Return the servo to the initial position
    servo_pwm.ChangeDutyCycle(8)
    time.sleep(1)  # Wait for the servo to move back
    reset_system()

# Example usage
try:
    while True:
        move_servo_and_reset()
        time.sleep(5)  # Wait 10 seconds before moving the servo again
except KeyboardInterrupt:
    pass
finally:
    servo_pwm.stop()  # Stop the PWM signal
    GPIO.cleanup()  # Clean up the GPIO pins
