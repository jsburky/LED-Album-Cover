from evdev import InputDevice, categorize, ecodes
import subprocess
import threading

# Find the event for your USB keypad (use ls /dev/input/ to list input devices)
# Replace '/dev/input/eventX' with the appropriate event number for your keypad
dev = InputDevice('/dev/input/eventX')

# Define the commands corresponding to each key
command_mapping = {
    '0': '/home/ledboard/shutdown_services.sh',
    '1': 'sudo python3 /home/ledboard/rpi-rgb-led-matrix/bindings/python/samples/album.py',
    # Add more commands as needed
}

# Global variable to store the current subprocess
current_process = None

# Define a function to execute commands
def execute_command(key):
    global current_process
    command = command_mapping.get(key)
    if current_process is not None:
        current_process.terminate()
        print("Cancelled current command")
        current_process = None

    if command is not None:
        # If the command is the shutdown script, execute it directly
        if key == '0':
            subprocess.Popen(command, shell=True)
        else:
            current_process = subprocess.Popen(command.split())

# Define a function to read input from the keypad
def read_keypad():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                key = str(key_event.keycode[-1])
                execute_command(key)

# Start reading input from the keypad on a separate thread
keypad_thread = threading.Thread(target=read_keypad)
keypad_thread.daemon = True
keypad_thread.start()

# Keep the main thread alive
keypad_thread.join()
