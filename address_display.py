#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import qrcode
import numpy as np

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        LOCAL_IP = 'LOCAL_IP'
        PORT = ':8888'
        canvas = self.matrix

        img = qrcode.make('http://' + LOCAL_IP + PORT + '/authorize')
        # Generate a QR code
        qr = qrcode.QRCode(
            version=6,  # Adjust to ensure the QR code is 64x64
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        data = LOCAL_IP + PORT + "/authorize"  # Replace with your desired data
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Resize the image to 64x64 pixels
        img = img.resize((64, 64))

        # Convert image to a numpy array
        img_array = np.array(img)

        # Convert the numpy array to a list of lists with '1' for black and '0' for white
        qr_code_list = [['1' if pixel == 0 else '0' for pixel in row] for row in img_array]

        # The qr_code_list now holds the 64x64 array in memory
        # print(qr_code_list)
        
        while True:
            for i in range(64):
                for j in range(64):
                    pixel_value = qr_code_list[i][j]

                    if pixel_value == '1':
                        r, g, b = 0, 0, 0
                    else:
                        r, g, b = 255, 255, 255

                    self.matrix.SetPixel(j, i, r, g, b)
            time.sleep(1)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
