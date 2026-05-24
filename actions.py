import os
import smtplib
import subprocess
import datetime
import random
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import wikipedia
import config

def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    clean_query = query.replace("wikipedia", "").replace("search", "").replace("for", "").strip()
    if not clean_query:
        return "What would you like me to search Wikipedia for?"
    try:
        # Retrieve short summary
        results = wikipedia.summary(clean_query, sentences=2)
        return f"According to Wikipedia: {results}"
    except wikipedia.exceptions.DisambiguationError as e:
        # Many possibilities
        options = ", ".join(e.options[:3])
        return f"There are multiple topics named {clean_query}. It could refer to: {options}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"Sorry, I could not find any Wikipedia article matching '{clean_query}'."
    except Exception as e:
        return f"An error occurred while reaching Wikipedia: {e}"

def send_email(to_email, subject, body):
    """Sends an email using the SMTP configurations in config.py."""
    if not config.EMAIL_USER or not config.EMAIL_PASS:
        return "Email credentials are not configured. Please set EMAIL_USER and EMAIL_PASS in your .env file."
    
    try:
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and authenticate
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return f"Email sent successfully to {to_email}."
    except Exception as e:
        return f"Failed to send email. Error: {e}"

def open_website(query):
    """Opens a website in the default browser based on keywords."""
    # Check preconfigured sites
    for site, url in config.WEBSITES.items():
        if site in query:
            webbrowser.open(url)
            return f"Opening {site.title()}"
    
    # Generic command extraction
    search_query = query.replace("open website", "").replace("open", "").strip()
    if search_query:
        # Check if it looks like a clean web address
        if "." in search_query and " " not in search_query:
            url = f"https://{search_query}" if not search_query.startswith("http") else search_query
            webbrowser.open(url)
            return f"Opening {search_query}"
        else:
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            return f"Searching Google for '{search_query}'"
    else:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

def play_music(query=""):
    """Plays music from local disk (if configured) or searches YouTube."""
    song_name = query.replace("play music", "").replace("play song", "").replace("play", "").strip()
    
    # Local music playback check
    play_local = "local" in query or not song_name
    if play_local and config.MUSIC_DIR:
        if os.path.exists(config.MUSIC_DIR):
            try:
                songs = [f for f in os.listdir(config.MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.m4a', '.mp4'))]
                if songs:
                    random_song = random.choice(songs)
                    song_path = os.path.join(config.MUSIC_DIR, random_song)
                    os.startfile(song_path)
                    return f"Playing local music: {random_song}"
                else:
                    return f"No audio files found in music directory: {config.MUSIC_DIR}"
            except Exception as e:
                return f"Error trying to play local music: {e}"
        else:
            if "local" in query:
                return f"Local music directory not found: {config.MUSIC_DIR}"

    # YouTube playback
    if song_name:
        url = f"https://www.youtube.com/results?search_query={song_name}"
        webbrowser.open(url)
        return f"Playing '{song_name}' on YouTube"
    else:
        webbrowser.open("https://music.youtube.com")
        return "Opening YouTube Music"

def get_system_time():
    """Returns the current date and time."""
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%B %d, %Y")
    day_str = now.strftime("%A")
    return f"Today is {day_str}, {date_str}. The current time is {time_str}."

def run_os_command(query):
    """Executes basic OS automation tasks on Windows."""
    query = query.lower()
    if "notepad" in query:
        try:
            subprocess.Popen("notepad.exe")
            return "Opening Notepad"
        except Exception as e:
            return f"Failed to open Notepad: {e}"
    elif "calculator" in query or "calc" in query:
        try:
            subprocess.Popen("calc.exe")
            return "Opening Calculator"
        except Exception as e:
            return f"Failed to open Calculator: {e}"
    elif "command prompt" in query or "cmd" in query:
        try:
            subprocess.Popen("cmd.exe")
            return "Opening Command Prompt"
        except Exception as e:
            return f"Failed to open Command Prompt: {e}"
    elif "file explorer" in query or "explorer" in query or "this pc" in query:
        try:
            subprocess.Popen("explorer.exe")
            return "Opening File Explorer"
        except Exception as e:
            return f"Failed to open File Explorer: {e}"
    else:
        return "Application shortcut not recognized."
