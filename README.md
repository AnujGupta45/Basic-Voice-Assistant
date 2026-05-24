# Basic Voice Assistant

A personal desktop voice assistant built in Python that supports voice commands for web searching, playing music, sending emails, looking up information on Wikipedia, and running basic system applications.

## Features

- **Speech Recognition & Text-to-Speech**: Speech-to-text uses the free Google Web Speech API and text-to-speech uses `pyttsx3` (offline, SAPI5 on Windows).
- **Web Browsing & Search**: Hands-free opening of preset websites like Google, YouTube, GitHub, and StackOverflow, or performing general Google searches.
- **Music Playback**: Search and play tracks on YouTube or play random music files from a configured local directory.
- **Wikipedia Integration**: Retrieves a two-sentence summary of any topic directly via the Wikipedia API.
- **Email Automation**: Compose and send emails using SMTP (fully supports SSL/TLS authentication).
- **OS Automation**: Launch tools like Notepad, Calculator, Command Prompt, or File Explorer.
- **Robust Fallback**: Automatically switches to **Keyboard Command Mode** if a microphone is not connected or the speech recognition service is offline.

---

## Technical Stack

- **Language**: Python 3.11+
- **Speech Input**: `SpeechRecognition`, `PyAudio`
- **Speech Output**: `pyttsx3`
- **APIs**: Wikipedia API, SMTP (smtplib)
- **Utilities**: `webbrowser`, `subprocess`, `os`, `python-dotenv`

---

## Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed (this project was built and verified with Python 3.11.1).

### Setup and Installation

1. **Clone or navigate** into the project folder.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On Windows, `pyaudio` installs automatically via wheels. If you run into build errors, verify your compiler tools or try installing `pip install pipwin` then `pipwin install pyaudio`.*

3. **Configure Environment Variables**:
   Copy the example environment file and name it `.env`:
   ```bash
   copy .env.example .env
   ```
   Open the `.env` file and configure:
   - `EMAIL_USER`: Your email address.
   - `EMAIL_PASS`: Your email password (for Gmail, this **must** be an [App Password](https://support.google.com/accounts/answer/185833)).
   - `MUSIC_DIR`: (Optional) Absolute path to a folder on your computer containing music files (e.g. `C:\Users\Username\Music`).

---

## Running the Assistant

Execute the orchestrator:
```bash
python main.py
```

Upon launching, the assistant will greet you (e.g. "Good morning!") and listen for voice commands. If a microphone is not detected, it will display `[System Info] Microphone not detected/accessible` and prompt you to type commands.

### Supported Voice Commands

Here are some examples of what you can say:

| Action / Category | Example Voice Commands |
| :--- | :--- |
| **System Info** | "what is the time" / "what is the date" |
| **Wikipedia** | "search wikipedia for Albert Einstein" / "wikipedia space exploration" |
| **Web Browsing** | "open google" / "open youtube" / "open github.com" / "search google for python tutorials" |
| **Music** | "play shape of you" / "play music" / "play local music" |
| **Email** | "send an email" / "send mail" (follow prompt to provide email, subject, body, and say "yes" to send) |
| **System Utilities** | "open notepad" / "open calculator" / "open command prompt" / "open file explorer" |
| **Identify** | "who are you" / "what can you do" |
| **Termination** | "goodbye" / "exit" / "stop" / "go offline" |

---

## Running Tests

Automated integration tests are provided to verify the routing, wikipedia lookup, email format preparation, and OS commands without invoking actual physical speakers or microphone streams.

Run tests using Python's built-in unittest framework:
```bash
python -m unittest test_assistant.py
```
