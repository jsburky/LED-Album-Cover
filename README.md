# LED Album Cover
## Parts Needed:
- [Adafruit 64x64 display](https://www.adafruit.com/product/5362)
- [Raspberry Pi Bonnet](https://www.adafruit.com/product/3211)
- 5V 4A Power Supply for 64x64 or 5V 15A for 128x128
- Raspberry Pi (zero - 4) Would recommend a 4 for larger display

## Setting Up Spotify and album.js:
- Set up Spotify for developers account and start a new app
- Go to settings
- Take note of the Client ID and Client Secret
- Make the Redirect URL: http://localhost:8888/callback
- Save the settings
- Download the album.js file and move to a folder
- in the same folder as album.js, make a file called .env
- In .env add two lines
  - CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
  - CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
- Make sure node js and npm are installed and working
- Install these dependencies using npm install MODULE_NAME
  - express
  - axios
  - child_process
  - fs
  - path
  - sharp
  - dotenv
- Running the code with node album.js should produce two files:
  - A .jpg of the album cover of the song playing
  - A 128x128 of the album cover of the song playing
- The album cover should update whenever the song changes
