#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime

#To run add: 'sudo python /home/ledboard/rpi-rgb-led-matrix/bindings/python/samples/time.py --led-rows=64 --led-cols=64 --led-slowdown-gpio=4',
#To main.py under the number to select
class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix
        font = graphics.Font()

        # Load the font; make sure the path is correct
        font.LoadFont("../../../fonts/9x18B.bdf")  # Adjust the path if necessary

        white = graphics.Color(255, 255, 255)

        while True:
            canvas.Clear()

            now = datetime.now()
            display = now.strftime("%I:%M")
            print(display)

            # Adjust these values based on your display size
            x_pos = 10  # x position of the text
            y_pos = 15  # y position of the baseline of the text

            # Draw the time on the canvas
            graphics.DrawText(canvas, font, x_pos, y_pos, white, display)
            graphics.DrawLine(canvas, 0, 18, 64, 18, white)
            graphics.DrawLine(canvas, 32, 18, 32, 64, white)
            # Pause for a second
            time.sleep(1)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if not graphics_test.process():
        graphics_test.print_help()
