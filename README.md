# 🎙️ Basic Voice Assistant

Welcome to your new personal desktop helper! This is a friendly, hands-free voice assistant built in Python designed to make your daily computer tasks a breeze. Whether you want to search the web, check the weather, compose an email, or get system updates, you can do it all just by speaking.

---

## 🚀 Quick Start (No Setup Required!)

We have precompiled the assistant into a standalone Windows executable. You can download and run it directly without installing Python or setting up any dependencies:

👉 **[Download VoiceAssistant.exe directly from GitHub](https://github.com/AnujGupta45/Basic-Voice-Assistant/raw/main/release/VoiceAssistant.exe)**

> [!NOTE]
> When running the executable, it will open a Command Prompt window. If you don't have a microphone plugged in, it will automatically switch to **Keyboard Command Mode** so you can type your commands.

---

## 🛠️ For Developers (Running from Source)

If you'd like to customize the assistant or run it directly from the code:

### 1. Install Dependencies
Make sure you have Python 3.8+ installed (verified on Python 3.11). Install the required packages:
```bash
pip install -r requirements.txt
```
*(On Windows, `pyaudio` installs automatically. If you hit any issues, try running `pip install pipwin` followed by `pipwin install pyaudio`.)*

### 2. Configure Settings (Optional)
If you want to use email automation or play music from your local library, configure your environment variables:
1. Make a copy of `.env.example` and rename it to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and fill in:
   - `EMAIL_USER` & `EMAIL_PASS`: For email sending (supports App Passwords for Gmail).
   - `MUSIC_DIR`: The path to your local music folder.

### 3. Run the Assistant
Launch the assistant orchestrator:
```bash
python main.py
```

---

## 🗣️ What Can You Ask It?

The assistant is conversational and listens for natural commands. Here are some of the things you can tell it:

### 🌐 Web & Search
* *"open google"* / *"open youtube"* / *"open github.com"*
* *"search google for Python programming tutorials"*
* *"search wikipedia for Albert Einstein"*

### 🎵 Music & Entertainment
* *"play local music"* (shuffles songs from your configured music folder)
* *"play Shape of You"* (searches and plays on YouTube)
* *"tell a joke"* (gets a laugh from a joke API or local backups)

### 📧 Email Automation
* *"send an email"* (the assistant will guide you step-by-step to input the address, subject, and message)

### 🖥️ OS Automation & System Info
* *"open notepad"* / *"open calculator"* / *"open file explorer"* / *"open command prompt"*
* *"system status"* (reads out CPU load, RAM usage, and battery status)
* *"volume up"* / *"volume down"* / *"mute"* / *"unmute"*

### 🌦️ Daily Updates
* *"what is the time"* / *"what is the date"*
* *"check the weather in London"* (or just *"check the weather"* for your location)
* *"read the news"* (retrieves the top 3 headlines of the day)

### 👋 Leaving
* *"goodbye"* / *"exit"* / *"stop"* / *"go offline"*

---

## 🧠 Smart Features Built-in

* **Keyboard Fallback**: If you don't have a working microphone or the internet connection drops, the assistant won't crash—it will gently switch to Keyboard Mode so you can type commands.
* **Ambient Noise Tuning**: Automatically adjusts microphone sensitivity to filter out background noise before listening.
* **Fully Tested**: Includes a robust suite of unit tests verifying all commands and actions. Run them anytime using:
  ```bash
  python -m unittest test_assistant.py
  ```

Enjoy using your voice assistant! Feel free to customize and expand its vocabulary in `main.py` and `actions.py`.
