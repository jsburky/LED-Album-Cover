#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
import requests

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
            temperature = float(data['main']['temp'])
            return temperature
        except Exception as e:
            print("Error fetching weather data:", e)
            return None

    def run(self):
        # Create two canvases: one for the display and one for the buffer
        canvas = self.matrix
        buffer = self.matrix.CreateFrameCanvas()

        top_font = graphics.Font()
        top_font.LoadFont("../../../fonts/9x18B.bdf")  # Adjust the path if necessary

        ticker_font = graphics.Font()
        ticker_font.LoadFont("../../../fonts/6x10.bdf")
        ticker_text = "Sample News Ticker: Scrolling Text Here! " * 3  # Adjust text as needed
        ticker_x = buffer.width

        white = graphics.Color(255, 255, 255)
        lat, lon = self.get_location()
        last_temperature = None

        while True:
            now = datetime.now()
            display = now.strftime("%I:%M")
            month = now.strftime("%b").upper()
            day = now.strftime("%d")

            # Draw on the buffer
            buffer.Clear()

            # Draw the top portion of the display
            graphics.DrawText(buffer, top_font, 10, 14, white, display)
            graphics.DrawLine(buffer, 0, 18, 64, 18, white)
            graphics.DrawLine(buffer, 0, 45, 64, 45, white)
            graphics.DrawLine(buffer, 32, 18, 32, 45, white)
            graphics.DrawText(buffer, top_font, 35, 31, white, month)
            graphics.DrawText(buffer, top_font, 40, 43, white, day)
            graphics.DrawText(buffer, top_font, 3, 37, white, last_temperature if last_temperature else "N/A")

            # Draw the bottom portion (ticker text)
            graphics.DrawText(buffer, ticker_font, ticker_x, 59, white, ticker_text)
            ticker_x -= 1
            if ticker_x < -len(ticker_text) * 6:  # Adjust width as needed
                ticker_x = buffer.width

            # Swap buffer with canvas to update display
            buffer = self.matrix.SwapOnVSync(buffer)

            # Sleep for 1 second to refresh the entire screen
            time.sleep(0.05)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
