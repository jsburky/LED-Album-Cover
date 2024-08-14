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
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={self.weather_api_key}"
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
        font.LoadFont("../../../fonts/9x18B.bdf")  # Adjust the path if necessary

        white = graphics.Color(255, 255, 255)
        lat, lon = self.get_location()
        last_temperature = None
        last_display = None

        while True:
            now = datetime.now()
            display = now.strftime("%I:%M")
            month = now.strftime("%b").upper()
            day = now.strftime("%d")

            # Fetch the temperature
            if lat and lon:
                temperature = self.get_temperature(lat, lon)
                if temperature is not None:
                    temp_display = f"{round(temperature)}°"
                    if last_temperature != temp_display:
                        last_temperature = temp_display
                        temperature_changed = True
                    else:
                        temperature_changed = False
                else:
                    temp_display = "N/A"
                    temperature_changed = True
            else:
                temp_display = "N/A"
                temperature_changed = True

            # Redraw only if something has changed
            if last_display != (display, month, day, temp_display):
                canvas.Clear()
                graphics.DrawText(canvas, font, 10, 14, white, display)
                graphics.DrawLine(canvas, 0, 18, 64, 18, white)
                graphics.DrawLine(canvas, 0, 45, 64, 45, white)
                graphics.DrawLine(canvas, 32, 18, 32, 45, white)
                graphics.DrawText(canvas, font, 35, 31, white, month)
                graphics.DrawText(canvas, font, 40, 43, white, day)
                graphics.DrawText(canvas, font, 3, 37, white, temp_display)
                last_display = (display, month, day, temp_display)

            # Sleep before next update
            time.sleep(1)  # Adjust as needed

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
