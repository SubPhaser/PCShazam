import soundcard as sc
import numpy as np
from scipy.io import wavfile
import time
from ShazamAPI import Shazam
import pyperclip
import os
import sys
import threading
from datetime import datetime

def countdown(duration):
    for i in range(duration, 0, -1):
        sys.stdout.write(f"\rRecording: {i} seconds left...")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rRecording finished!       \n")
    sys.stdout.flush()

def record_audio(duration, samplerate=44100):
    print(f"Starting to record for {duration} seconds...")
    countdown_thread = threading.Thread(target=countdown, args=(duration,))
    countdown_thread.start()
    
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate) as mic:
        data = mic.record(numframes=samplerate * duration)
    
    countdown_thread.join()
    return data

def save_audio(filename, recording, samplerate=44100):
    normalized_recording = np.int16(recording * 32767)
    wavfile.write(filename, samplerate, normalized_recording)
    print(f"Audio saved as {filename}")

def identify_song(filename):
    print("Identifying song...")
    with open(filename, 'rb') as file:
        audio_bytes = file.read()
    
    shazam = Shazam(audio_bytes)
    recognize_generator = shazam.recognizeSong()
    
    try:
        response = next(recognize_generator)
        if 'track' in response[1]:
            track = response[1]['track']
            title = track.get('title', 'Unknown Title')
            artist = track.get('subtitle', 'Unknown Artist')
            song_info = f"{title} by {artist}"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                'full_info': song_info,
                'timestamp': timestamp
            }
        else:
            print("\033[91mSong not recognized\033[0m")
            return None
    except StopIteration:
        print("\033[91mSong not recognized\033[0m")
        return None

def save_identified_song(song_info, filename="identified_songs.txt"):
    full_info = f"{song_info['timestamp']} - {song_info['full_info']}"
    with open(filename, "a") as file:
        file.write(full_info + "\n")
    print(f"Song information saved to {filename}")

def copy_to_clipboard(text):
    pyperclip.copy(text)
    print(f"Copied to clipboard: {text}")

def main():
    duration = 10  # Recording duration in seconds
    audio_filename = "recorded_audio.wav"
    
    recording = record_audio(duration)
    save_audio(audio_filename, recording[:, 0])  # Save only the first channel
    time.sleep(1)  # Give some time for the file to be saved
    
    song_info = identify_song(audio_filename)
    
    if song_info:
        save_identified_song(song_info)
        print(f"\033[92mSong identified: {song_info['full_info']}\033[0m")
        copy_to_clipboard(song_info['full_info'])
    
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
        print(f"Removed temporary audio file: {audio_filename}")
    else:
        print(f"Temporary audio file not found: {audio_filename}")
    
    print("Script finished.")

if __name__ == "__main__":
    main()