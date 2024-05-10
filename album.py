import os
import requests
from flask import Flask, redirect, request
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import subprocess
import sys
import signal
import threading
import psutil

command = ["sudo", "python", "image_show.py", "--led-rows=64", "--led-cols=64", "--led-slowdown-gpio=4"]

instructions = ["sudo", "python", "address_display.py", "--led-rows=64", "--led-cols=64", "--led-slowdown-gpio=4"]

address_display = subprocess.Popen(instructions)

# Load environment variables from .env file
load_dotenv()

# Replace with your own Spotify API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Spotify API endpoints
API_BASE_URL = 'https://api.spotify.com/v1'

LOCAL_IP = '192.168.1.###'
PORT = 8888

# Your redirect URI (must be registered in your Spotify Developer Application)
REDIRECT_URI = f'http://{LOCAL_IP}:{PORT}/callback'

# Scopes determine the level of access your app has
SCOPES = ['user-read-currently-playing']

# Create a Flask web server
app = Flask(__name__)

current_track_id = None
image_show_process = None

# Function to request a Spotify access token using the Authorization Code grant
def get_access_token(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data)
    response_data = response.json()
    return response_data['access_token']

# Function to initiate the Spotify authorization process
def authorize_spotify():
    authorize_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={"".join(SCOPES)}&redirect_uri={REDIRECT_URI}'
    return redirect(authorize_url)

# Function to download the album cover image, resize it to 64x64 pixels, and extract RGB values
def download_and_extract_rgb_values(album_cover_url):
    image_path = os.path.join(os.getcwd(), 'album_cover.jpg')
    response = requests.get(album_cover_url)
    image = Image.open(BytesIO(response.content))

    if image.mode != "RGB":
        image = image.convert("RGB")
        
    image.save(image_path)
    # Resize the image to 64x64 pixels
    resized_image = image.resize((64, 64))
    resized_image_path = os.path.join(os.getcwd(), 'album_cover_resized.jpg')
    resized_image.save(resized_image_path)

    print(f'Album cover resized to 64x64 pixels and saved to {resized_image_path}')

    # Extract RGB values of each pixel
    pixel_data = list(resized_image.getdata())

    # Create a text file and write RGB values
    text_file_path = os.path.join(os.getcwd(), 'pixel_data.txt')
    with open(text_file_path, 'w') as text_file:
        for pixel in pixel_data:
            text_file.write(f'({pixel[0]}, {pixel[1]}, {pixel[2]})\n')

    print(f'RGB values of each pixel written to {text_file_path}')
    image.close()

# Function to start the image_show.py subprocess
def start_image_show():
    global image_show_process
    try:
        image_show_process = subprocess.Popen(command)
    except Exception as e:
        print(f'Error starting image_show subprocess: {e}')

# Function to stop the image_show.py subprocess
def stop_image_show():
    global image_show_process
    if image_show_process:
        image_show_process.send_signal(signal.SIGINT)
        image_show_process.wait()  # Wait for the subprocess to terminate
        
lock = threading.Lock()

# Function to periodically check for changes in the currently playing track
def check_currently_playing(access_token):
    global current_track_id
    try:
        response = requests.get(
            f'{API_BASE_URL}/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {access_token}',
            },
        )
        response.raise_for_status()
        track = response.json().get('item')
        # monitor_vitals()
        if track and track.get('id') != current_track_id:
            current_track_id = track['id']
            album_cover_url = track['album']['images'][0]['url']
            stop_image_show()  # Stop the subprocess
            download_and_extract_rgb_values(album_cover_url)
            start_image_show()  # Start the subprocess
            
    except requests.exceptions.RequestException as e:
        print(f'Error during network request: {e}')

    except Exception as e:
        print(f'Error during currently playing check: {e}')
        
def monitor_vitals():
    cpu_per = psutil.cpu_percent()
    print(f'CPU Usage: {cpu_per}%')
    mem = psutil.virtual_memory()
    total_memory = mem.total
    available_memory = mem.available
    used_memory = mem.used
    memory_percent = mem.percent
    print(f'Total Memory: {total_memory} bytes')
    print(f'Available Memory: {available_memory} bytes')
    print(f'Used Memory: {used_memory} bytes')
    print(f'Memory Usage: {memory_percent}%')
    print('-' * 30)
    
# Callback route to handle Spotify's redirect after user authorization
@app.route('/callback')
def callback():
    code = request.args.get('code')

    if code:
        try:
            access_token = get_access_token(code)
            
            def check_loop():
                while True:
                    check_currently_playing(access_token)
                    import time
                    time.sleep(1)  # Check every second

            threading.Thread(target=check_loop).start()
            start_image_show()  # Start the image_show.py subprocess
            address_display.terminate()
            return 'Authorization complete. You can close this window.'

        except Exception as e:
            print(f'Error: {e}')
            return 'Error during authorization.', 500
    else:
        print('No authorization code received.')
        return 'No authorization code received.', 400

# Route to initiate the Spotify authorization process
@app.route('/authorize')
def authorize_spotify_route():
    return authorize_spotify()

# Start the Flask server on the specified port
if __name__ == '__main__':
    app.run(host=LOCAL_IP, port=PORT)
