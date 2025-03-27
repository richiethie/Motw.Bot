import os
import time
from instagrapi import Client
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
SESSION_FILE = "session.json"  # File to store the login session

cl = Client()

def login():
    # If session file exists, load it
    if os.path.exists(SESSION_FILE):
        print("Loading session from file...")
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()  # Test if session is still valid
            print("Session loaded successfully!")
            return
        except Exception:
            print("Session expired. Logging in again...")

    # If session is not valid, log in and save session
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
    print("Logged in and session saved.")

# Example function to fetch memes
def fetch_memes():
    inbox = cl.direct_threads()  # Get the threads
    print(f"Total threads: {len(inbox)}")  # Print total number of threads for debugging
    for thread in inbox:
        print(f"Thread Title: {thread.thread_title}")  # Print thread title or other identifier
        for msg in thread.messages:
            # Instead of checking for msg.media, check for msg.clip
            if hasattr(msg, "clip") and msg.clip:
                clip = msg.clip  # This is your Media object
                # Check if clip has a video_url attribute
                if hasattr(clip, 'video_url'):
                    print(f"Found a video meme: {clip.video_url}")
                else:
                    print("Clip found but no video_url attribute")

# Login and then fetch memes
login()
fetch_memes()
