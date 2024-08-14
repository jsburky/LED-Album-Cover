#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
import requests

# To run add: 'sudo python /home/ledboard/rpi-rgb-led-matrix/bindings/python/samples/time.py --led-rows=64 --led-cols=64 --led-slowdown-gpio=4',
# To main.py under the number to select

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.weather_api_key = "API_KEY"  # Replace with your actual API key

    # Weather API: https://openweathermap.org/
    def get_location(self):
        try:
            response = requests.get('https://ipinfo.io/')
            data = response.json()
            loc = data['loc'].split(',')
            return loc[0], loc[1]  # Latitude, Longitude
        except Exception as e:
            print("Error fetching location:", e)
            return None, None

    def get_temperature(self, lat, lon):
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={self.weather_api_key}"
            response = requests.get(weather_url)
            data = response.json()
            temperature = data['main']['temp']
            return temperature
        except Exception as e:
            print("Error fetching weather data:", e)
            return None

    def run(self):
        canvas = self.matrix
        font = graphics.Font()

        # Load the font; make sure the path is correct
        font.LoadFont("../../../fonts/9x18B.bdf")  # Adjust the path if necessary

        white = graphics.Color(255, 255, 255)
        temperature = None
        lat, lon = self.get_location()

        while True:
            canvas.Clear()

            now = datetime.now()
            display = now.strftime("%I:%M")
            print(display)

            # Adjust these values based on your display size
            x_pos = 10  # x position of the text
            y_pos = 14  # y position of the baseline of the text

            # Draw the time on the canvas
            graphics.DrawText(canvas, font, x_pos, y_pos, white, display)
            graphics.DrawLine(canvas, 0, 18, 64, 18, white)
            graphics.DrawLine(canvas, 0, 45, 64, 45, white)
            graphics.DrawLine(canvas, 32, 18, 32, 45, white)

            month = now.strftime("%b").upper()
            day = now.strftime("%d")
            # year = now.strftime("%y")
            graphics.DrawText(canvas, font, 35, 31, white, month)
            graphics.DrawText(canvas, font, 40, 43, white, day)
            # graphics.DrawText(canvas, font, 40, 60, white, year)

            # Fetch temperature if not already fetched
            if not temperature and lat and lon:
                temperature = self.get_temperature(lat, lon)

            # Format the temperature display
            if temperature is not None:
                temp_display = f"{round(temperature)}°"  # Convert to string with rounded value
            else:
                temp_display = "N/A"

            # Display temperature if within the range
            if temperature is not None and -10 < temperature < 100:
                graphics.DrawText(canvas, font, 3, 37, white, temp_display)
            else:
                graphics.DrawText(canvas, font, 3, 37, white, temp_display)  # Adjust position if needed

            time.sleep(1)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
