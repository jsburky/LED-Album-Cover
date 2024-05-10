#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        LOCAL_IP = '192.168.1.###'
        PORT = ':8888'
        WIFI = 'WIFI'
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        WIDTH = 5
        HEIGHT = 8

        white = graphics.Color(255, 255, 255)
        while True:
            canvas.Clear()
            graphics.DrawText(canvas, font, 2, 10, white, "WiFi: ")
            graphics.DrawText(canvas, font, 2, 10 + HEIGHT, white, WIFI)
            graphics.DrawText(canvas, font, 2, 10 + HEIGHT * 2, white, "Address:")
            # graphics.DrawText(canvas, font, 2, 10 + HEIGHT * 3, white, "http://")
            graphics.DrawText(canvas, font, 2, 10 + HEIGHT * 4, white, LOCAL_IP)
            graphics.DrawText(canvas, font, 2, 10 + HEIGHT * 5, white, PORT)
            graphics.DrawText(canvas, font, 2, 10 + HEIGHT * 6, white, "/authorize")

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
