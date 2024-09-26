#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
from datetime import datetime, timedelta
import requests
import threading
import json
import os

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.weather_api_key = "YOUR_WEATHER_API_KEY"
        self.polygon_api_key = "YOUR_POLYGON_API_KEY"
        self.stock_symbols = [
            "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NFLX", "BA", "NVDA", "BABA", "FB", "V", "JPM", "JNJ", "WMT", "PG",
            "DIS", "MA", "PYPL", "UNH", "HD", "VZ", "ADBE", "CMCSA", "NFLX", "PFE", "KO", "PEP", "T", "ABT", "CSCO",
            "COST", "LLY", "AVGO", "MRK", "INTC", "XOM", "MCD", "NKE", "IBM", "CRM", "CVX", "TXN", "HON", "MDT", "WFC",
            "QCOM", "ACN", "ORCL", "LIN", "SCHW", "SBUX", "UPS", "MS", "BLK", "PM", "RTX", "NEE", "AMGN", "MMM", "GS",
            "CAT", "INTU", "AMAT", "BKNG", "TMO", "ISRG", "SPGI", "ZTS", "BA", "GE", "USB", "MU", "DE", "FDX", "CI",
            "LOW", "DHR", "LMT", "SYK", "PLD", "ADI", "COP", "AMT", "AON", "FIS", "GILD", "VRTX", "CB", "C", "NOW",
            "MMC", "TFC", "ADP", "DUK", "BDX", "CL", "TGT", "BMY", "ECL", "ITW", "APD", "CCI", "EW", "CME", "FISV",
            "MSCI", "NSC", "MAR", "ICE", "MDLZ", "AEP", "EOG", "PGR", "MCO", "SO", "KDP", "A", "PPG", "ETN", "AIG",
            "AZO", "CDW", "CMG", "DG", "EQIX", "HSY", "PH", "SHW", "SNPS", "WM", "ADM", "BAX", "AFL", "ALL", "BXP", 
            "COF", "CPRT", "CTAS", "DD", "DLTR", "DTE", "EL", "EMR", "EXR", "FMC", "GLW", "HAS", "HUM", "IDXX", "IFF"
        ]
        self.stock_prices = self.load_stock_prices()
        self.last_update_times = {symbol: None for symbol in self.stock_symbols}
        self.update_interval = timedelta(minutes=1)
        self.update_thread = threading.Thread(target=self.schedule_updates)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.last_temp_update = 0
        self.temp_update_interval = 20

        # Path to the folder with your weather images (32x26 px)
        self.weather_images_path = "./weather_images/"
        self.weather_images = {
            "clear_sky_day": "clear_sky_day.png",
            "clear_sky_night": "clear_sky_night.png",
            "cloudy": "cloudy.png",
            "partially_cloudy_day": "partially_cloudy_day.png",
            "partially_cloudy_night": "partially_cloudy_night.png",
            "windy": "windy.png",
            "rainy": "rainy.png",
            "snowy": "snowy.png",
            "thunder": "thunder.png"
        }

    def load_stock_prices(self):
        """Load cached stock prices."""
        try:
            if os.path.exists("stock_prices.json"):
                with open("stock_prices.json", "r") as f:
                    return json.load(f)
            else:
                return {symbol: None for symbol in self.stock_symbols}
        except Exception as e:
            print(f"Error loading stock prices: {e}")
            return {symbol: None for symbol in self.stock_symbols}

    def save_stock_prices(self):
        """Save the stock prices to a JSON file."""
        try:
            with open("stock_prices.json", "w") as f:
                json.dump(self.stock_prices, f)
        except Exception as e:
            print(f"Error saving stock prices: {e}")

    def get_weather_image(self, condition):
        """Loads the image based on the current weather condition."""
        image_path = os.path.join(self.weather_images_path, self.weather_images.get(condition, "clear_sky_day.png"))
        image = Image.open(image_path)
        return image.convert('RGB')

    def display_weather_image(self, buffer, condition):
        """Displays the weather image in the 32x26 px area."""
        image = self.get_weather_image(condition)
        image = image.resize((32, 26))  # Resize to fit the 32x26 display area
        buffer.SetImage(image, 3, 20)  # Position it at (3, 20)

    def run(self):
        canvas = self.matrix
        buffer = self.matrix.CreateFrameCanvas()

        top_font = graphics.Font()
        top_font.LoadFont("../../../fonts/9x18B.bdf")

        ticker_font = graphics.Font()
        ticker_font.LoadFont("../../../fonts/6x10.bdf")
        ticker_x = buffer.width

        white = graphics.Color(255, 255, 255)
        lat, lon = self.get_location()
        last_temperature = None

        ticker_text = self.get_stock_data()

        # Alternate between temperature and weather image
        display_temperature = True
        last_switch_time = time.time()

        while True:
            now = datetime.now()
            display = now.strftime("%I:%M")
            month = now.strftime("%b").upper()
            day = now.strftime("%d")

            # Fetch the temperature every 20 seconds
            if time.time() - self.last_temp_update >= self.temp_update_interval:
                if lat and lon:
                    temperature = self.get_temperature(lat, lon)
                    if temperature is not None:
                        temp_display = f"{round(temperature)}°"
                        if last_temperature != temp_display:
                            last_temperature = temp_display
                    else:
                        temp_display = "N/A"
                else:
                    temp_display = "N/A"

                self.last_temp_update = time.time()

            # Draw on the buffer
            buffer.Clear()

            # Draw the top portion of the display
            graphics.DrawText(buffer, top_font, 10, 14, white, display)
            graphics.DrawLine(buffer, 0, 18, 64, 18, white)
            graphics.DrawLine(buffer, 0, 45, 64, 45, white)
            graphics.DrawLine(buffer, 32, 18, 32, 45, white)
            graphics.DrawText(buffer, top_font, 35, 31, white, month)
            graphics.DrawText(buffer, top_font, 40, 43, white, day)

            # Alternate between showing temperature and weather image every 5 seconds
            if time.time() - last_switch_time >= 5:
                display_temperature = not display_temperature
                last_switch_time = time.time()

            if display_temperature:
                graphics.DrawText(buffer, top_font, 3, 37, white, last_temperature if last_temperature else "N/A")
            else:
                weather_condition = "clear_sky_day"  # Example, replace with actual condition
                self.display_weather_image(buffer, weather_condition)

            # Draw the bottom portion (ticker text)
            graphics.DrawText(buffer, ticker_font, ticker_x, 59, white, ticker_text)
            ticker_x -= 1
            if ticker_x < -len(ticker_text) * 6:  # Adjust width as needed
                ticker_x = buffer.width
                ticker_text = self.get_stock_data()

            # Swap buffer with canvas to update display
            buffer = self.matrix.SwapOnVSync(buffer)

            time.sleep(0.05)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
