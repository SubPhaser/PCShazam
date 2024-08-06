# PC Sound Identifier

This simple Python app identifies songs playing on your PC, similar to Shazam.

## What it does

- Records the audio playing on your PC
- Identifies the song using Shazam's database
- Saves the song info to a file and copies it to your clipboard

## Setup

1. Make sure you have Python installed on your PC.
2. Download this project.
3. Open a command prompt in the project folder.
4. Run this command to install required packages:
   ```
   pip install -r requirements.txt
   ```

## How to use

1. Play a song on your PC (from any source - YouTube, Spotify, etc.)
2. Double-click the `run_shazam.bat` file
3. Wait for 10 seconds while it records
4. The app will try to identify the song and show you the result

## Notes

- Make sure your PC's sound isn't muted
- The app might not identify every song, but you can try running it again
- No mic needed.

