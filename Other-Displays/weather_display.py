#!/usr/env/bin python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime, timedelta
import requests
import threading
import json
import os


# Centered high to allow peeking over clouds
SUN_ART = [
    "              X                ",
    "              X                ",
    "              X                ",
    "  X           X           X     ",
    "   X          X          X      ",
    "    X                   X      ",
    "     X     XXXXXXX     X      ",
    "      X  XXXXXXXXXXX  X       ",
    "        XXXXXXXXXXXXX        ",
    "       XXXXXXXXXXXXXXX       ",
    "      XXXXXXXXXXXXXXXXX      ",
    "XXXX  XXXXXXXXXXXXXXXXX  XXXX    ",
    "      XXXXXXXXXXXXXXXXX      ",
    "      XXXXXXXXXXXXXXXXX      ",
    "       XXXXXXXXXXXXXXX       ",
    "        XXXXXXXXXXXXX        ",
    "      X  XXXXXXXXXXX  X       ",
    "     X     XXXXXXX     X      ",
    "    X                   X      ",
    "   X          X          X      ",
    "  X           X           X     ",
    "              X                ",
    "              X                ",
    "              X                ",
    "                              ",
]

PARTIAL_SUN_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "           XXXXXXX          ",
    "         XXXXXXXXXXX        ",
    "        XXXXXXXXXXXXX       ",
    "       XXXXXXXXXXXXXXX      ",
    "      XXXXXXXXXXXXXXXXX     ",
    "      XXXXXXXXXXXXXXXXX     ",
    "      XXXXXXXXXXXXXXXXX     ",
    "      XXXXXXXXXXXXXXXXX     ",
    "       XXXXXXXXXXXXXXX      ",
    "        XXXXXXXXXXXXX       ",
    "         XXXXXXXXXXX        ",
    "           XXXXXXX          ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]

# Positioned to align with the sun
MOON_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "             XXXXX            ",
    "           XXXXX              ",
    "          XXXXX               ",
    "         XXXXX                ",
    "        XXXXXX                ",
    "       XXXXXXX                ",
    "       XXXXXXX                ",
    "       XXXXXXX                ",
    "       XXXXXXX                ",
    "       XXXXXXXX               ",
    "       XXXXXXXXX              ",
    "       XXXXXXXXX              ",
    "        XXXXXXXXXX      X     ",
    "        XXXXXXXXXXXXX XXX     ",
    "         XXXXXXXXXXXXXX       ",
    "           XXXXXXXXXXX        ",
    "             XXXXXXX          ",
    "                              ",
    "                              ",
    "                              ",
]

# The user-specified cloud, positioned lower in the frame
CLOUD_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "             XXXXX            ",
    "          XXXXXXXXX           ",
    "     XXXXXXXXXXXXXXXXXXX      ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXX    ",
    "     XXXXXXXXXXXXXXXXXXXX     ",
    "       XXXXXXXXXXXXXXXX       ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]

PARTIAL_CLOUD = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "             XXXXX            ",
    "          XXXXXXXXX           ",
    "     XXXXXXXXXXXXXXXXXXX      ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXX    ",
    "     XXXXXXXXXXXXXXXXXXXX     ",
    "       XXXXXXXXXXXXXXXX       ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]


MOON_CLOUD_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "             XXXXX            ",
    "          XXXXXXXXX           ",
    "     XXXXXXXXXXXXXXXXXXX      ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXXX   ",
    "   XXXXXXXXXXXXXXXXXXXXXXX    ",
    "     XXXXXXXXXXXXXXXXXXXX     ",
    "       XXXXXXXXXXXXXXXX       ",
    "                              ",
    "                              ",
    "                              ",

]


# Rain positioned to fall from the cloud
RAIN_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "     X    X    X    X         ",
    "    X    X    X    X          ",
    "   X    X    X    X           ",
    "  X    X    X    X            ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]

# Snow positioned to fall from the cloud
SNOW_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "    X   X       X   X         ",
    "     X X   X X   X X          ",
    "      X     X     X           ",
    "     X X   X X   X X          ",
    "    X   X       X   X         ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]

