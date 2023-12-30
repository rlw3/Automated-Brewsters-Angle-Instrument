import RPi.GPIO as GPIO
import time

# GPIO pin assignments for the motors.
# For each motor, specify the GPIO pins connected to the 'step' and 'dir' inputs of the DRV8825.
detector_motor_pins = {'step': 17, 'dir': 18}  # Replace with the actual GPIO pins used for the detector motor.
sample_motor_pins = {'step': 23, 'dir': 24}    # Replace with the actual GPIO pins used for the sample motor.

# Set up the GPIO pins.
GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbering.
for motor_pins in [detector_motor_pins, sample_motor_pins]:
    for pin in motor_pins.values():
        GPIO.setup(pin, GPIO.OUT)  # Set each pin as an output.
        GPIO.output(pin, 0)  # Initialize the pin to low.

def move_motor(motor_pins, direction, steps=1):
    """
    Function to move a motor a certain number of steps in a given direction.

    Parameters:
    motor_pins (dict): Dictionary with 'step' and 'dir' pins of the motor.
    direction (str): Direction to rotate the motor ('cw' for clockwise, 'ccw' for counterclockwise).
    steps (int): Number of steps to move the motor.
    """
    # Set the direction of rotation.
    GPIO.output(motor_pins['dir'], GPIO.HIGH if direction == 'cw' else GPIO.LOW)
    
    # Move the motor the specified number of steps.
    for _ in range(steps):
        GPIO.output(motor_pins['step'], GPIO.HIGH)  # Trigger one step.
        time.sleep(0.001)  # Wait a short time.
        GPIO.output(motor_pins['step'], GPIO.LOW)   # Reset the step pin.
        time.sleep(0.001)  # Wait a short time before the next step.

try:
    # Get initial angles from the user.
    detector_angle = float(input("Enter initial detector angle: "))
    sample_angle = float(input("Enter initial sample plate angle: "))

    # Main loop to control the motors based on user input.
    while True:
        # Display the current angles.
        print(f"Current angles - Detector: {detector_angle}, Sample: {sample_angle}")

        # Ask the user for the next action.
        move_choice = input("Enter number of degrees to move: ")
        direction_choice = input("0 for smaller angle, 1 for wider angle: ")

        # Convert inputs to appropriate types.
        move_choice = float(move_choice)
        direction_choice = int(direction_choice)

        # Move the motors based on the user's choice.
        if direction_choice == 0:
            # Move for a smaller angle.
            move_motor(detector_motor_pins, 'cw', int(move_choice))
            move_motor(sample_motor_pins, 'ccw', int(move_choice))
            detector_angle += move_choice
            sample_angle -= move_choice
        elif direction_choice == 1:
            # Move for a wider angle.
            move_motor(detector_motor_pins, 'ccw', int(move_choice))
            move_motor(sample_motor_pins, 'cw', int(move_choice))
            detector_angle -= move_choice
            sample_angle += move_choice

except KeyboardInterrupt:
    # Handle the user pressing CTRL+C.
    print("Program terminated.")

finally:
    # Clean up the GPIO settings before exiting.
    GPIO.cleanup()
