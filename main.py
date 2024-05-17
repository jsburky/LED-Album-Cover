from evdev import InputDevice, categorize, ecodes
import subprocess
import threading

# Find the event for your USB keypad (use `ls /dev/input/` to list input devices)
# Replace '/dev/input/eventX' with the appropriate event number for your keypad
dev = InputDevice('/dev/input/event#')

# Define the commands corresponding to each key
command_mapping = {
    '0': None,  # No command for '0'
    '1': 'sudo python album.py',
    '2': 'command2',
    '3': 'command3',
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
