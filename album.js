const express = require('express');
const axios = require('axios');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
require('dotenv').config();

// Replace with your own Spotify API credentials
const clientId = process.env.CLIENT_ID;
const clientSecret = process.env.CLIENT_SECRET;

// // Spotify API endpoints
const apiBaseUrl = 'https://api.spotify.com/v1';

// Your redirect URI (must be registered in your Spotify Developer Application settings)
const redirectUri = 'http://localhost:8888/callback';

// Scopes determine the level of access your app has
const scopes = ['user-read-currently-playing'];

// Create an Express web server
const app = express();

let currentTrackId = null;

// Function to request a Spotify access token using the Authorization Code flow
async function getAccessToken(code) {
    try {
        const response = await axios.post('https://accounts.spotify.com/api/token', null, {
            params: {
                grant_type: 'authorization_code',
                code,
                redirect_uri: redirectUri,
            },
            auth: {
                username: clientId,
                password: clientSecret,
            },
        });

        return response.data.access_token;
    } catch (error) {
        console.error('Error getting access token:', error.response ? error.response.status : error.message);
        throw error;
    }
}

// Function to initiate the Spotify authorization process
function authorizeSpotify(req, res) {
    const authorizeUrl = `https://accounts.spotify.com/authorize?response_type=code&client_id=${clientId}&scope=${scopes.join('%20')}&redirect_uri=${redirectUri}`;
    res.redirect(authorizeUrl);
}


// Function to download the album cover image, resize it to 18x18 pixels, and extract RGB values
async function downloadAndExtractRGBValues(albumCoverUrl) {
    const imagePath = path.join(__dirname, 'album_cover.jpg'); // Save in the same directory as the script
    const responseImage = await axios.get(albumCoverUrl, { responseType: 'stream' });
    const imageStream = fs.createWriteStream(imagePath);

    responseImage.data.pipe(imageStream);

    imageStream.on('finish', async () => {
        console.log(`Album cover downloaded to ${imagePath}`);

        // Open the image using sharp
        const image = sharp(imagePath);

        // Resize the image to 128x18 pixels
        //Also a commented option for 64x64 pixels but adjust as needed
        const resizedImagePath = path.join(__dirname, 'album_cover_resized.jpg');
        await image.resize(128, 128).toFile(resizedImagePath);
        // await image.resize(64, 64).toFile(resizedImagePath);

        console.log(`Album cover resized to 128x128 pixels and saved to ${resizedImagePath}`);

        // Extract RGB values of each pixel
        const pixelData = await image.raw().toBuffer();

        // Create a text file and write RGB values
        const textFilePath = path.join(__dirname, 'pixel_data.txt');
        const textStream = fs.createWriteStream(textFilePath);

        for (let i = 0; i < pixelData.length; i += 3) {
            const r = pixelData[i];
            const g = pixelData[i + 1];
            const b = pixelData[i + 2];
            textStream.write(`(${r}, ${g}, ${b})\n`);
        }

        textStream.end();

        console.log(`RGB values of each pixel written to ${textFilePath}`);
    });

    imageStream.on('error', (error) => {
        console.error('Error downloading album cover:', error);
    });
}


// Function to periodically check for changes in the currently playing track
async function checkCurrentlyPlaying(accessToken) {
    try {
        const response = await axios.get(`${apiBaseUrl}/me/player/currently-playing`, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });

        const track = response.data.item;

        if (track && track.id !== currentTrackId) {
            currentTrackId = track.id;
            const albumCoverUrl = track.album.images[0].url;
            await downloadAndExtractRGBValues(albumCoverUrl); // Download and resize the album cover
        }
    } catch (error) {
        console.error('Error checking currently playing track:', error.response ? error.response.status : error.message);
    }
}

// Callback route to handle Spotify's redirect after user authorization
app.get('/callback', async (req, res) => {
    const code = req.query.code;

    if (code) {
        try {
            const accessToken = await getAccessToken(code);

            // Start checking for changes in the currently playing track periodically
            setInterval(() => {
                checkCurrentlyPlaying(accessToken);
            }, 500); // Check every 5 seconds

            res.send('Authorization complete. You can close this window.');
        } catch (error) {
            console.error('Error:', error.response ? error.response.status : error.message);
            res.status(500).send('Error during authorization.');
        }
    } else {
        console.error('No authorization code received.');
        res.status(400).send('No authorization code received.');
    }
});

// Route to initiate the Spotify authorization process
app.get('/authorize', authorizeSpotify);

// Start the Express server on the specified port
const port = 8888;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
    console.log('To authorize the app, open this URL in your web browser:');
    console.log(`http://localhost:${port}/authorize`);

    // Open the URL in the default browser using the child_process module
    spawn('cmd', ['/c', 'start', `http://localhost:${port}/authorize`]);
});
