import sys
import datetime
from voice_engine import VoiceEngine
import actions

def greet_user(engine):
    """Greets the user based on the current time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    engine.speak(f"{greeting} I am your personal voice assistant. How can I help you today?")

def execute_command(engine, query, text_mode=False):
    """Parses user input commands and routes to correct actions."""
    if not query:
        return True
    
    # 1. Stop / Exit commands
    if any(word in query for word in ["goodbye", "exit", "quit", "stop", "offline", "bye"]):
        engine.speak("Goodbye! Have a nice day.")
        return False
        
    # 2. Time & Date commands
    elif any(word in query for word in ["time", "date", "day"]):
        info = actions.get_system_time()
        engine.speak(info)

    # 3. Wikipedia search commands
    elif "wikipedia" in query:
        engine.speak("Searching Wikipedia...")
        result = actions.search_wikipedia(query)
        engine.speak(result)

    # 4. Email automation commands
    elif "email" in query or "send mail" in query or "send an email" in query:
        engine.speak("Sure, let's draft an email.")
        
        # Recipient email
        engine.speak("Please enter the recipient's email address.")
        recipient = input("Recipient email: ").strip()
            
        if not recipient:
            engine.speak("Email cancelled because no recipient was provided.")
            return True
            
        # Subject
        engine.speak("What is the subject of the email?")
        if text_mode:
            subject = input("Subject: ").strip()
        else:
            subject = engine.listen()
            if subject in ["mic_error", "request_error", ""]:
                subject = input("Subject (type): ").strip()
        
        # Body
        engine.speak("What is the message body?")
        if text_mode:
            body = input("Message: ").strip()
        else:
            body = engine.listen()
            if body in ["mic_error", "request_error", ""]:
                body = input("Message (type): ").strip()

        # Confirmation
        engine.speak(f"Preparing email to {recipient} with subject '{subject}'. Should I send it?")
        if text_mode:
            confirm = input("Confirm send? (yes/no): ").strip().lower()
        else:
            confirm = engine.listen()
            if confirm in ["mic_error", "request_error", ""]:
                confirm = input("Confirm send? (yes/no): ").strip().lower()
                    
        if "yes" in confirm or "y" in confirm:
            engine.speak("Sending the email...")
            response = actions.send_email(recipient, subject, body)
            engine.speak(response)
        else:
            engine.speak("Email cancelled.")

    # 5. Web Browsing commands
    elif "open" in query or "website" in query or "search google" in query:
        response = actions.open_website(query)
        engine.speak(response)

    # 6. Music Playback commands
    elif "play" in query or "music" in query or "song" in query:
        response = actions.play_music(query)
        engine.speak(response)

    # 7. OS applications/automation commands
    elif any(app in query for app in ["notepad", "calculator", "calc", "cmd", "command prompt", "explorer", "file explorer"]):
        response = actions.run_os_command(query)
        engine.speak(response)

    # 8. Help / Information command
    elif "who are you" in query or "what can you do" in query:
        engine.speak("I am your voice assistant. I can search Wikipedia, send emails, open websites, play music, tell you the time, and open programs like Notepad or Calculator.")
    
    # 9. Fallback
    else:
        engine.speak("I didn't quite catch that. Try commands like 'open YouTube', 'search Wikipedia for space', 'what time is it', or 'open Notepad'.")
        
    return True

def main():
    print("=========================================")
    print("       BASIC VOICE ASSISTANT             ")
    print("=========================================")
    
    engine = VoiceEngine()
    text_mode = False
    
    # Detect if microphone is available, otherwise switch to keyboard entry mode
    try:
        import speech_recognition as sr
        # Test building a microphone stream
        with sr.Microphone() as source:
            pass
    except Exception:
        print("[System Info] Microphone not detected/accessible. Running in Keyboard Command Mode.")
        text_mode = True

    greet_user(engine)
    
    running = True
    while running:
        if text_mode:
            try:
                query = input("\nEnter Command (type 'exit' to quit): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                break
        else:
            query = engine.listen()
            if query == "mic_error":
                print("[Warning] Microphone connection issue. Switching to Keyboard Command Mode.")
                text_mode = True
                continue
            elif query == "request_error":
                engine.speak("I had trouble communicating with the speech service. Switching to keyboard mode.")
                text_mode = True
                continue
            elif not query:
                # No voice input detected within timeout, loop again
                continue
        
        running = execute_command(engine, query, text_mode)

if __name__ == "__main__":
    main()
