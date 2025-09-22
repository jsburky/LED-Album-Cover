#!/usr/env/bin python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime, timedelta
import requests
import threading
import json
import os
import logging

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

        # --- Setup Logging ---
        self.logger = logging.getLogger("GraphicsTest")
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler('error.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
        self.update_interval = timedelta(minutes=5) # Increased interval for more complex query
        self.update_thread = threading.Thread(target=self.schedule_updates)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.last_weather_update = 0
        self.weather_update_interval = 300  # Fetch new weather data every 5 minutes

        self.weather_data = None
        self.show_weather_icon = False
        self.last_weather_toggle_time = 0
        self.weather_toggle_interval = 15 # Switch between temp and icon every 15 seconds

    def load_stock_prices(self):
        try:
            if os.path.exists("stock_prices.json"):
                with open("stock_prices.json", "r") as f:
                    return json.load(f)
            else:
                return {} # Initialize as empty dict for new structure
        except Exception:
            self.logger.exception("Error loading stock prices")
            return {}

    def save_stock_prices(self):
        try:
            with open("stock_prices.json", "w") as f:
                json.dump(self.stock_prices, f)
        except Exception:
            self.logger.exception("Error saving stock prices")

    def get_location(self):
        try:
            response = requests.get('https://ipinfo.io/')
            data = response.json()
            loc = data['loc'].split(',')
            return loc[0], loc[1]
        except Exception:
            self.logger.exception("Error fetching location")
            return None, None

    def get_weather_data(self, lat, lon):
        """Fetches temperature, condition, and day/night status."""
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={self.weather_api_key}"
            response = requests.get(weather_url)
            data = response.json()
            temperature = float(data['main']['temp'])
            condition = data['weather'][0]['main']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']
            current_time = time.time()
            is_day = sunrise < current_time < sunset
            return {"temperature": temperature, "condition": condition, "is_day": is_day}
        except Exception:
            self.logger.exception("Error fetching weather data")
            return None

    def update_stock_price(self, symbol):
        """Fetches last two trading days to determine price change."""
        today = datetime.now()
        # Look back 5 days to ensure we capture at least two trading days
        to_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        from_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')

        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}'
        params = {'apiKey': self.polygon_api_key, 'sort': 'desc', 'limit': 2}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses
            data = response.json()

            status = 'flat'
            price_text = f"{symbol}: N/A"

            if 'results' in data and len(data['results']) > 0:
                latest_close = data['results'][0]['c']
                price_text = f"{symbol}: ${latest_close:.2f}"

                if len(data['results']) > 1:
                    previous_close = data['results'][1]['c']
                    if latest_close > previous_close:
                        status = 'up'
                    elif latest_close < previous_close:
                        status = 'down'

            self.stock_prices[symbol] = {'text': price_text, 'status': status}
            self.last_update_times[symbol] = datetime.now()
            self.save_stock_prices()

        except Exception:
            self.logger.exception(f"Error fetching stock data for {symbol}")
            # Use cached data if available on error
            if symbol not in self.stock_prices:
                self.stock_prices[symbol] = {'text': f"{symbol}: N/A", 'status': 'flat'}


    def schedule_updates(self):
        while True:
            try:
                for symbol in self.stock_symbols:
                    last_update_time = self.last_update_times.get(symbol)
                    if last_update_time is None or datetime.now() - last_update_time >= self.update_interval:
                        self.update_stock_price(symbol)
                        time.sleep(12)  # Respect API rate limit (5 calls/min)
                time.sleep(10)
            except Exception:
                self.logger.exception("An error occurred in the schedule_updates thread")
                time.sleep(60) # Wait before retrying after an error

    def draw_layered_icon(self, canvas, x_offset, y_offset, layers):
        """Draws a weather icon by layering multiple 30x24 art assets."""
        for art, color in layers:
            for y, row_str in enumerate(art):
                for x, char in enumerate(row_str):
                    if char == 'X':
                        canvas.SetPixel(x + x_offset, y + y_offset, color.red, color.green, color.blue)

    def draw_ticker_arrow(self, canvas, x, y, status, colors):
        """Manually draws a pixel art arrow for the ticker."""
        green, red, yellow = colors
        # The 6x10 font's baseline is at y. Text is ~10px tall, from y-9 to y.
        # This calculation centers the new 3px tall shapes vertically.
        arrow_y = y - 6
        width = 5 # Width of the arrow art plus padding

        if status == 'up':
            color = green
            # Top point
            canvas.SetPixel(x + 2, arrow_y, color.red, color.green, color.blue)
            # Middle row
            canvas.SetPixel(x + 1, arrow_y + 1, color.red, color.green, color.blue)
            canvas.SetPixel(x + 2, arrow_y + 1, color.red, color.green, color.blue)
            canvas.SetPixel(x + 3, arrow_y + 1, color.red, color.green, color.blue)
            # Bottom row
            canvas.SetPixel(x,     arrow_y + 2, color.red, color.green, color.blue)
            canvas.SetPixel(x + 1, arrow_y + 2, color.red, color.green, color.blue)
            canvas.SetPixel(x + 2, arrow_y + 2, color.red, color.green, color.blue)
            canvas.SetPixel(x + 3, arrow_y + 2, color.red, color.green, color.blue)
            canvas.SetPixel(x + 4, arrow_y + 2, color.red, color.green, color.blue)
            
        elif status == 'down':
            color = red
            # Top row
            canvas.SetPixel(x,     arrow_y, color.red, color.green, color.blue)
            canvas.SetPixel(x + 1, arrow_y, color.red, color.green, color.blue)
            canvas.SetPixel(x + 2, arrow_y, color.red, color.green, color.blue)
            canvas.SetPixel(x + 3, arrow_y, color.red, color.green, color.blue)
            canvas.SetPixel(x + 4, arrow_y, color.red, color.green, color.blue)
            # Middle row
            canvas.SetPixel(x + 1, arrow_y + 1, color.red, color.green, color.blue)
            canvas.SetPixel(x + 2, arrow_y + 1, color.red, color.green, color.blue)
            canvas.SetPixel(x + 3, arrow_y + 1, color.red, color.green, color.blue)
            # Bottom point
            canvas.SetPixel(x + 2, arrow_y + 2, color.red, color.green, color.blue)

        else: # flat
            color = yellow
            # Draw a 3-pixel tall solid bar, 5 pixels wide
            for row in range(3):
                for col in range(5):
                    canvas.SetPixel(x + col, arrow_y + row, color.red, color.green, color.blue)
        return width


    def run(self):
        canvas = self.matrix
        buffer = self.matrix.CreateFrameCanvas()

        top_font = graphics.Font()
        # Make sure this path is correct for your environment
        top_font.LoadFont("../../../fonts/9x18B.bdf")

        ticker_font = graphics.Font()
        # Make sure this path is correct for your environment
        ticker_font.LoadFont("../../../fonts/6x10.bdf")

        ticker_x = buffer.width
        total_ticker_width = 0

        # --- Color Palette ---
        white = graphics.Color(255, 255, 255)
        green = graphics.Color(0, 255, 0)
        red = graphics.Color(255, 0, 0)
        yellow = graphics.Color(255, 255, 0)
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

        lat, lon = self.get_location()
        self.last_weather_toggle_time = time.time()

        try:
            while True:
                now = datetime.now()
                display_time = now.strftime("%I:%M")
                month = now.strftime("%b").upper()
                day = now.strftime("%d")

                if time.time() - self.last_weather_toggle_time >= self.weather_toggle_interval:
                    self.show_weather_icon = not self.show_weather_icon
                    self.last_weather_toggle_time = time.time()

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
                        
                        self.draw_layered_icon(buffer, 1, 20, layers)

                    else:
                        temp_display = f"{round(self.weather_data['temperature'])}°"
                        font_width = 9
                        text_width = len(temp_display) * font_width
                        centered_x = (32 - text_width) // 2
                        graphics.DrawText(buffer, top_font, centered_x, 37, white, temp_display)
                else:
                    graphics.DrawText(buffer, top_font, 9, 37, white, "...")

                # --- Draw Scrolling Ticker ---
                current_x = ticker_x
                temp_total_width = 0
                separator = " | "
                for symbol in self.stock_symbols:
                    stock_data = self.stock_prices.get(symbol)
                    if not stock_data: continue

                    # Draw Price Text
                    price_text = stock_data['text'] + " "
                    text_width = graphics.DrawText(buffer, ticker_font, current_x, 59, white, price_text)
                    current_x += text_width
                    temp_total_width += text_width

                    # Draw Arrow
                    status = stock_data.get('status', 'flat')
                    arrow_width = self.draw_ticker_arrow(buffer, current_x, 59, status, (green, red, yellow))
                    current_x += arrow_width
                    temp_total_width += arrow_width

                    # Draw Separator
                    sep_width = graphics.DrawText(buffer, ticker_font, current_x, 59, white, separator)
                    current_x += sep_width
                    temp_total_width += sep_width

                total_ticker_width = temp_total_width
                ticker_x -= 1
                if ticker_x < -total_ticker_width:
                    ticker_x = buffer.width

                buffer = self.matrix.SwapOnVSync(buffer)
                time.sleep(0.05)
        except Exception:
            self.logger.exception("An unhandled error occurred in the main run loop")
        finally:
            # Optional cleanup
            print("Exiting.")

if __name__ == "__main__":
    try:
        graphics_test = GraphicsTest()
        if not graphics_test.process():
            graphics_test.print_help()
    except Exception:
        logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.exception("A critical error occurred at the top level")
        print("A critical error occurred. Check error.log for details.")
