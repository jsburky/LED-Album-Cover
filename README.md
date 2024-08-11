# LED Album Cover
## Parts Needed:
- [Adafruit 64x64 display](https://www.adafruit.com/product/5362)
- [Raspberry Pi Bonnet](https://www.adafruit.com/product/3211)
- 5V 4A Power Supply for 64x64 or 5V 15A for 128x128
- Raspberry Pi (zero - 4) Would recommend a 4 for better peformance 
- A computer with ssh capability. This can be done by connecting a monitor to the Pi but, it is easier with ssh because you can copy over code from this repository
## Setting Up Raspberry Pi
- For help with the next steps look [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices)
- First, on the Raspberry Pi Bonnet solder the E pad to the 8 pad it should look like this:

  
![Raspberry Pi Bonnet E Pad to 8 Pad Short](/images/E8_Short.jpg)


- Next, solder a jumper wire between GPIO 4 and GPIO 18. This will reduce the flicker. It should look like this:

  
![Raspberry Pi Bonnet GPIO 4 to GPIO 18 Short](/images/GPIO_Short.jpg)


- Next, you want to plug in the power cable and ribbon cable (make sure its the "in" connection" to the led screen like this:


![Matrix Panel Wiring](/images/Panel_Wires.jpg)


- Then, cut off the other end of the power cable and attach to bonnet like this:

  
![Raspberry Pi Bonnet 5V Out](/images/5V_Out.jpg)


- Connect ribbon cable to bonnet.
- Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash Raspberry Pi OS Lite (64/32 bit depending on which Pi is being used) to an SD Card. I would recommend going through the settings to set up a hostname, wifi, username and password, and enable ssh
- Insert SD Card in Pi
- Plug in the bonnet using the power supply. You can power the raspberry pi seperate or through the bonnet depending on current supply.
- Once turned on, if set up properly, you can ssh from another computer using hostname@LOCAL_IP then entering the password. Or, you can attach a monitor and keyboard to setup
  - LOCAL_IP usally takes the form of 192.168.1.### and can be found on your routers desktop settings as a connected device

## Setting up LED Matrix Library
- Once at the pi's command line enter:
  - curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
  - then: sudo bash rgb-matrix.sh
- This will bring you to a setup menu for the library. The settings you want are:
  - Continue?: y
  - Adafruit RGB Matrix Bonnet: 1
  - Quality: 1
- Confirm Settings and answer yes to reboot after installation
- navigate to config.txt file with sudo nano /boot/firmware/config.txt
- Set dtparam=audio=off and save file with ctrl o then exit with ctrl x
- navigate to blacklist.conf with sudo nano /etc/modprobe.d/blacklist.conf
- Add line: blacklist snd_bcm2835 then save file with ctrl o and exit with ctrl x
- Lastly navigate to cmdline.txt with sudo nano /boot/firmware/cmdline.txt
- At the end of the line of text, add isolcpus=3 then save file with ctrl o and exit with ctrl x
- Reboot Pi with sudo reboot

## Setting Up Spotify Account:
- Set up Spotify for developers account and start a new app
- Give the app a name and description
- Make the Redirect URL: http://LOCAL_IP:8888/callback
  - You will want LOCAL_IP to be the address you used to ssh into the pi
- Go to settings
- Take note of the Client ID and Client Secret
- Save the settings

## Setting Up Python Code:
- Install these dependencies using sudo apt install python3-MODULE_NAME
  - flask
  - requests
  - psutil
  - dotenv
  - qrcode
  - numpy
- The rest should come installed with python on Raspberry Pi but, if you get an error install it using the same method
- Navigate to the sample folder with cd ~/rpi-rgb-led-matrix/bindings/python/samples
- in this folder create album.py, image_show.py, and address_display.py and copy the respective code from this repo
- In album.py edit the variable LOCAL_IP to match the local ip of your Pi
- In address_display.py update the LOCAL_IP to the ip 
  - This step is really optional but it shows a qr code to connect to the display
- Then save file with ctrl o and exit with ctrl x
- in the same folder create a file called .env by typing nano .env
- In .env add two lines
  - CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
  - CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
- Then save file with ctrl o and exit with ctrl x

## Running from boot with keyboard input 
- This allows for the code the be run without a monitor or ssh
- Install evdev using sudo apt install python3-evdev
- In the same directory as the rest of the scripts, create main.py by typing nano main.py
- Copy the code from the file on gitub
- Change the event# to the event of the keyboard you plugged in. For me, this was event 0
  - Use ls /dev/input/ to find the curent events
  - Run ls /dev/input/ before and after plugging in the keyboard to see which events get added
- After changing the code, run sudo main.py and press 1 to run the album.py file.
- 0 terminates the code that is running
- Type: sudo nano /etc/systemd/system/program_launcher.service
  - Copy over the contents of the file: program_launcher.service
  - Then save file with ctrl o and exit with ctrl x
- Go to the home directory with cd ~
- Type sudo nano shutdown_services.sh
  - Copy over the contents of the file: shutdown_services.sh
  - Then save file with ctrl o and exit with ctrl x
- run: sudo systemctl daemon-reload
- run: sudo systemctl start program_launcher.service
- run: sudo systemctl enable program_launcher.service
- run: sudo reboot
## Running The Program (With ssh or a monitor):
- Make sure you are in the samples folder by typing cd ~/rpi-rgb-led-matrix/bindings/python/samples
- Run: sudo python album.py
- On another device, in a browser, visit http://LOCAL_IP:8888/authorize and log in to Spotify.
- Once Spotify is playing, the album cover should be displayed on the matrix
- Please leave comments for errors and improvements.
- Thanks to hzeller for creating the [matrix driver](https://github.com/hzeller/rpi-rgb-led-matrix)

