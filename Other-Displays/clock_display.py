#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime, timedelta
import requests
import threading
import json
import os

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.weather_api_key = "YOUR_WEATHER_API_KEY"  # Replace with your actual Weather API key
        self.polygon_api_key = "YOUR_POLYGON_API_KEY"  # Replace with your Polygon.io API key
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

        self.stock_prices = self.load_stock_prices()  # Load cached prices
        self.last_update_times = {symbol: None for symbol in self.stock_symbols}  # Track last update times for each stock
        self.update_interval = timedelta(minutes=1)  # Update interval for each stock
        self.update_thread = threading.Thread(target=self.schedule_updates)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.last_temp_update = 0  # Timestamp for the last temperature update
        self.temp_update_interval = 20  # Temperature update interval in seconds

    def load_stock_prices(self):
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
        try:
            with open("stock_prices.json", "w") as f:
                json.dump(self.stock_prices, f)
        except Exception as e:
            print(f"Error saving stock prices: {e}")

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

    def update_stock_price(self, symbol):
        try:
            url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev'
            params = {
                'apiKey': self.polygon_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                # Fetch the most recent end-of-day data
                recent_data = data['results'][0]
                price = recent_data['c']
                self.stock_prices[symbol] = f"{symbol}: ${float(price):.2f}"
            else:
                # Use cached price if available, otherwise set to N/A
                self.stock_prices[symbol] = self.stock_prices.get(symbol, f"{symbol}: N/A")
            self.last_update_times[symbol] = datetime.now()
            self.save_stock_prices()  # Save prices after each update
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            self.stock_prices[symbol] = self.stock_prices.get(symbol, f"{symbol}: N/A")

    def schedule_updates(self):
        while True:
            for symbol in self.stock_symbols:
                last_update_time = self.last_update_times[symbol]
                if last_update_time is None or datetime.now() - last_update_time >= self.update_interval:
                    self.update_stock_price(symbol)
                    # Respect the rate limit by sleeping between API calls
                    time.sleep(60 / 5)  # 60 seconds divided by 5 requests
            time.sleep(10)  # Small delay to prevent tight looping

    def get_stock_data(self):
        # Return cached stock prices, ensuring all values are strings
        return " | ".join(price if price else f"{symbol}: N/A" for symbol, price in self.stock_prices.items())

    def run(self):
        # Create two canvases: one for the display and one for the buffer
        canvas = self.matrix
        buffer = self.matrix.CreateFrameCanvas()

        top_font = graphics.Font()
        top_font.LoadFont("../../../fonts/9x18B.bdf")  # Adjust the path if necessary

        ticker_font = graphics.Font()
        ticker_font.LoadFont("../../../fonts/6x10.bdf")
        ticker_x = buffer.width

        white = graphics.Color(255, 255, 255)
        lat, lon = self.get_location()
        last_temperature = None

        ticker_update_interval = 15  # Update ticker text every 15 seconds
        last_ticker_update = time.time()

        ticker_text = self.get_stock_data()  # Initial ticker text

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
                            temperature_changed = True
                        else:
                            temperature_changed = False
                    else:
                        temp_display = "N/A"
                        temperature_changed = True
                else:
                    temp_display = "N/A"
                    temperature_changed = True

                self.last_temp_update = time.time()  # Update the timestamp

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
                # Fetch new stock data when ticker is fully off screen
                ticker_text = self.get_stock_data()

            # Swap buffer with canvas to update display
            buffer = self.matrix.SwapOnVSync(buffer)

            # Sleep for a short interval to update the ticker smoothly
            time.sleep(0.05)  # Adjust as needed for smooth scrolling

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
