import pyttsx3
import speech_recognition as sr
import config

class VoiceEngine:
    def __init__(self):
        """Initializes the Text-to-Speech engine and Speech Recognizer."""
        try:
            self.tts = pyttsx3.init()
            self.setup_tts()
        except Exception as e:
            print(f"Warning: Failed to initialize pyttsx3 engine: {e}")
            self.tts = None

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 300  # Sensitivity threshold

    def setup_tts(self):
        """Configures rate, volume, and voice gender/index for pyttsx3."""
        if not self.tts:
            return
        try:
            self.tts.setProperty('rate', config.VOICE_RATE)
            self.tts.setProperty('volume', config.VOICE_VOLUME)
            
            voices = self.tts.getProperty('voices')
            if voices:
                index = min(config.VOICE_GENDER_INDEX, len(voices) - 1)
                self.tts.setProperty('voice', voices[index].id)
        except Exception as e:
            print(f"Error configuring TTS engine: {e}")

    def speak(self, text):
        """Converts text to speech and prints to console."""
        print(f"Assistant: {text}")
        if not self.tts:
            return
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"[TTS Playback Error: {e}]")

    def listen(self):
        """Listens to microphone input and converts it to text."""
        try:
            microphone = sr.Microphone()
        except Exception as e:
            print(f"Microphone init error: {e}. Please check your audio recording devices.")
            return "mic_error"

        with microphone as source:
            print("\nListening...")
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = self.recognizer.listen(source, timeout=4, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""
            except Exception as e:
                print(f"Audio capture error: {e}")
                return ""

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            # Unintelligible speech
            return ""
        except sr.RequestError as e:
            print(f"Network request error from speech service: {e}")
            return "request_error"
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
