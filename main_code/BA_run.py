import RPi.GPIO as GPIO
import time

# Constants for the stepper motors
DEGREES_PER_STEP = 1.7
STEPS_PER_REVOLUTION = 200
STEPS_PER_DEGREE = STEPS_PER_REVOLUTION / (360 / DEGREES_PER_STEP)  # Calculate steps per degree

# Function to move a motor a certain number of steps in a given direction
def move_motor(motor_pins, direction, degrees):
    """
    Move a motor a certain number of degrees in a given direction.

    Parameters:
    motor_pins (dict): Dictionary with 'step' and 'dir' pins of the motor.
    direction (str): Direction to rotate the motor ('cw' for clockwise, 'ccw' for counterclockwise).
    degrees (int): Number of degrees to move the motor.
    """
    steps = int(degrees * STEPS_PER_DEGREE)
    GPIO.output(motor_pins['dir'], GPIO.HIGH if direction == 'cw' else GPIO.LOW)

    for _ in range(steps):
        GPIO.output(motor_pins['step'], GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(motor_pins['step'], GPIO.LOW)
        time.sleep(0.001)

# GPIO pin assignments for the motors
detector_motor_pins = {'step': 17, 'dir': 18}
sample_motor_pins = {'step': 23, 'dir': 24}

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
for motor_pins in [detector_motor_pins, sample_motor_pins]:
    for pin in motor_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

try:
    # Get initial angles from the user
    detector_angle = float(input("Enter initial detector angle: "))
    sample_angle = float(input("Enter initial sample plate angle: "))

    while True:
        print(f"Current angles - Detector: {detector_angle}, Sample: {sample_angle}")

        move_choice = float(input("Enter number of degrees to move: "))
        direction_choice = int(input("0 for smaller angle, 1 for wider angle: "))

        if direction_choice == 0:
            move_motor(detector_motor_pins, 'cw', move_choice)
            move_motor(sample_motor_pins, 'ccw', move_choice)
            detector_angle += move_choice
            sample_angle -= move_choice
        elif direction_choice == 1:
            move_motor(detector_motor_pins, 'ccw', move_choice)
            move_motor(sample_motor_pins, 'cw', move_choice)
            detector_angle -= move_choice
            sample_angle += move_choice

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    GPIO.cleanup()
