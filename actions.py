import os
import smtplib
import subprocess
import datetime
import random
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ctypes
import requests
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

def get_weather(query):
    """Fetches weather from wttr.in using requests."""
    city = query.replace("weather", "").replace("temperature", "").replace("temp", "").replace("in", "").replace("for", "").strip()
    try:
        url = f"https://wttr.in/{city}?format=3" if city else "https://wttr.in/?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Could not retrieve weather information at this time (status code {response.status_code})."
    except Exception as e:
        return f"Unable to reach weather service: {e}"

def control_system_volume(command):
    """Controls Windows system volume using ctypes."""
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    
    if "mute" in command:
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
        return "Muting system volume."
    elif "unmute" in command:
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
        return "Toggled mute status."
    elif "up" in command or "increase" in command:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
        return "Increased volume."
    elif "down" in command or "decrease" in command:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
        return "Decreased volume."
    return "Volume command not recognized."

def get_news():
    """Fetches top 3 general news headlines from saurav.tech News API."""
    try:
        url = "https://saurav.tech/NewsAPI/top-headlines/category/general/us.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])[:3]
            if articles:
                headlines = []
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "").split(" - ")[0]
                    headlines.append(f"Headline {i}: {title}")
                return "Here are the top 3 news headlines. " + ". ".join(headlines)
            else:
                return "I couldn't find any news articles."
        else:
            return "I failed to retrieve the news at this time."
    except Exception as e:
        return f"Error reaching the news service: {e}"

def get_joke():
    """Fetches a random joke from the Official Joke API with local backup."""
    local_jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "How does a computer get drunk? It takes screenshots!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "What do you call a programmer from Finland? Nerdic!",
        "Why do programmers wear glasses? Because they can't C-sharp!",
        "Why did the database administrator leave the restaurant? There were too many tables!",
        "Why do Java programmers have to wear glasses? Because they don’t C#."
    ]
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"Here is a joke: {data.get('setup')} ... {data.get('punchline')}"
    except Exception:
        pass
    return f"Here is a joke: {random.choice(local_jokes)}"

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', ctypes.c_byte),
        ('BatteryFlag', ctypes.c_byte),
        ('BatteryLifePercent', ctypes.c_byte),
        ('Reserved1', ctypes.c_byte),
        ('BatteryLifeTime', ctypes.c_ulong),
        ('BatteryFullLifeTime', ctypes.c_ulong),
    ]

def get_system_info():
    """Fetches CPU, RAM, and Battery status natively on Windows."""
    info_parts = []
    
    # 1. CPU Load
    try:
        output = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode().strip()
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            info_parts.append(f"CPU load is at {lines[1]} percent")
    except Exception:
        pass
        
    # 2. RAM Usage
    try:
        output = subprocess.check_output("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize", shell=True).decode().strip()
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 2:
                free = int(parts[0]) / (1024 * 1024)
                total = int(parts[1]) / (1024 * 1024)
                used = total - free
                info_parts.append(f"RAM usage is {used:.1f} GB out of {total:.1f} GB total")
    except Exception:
        pass
        
    # 3. Battery Status
    try:
        status = SYSTEM_POWER_STATUS()
        if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            percent = status.BatteryLifePercent
            charging = "charging" if status.ACLineStatus == 1 else "not charging"
            if percent != 255:
                info_parts.append(f"Battery is at {percent} percent and is {charging}")
    except Exception:
        pass
        
    if info_parts:
        return "System Status: " + ", ".join(info_parts) + "."
    else:
        return "I could not retrieve the system status details."