# Bolt positioned to emerge from the cloud
BOLT_ART = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "           XXXX               ",
    "          XXXXX               ",
    "           XXXX               ",
    "            XXX               ",
    "           XXXX               ",
    "          XXX                 ",
    "         XXXX                 ",
    "          XX                  ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
]


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

        self.stock_prices = self.load_stock_prices()
        self.last_update_times = {symbol: None for symbol in self.stock_symbols}
        self.update_interval = timedelta(minutes=1)
        self.update_thread = threading.Thread(target=self.schedule_updates)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.last_weather_update = 0
        self.weather_update_interval = 300  # Fetch new weather data every 5 minutes

        # New variables for weather icon display
        self.weather_data = None  # Will store the dictionary of weather info
        self.show_weather_icon = False
        self.last_weather_toggle_time = 0
        self.weather_toggle_interval = 15 # Switch between temp and icon every 15 seconds

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
            return loc[0], loc[1]
        except Exception as e:
            print("Error fetching location:", e)
            return None, None

    def get_weather_data(self, lat, lon):
        """Fetches temperature, condition, and day/night status."""
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={self.weather_api_key}"
            response = requests.get(weather_url)
            data = response.json()

            temperature = float(data['main']['temp'])
            condition = data['weather'][0]['main']  # e.g., "Clear", "Clouds", "Rain"

            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']
            current_time = time.time()  # This is a UTC timestamp

            is_day = sunrise < current_time < sunset

            return {
                "temperature": temperature,
                "condition": condition,
                "is_day": is_day
            }
        except Exception as e:
            print("Error fetching weather data:", e)
            return None

    def update_stock_price(self, symbol):
        try:
            url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev'
            params = {'apiKey': self.polygon_api_key}
            response = requests.get(url, params=params)
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                recent_data = data['results'][0]
                price = recent_data['c']
                self.stock_prices[symbol] = f"{symbol}: ${float(price):.2f}"
            else:
                self.stock_prices[symbol] = self.stock_prices.get(symbol, f"{symbol}: N/A")
            self.last_update_times[symbol] = datetime.now()
            self.save_stock_prices()
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            self.stock_prices[symbol] = self.stock_prices.get(symbol, f"{symbol}: N/A")

    def schedule_updates(self):
        while True:
            for symbol in self.stock_symbols:
                last_update_time = self.last_update_times[symbol]
                if last_update_time is None or datetime.now() - last_update_time >= self.update_interval:
                    self.update_stock_price(symbol)
                    time.sleep(12)  # Respect the 5 requests/minute limit
            time.sleep(10)

    def get_stock_data(self):
        return " | ".join(price if price else f"{symbol}: N/A" for symbol, price in self.stock_prices.items())

    def draw_layered_icon(self, canvas, x_offset, y_offset, layers):
        """Draws a weather icon by layering multiple 30x24 art assets.

        Args:
            canvas: The canvas to draw on.
            x_offset: The top-left x-coordinate for the icon.
            y_offset: The top-left y-coordinate for the icon.
            layers: A list of tuples, where each is (art_array, color).
                    Layers are drawn in order, with later layers drawing on top.
        """
        for art, color in layers:
            # Each art asset is 24 rows high
            for y, row_str in enumerate(art):
                # And 30 columns wide
                for x, char in enumerate(row_str):
                    if char == 'X':
                        canvas.SetPixel(x + x_offset, y + y_offset, color.red, color.green, color.blue)

    def run(self):
        canvas = self.matrix
        buffer = self.matrix.CreateFrameCanvas()

        top_font = graphics.Font()
        top_font.LoadFont("../../../fonts/9x18B.bdf")

        ticker_font = graphics.Font()
        ticker_font.LoadFont("../../../fonts/6x10.bdf")
        ticker_x = buffer.width

        # --- Color Palette ---
        white = graphics.Color(255, 255, 255)
        sun_yellow = graphics.Color(255, 255, 0)
        moon_gray = graphics.Color(217, 214, 63)
        day_cloud_gray = graphics.Color(200, 200, 200)
        night_cloud_gray = graphics.Color(150, 150, 150)
        rain_cloud_gray = graphics.Color(180, 180, 180)
        snow_cloud_gray = graphics.Color(200, 200, 200)
        storm_cloud_gray = graphics.Color(100, 100, 100)
        fog_cloud_gray = graphics.Color(170, 170, 170)
        rain_blue = graphics.Color(100, 149, 237)
        bolt_yellow = graphics.Color(255, 255, 0)


        # lat, lon = self.get_location()

        ticker_text = self.get_stock_data()
        self.last_weather_toggle_time = time.time()

        while True:
            now = datetime.now()
            display_time = now.strftime("%I:%M")
            month = now.strftime("%b").upper()
            day = now.strftime("%d")

            # --- Weather/Icon Toggle Logic ---
            if time.time() - self.last_weather_toggle_time >= self.weather_toggle_interval:
                self.show_weather_icon = not self.show_weather_icon
                self.last_weather_toggle_time = time.time()

            # --- Fetch fresh weather data periodically ---
            if time.time() - self.last_weather_update >= self.weather_update_interval:
                if lat and lon:
                    fetched_data = self.get_weather_data(lat, lon)
                    if fetched_data:
                        self.weather_data = fetched_data
                self.last_weather_update = time.time()

            buffer.Clear()

            # --- Draw the static parts of the display ---
            graphics.DrawText(buffer, top_font, 10, 14, white, display_time)
            graphics.DrawLine(buffer, 0, 18, 64, 18, white)
            graphics.DrawLine(buffer, 0, 45, 64, 45, white)
            graphics.DrawLine(buffer, 32, 18, 32, 45, white)
            graphics.DrawText(buffer, top_font, 35, 31, white, month)
            graphics.DrawText(buffer, top_font, 40, 43, white, day)

            # --- Temperature / Icon Drawing Logic ---
            if self.weather_data:
                if self.show_weather_icon:
                    condition = self.weather_data['condition']
                    is_day = self.weather_data['is_day']
                    layers = []
                    condition = 'Rain'
                    if condition == "Clear":
                        layers = [(SUN_ART, sun_yellow)] if is_day else [(MOON_ART, moon_gray)]

                    elif condition == "Clouds":
                        if is_day:
                            layers = [(PARTIAL_SUN_ART, sun_yellow), (PARTIAL_CLOUD, day_cloud_gray)]
                        else:
                            layers = [(MOON_ART, moon_gray), (MOON_CLOUD_ART, night_cloud_gray)]

                    elif condition == "Thunderstorm":
                        layers = [(CLOUD_ART, storm_cloud_gray), (BOLT_ART, bolt_yellow)]

                    elif condition in ["Rain", "Drizzle"]:
                        layers = [(CLOUD_ART, rain_cloud_gray), (RAIN_ART, rain_blue)]

                    elif condition == "Snow":
                        layers = [(CLOUD_ART, snow_cloud_gray), (SNOW_ART, white)]

                    else:  # Default for Fog, Mist, Haze, etc.
                        layers = [(CLOUD_ART, fog_cloud_gray)]
                    
                    # Draw the final composed icon, centered in the panel
                    self.draw_layered_icon(buffer, 1, 20, layers)

                else:
                    # Draw centered temperature text
                    temp_display = f"{round(self.weather_data['temperature'])}°"
                    font_width = 9  # 9x18B font
                    text_width = len(temp_display) * font_width
                    centered_x = (32 - text_width) // 2
                    graphics.DrawText(buffer, top_font, centered_x, 37, white, temp_display)
            else:
                # Fallback if no weather data is available
                graphics.DrawText(buffer, top_font, 9, 37, white, "...")

            # --- Draw the scrolling ticker ---
            graphics.DrawText(buffer, ticker_font, ticker_x, 59, white, ticker_text)
            ticker_x -= 1
            if ticker_x < -len(ticker_text) * 6:
                ticker_x = buffer.width
                ticker_text = self.get_stock_data()

            buffer = self.matrix.SwapOnVSync(buffer)
            time.sleep(0.05)

if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()

