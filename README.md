# LED Album Cover
## Parts Needed:
- [Adafruit 64x64 display](https://www.adafruit.com/product/5362)
- [Raspberry Pi Bonnet](https://www.adafruit.com/product/3211)
- 5V 4A Power Supply for 64x64 or 5V 15A for 128x128
- Raspberry Pi (zero - 4) Would recommend a 4 for better peformance 

## Setting Up Raspberry Pi
- For help with the next steps look [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices)
- First, on the Raspberry Pi Bonnet solder the E pad to the 8 pad it should look like this:
- Next, solder a jumper wire between GPIO 4 and GPIO 18. This will reduce the flicker. It should look like this:
- Next, you want to plug in the power cable and ribbon cable to the led screen like this:
- Then, cut off the other end of the power cable and attach to bonnet like this:
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
- The rest should come installed with python on Raspberry Pi but, if you get an error install it using the same method
- Navigate to the sample folder with cd ~/rpi-rgb-led-matrix/bindings/python/samples
- in this folder create album.py and image_show.py and copy the respective code from this repo
- In album.py edit the variable LOCAL_IP to match the local ip of your Pi
- Then save file with ctrl o and exit with ctrl x
- in the same folder create a file called .env by typing nano .env
- In .env add two lines
  - CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
  - CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
- Then save file with ctrl o and exit with ctrl x

## Running The Program:
- Make sure you are in the samples folder by typing cd ~/rpi-rgb-led-matrix/bindings/python/samples
- Run: sudo python album.py
- On another device, in a browser, visit http://LOCAL_IP:8888/authorize and log in to Spotify.
- Once Spotify is playing, the album cover should be displayed on the matrix
- Please leave comments for errors and improvements.
- Thanks to hzeller for creating the [matrix driver](https://github.com/hzeller/rpi-rgb-led-matrix)

