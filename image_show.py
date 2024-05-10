#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        file_path = "pixel_data.txt"
        rgb_values = []
        with open(file_path, 'r') as file:
            for line in file:
                # Remove parentheses and split by comma
                rgb = line.strip()[1:-1].split(',')
                # Convert strings to integers
                rgb = [int(x.strip()) for x in rgb]
                rgb_values.append(rgb)

        # Display the matrix on the LED matrix
        while True:
            for i in range(64):
                for j in range(64):
                    index = i * 64 + j
                    r, g, b = rgb_values[index]
                    self.matrix.SetPixel(j, i, r, g, b)  # Set RGB values from rgb_values
            time.sleep(1)  # Adjust this value to change display speed

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
