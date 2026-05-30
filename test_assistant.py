import unittest
from unittest.mock import patch, MagicMock
import actions
import main

class TestVoiceAssistant(unittest.TestCase):
    @patch('wikipedia.summary')
    def test_search_wikipedia_success(self, mock_summary):
        mock_summary.return_value = "Python is a high-level programming language."
        response = actions.search_wikipedia("search wikipedia for Python")
        self.assertIn("Python is a high-level programming language", response)
        mock_summary.assert_called_once_with("Python", sentences=2)

    @patch('wikipedia.summary')
    def test_search_wikipedia_page_error(self, mock_summary):
        import wikipedia
        mock_summary.side_effect = wikipedia.exceptions.PageError("Page not found")
        response = actions.search_wikipedia("wikipedia unknown_topic_123")
        self.assertIn("could not find any Wikipedia article", response)

    @patch('smtplib.SMTP')
    @patch('config.EMAIL_USER', 'test@gmail.com')
    @patch('config.EMAIL_PASS', 'password123')
    def test_send_email_success(self, mock_smtp_class):
        mock_smtp = MagicMock()
        mock_smtp_class.return_value = mock_smtp
        
        response = actions.send_email("receiver@example.com", "Test Subject", "Test Body")
        
        self.assertIn("sent successfully", response)
        mock_smtp_class.assert_called_once_with("smtp.gmail.com", 587)
        mock_smtp.starttls.assert_called_once()
        mock_smtp.login.assert_called_once_with("test@gmail.com", "password123")
        mock_smtp.send_message.assert_called_once()

    def test_get_system_time(self):
        response = actions.get_system_time()
        self.assertIn("Today is", response)
        self.assertIn("The current time is", response)

    @patch('webbrowser.open')
    def test_open_website_preset(self, mock_web_open):
        response = actions.open_website("open google")
        self.assertEqual(response, "Opening Google")
        mock_web_open.assert_called_once_with("https://www.google.com")

    @patch('webbrowser.open')
    def test_open_website_custom_url(self, mock_web_open):
        response = actions.open_website("open example.com")
        self.assertEqual(response, "Opening example.com")
        mock_web_open.assert_called_once_with("https://example.com")

    @patch('webbrowser.open')
    def test_play_music_youtube(self, mock_web_open):
        response = actions.play_music("play shape of you")
        self.assertIn("shape of you", response)
        self.assertIn("YouTube", response)
        mock_web_open.assert_called_once_with("https://www.youtube.com/results?search_query=shape of you")

    @patch('subprocess.Popen')
    def test_run_os_command_notepad(self, mock_popen):
        response = actions.run_os_command("open notepad")
        self.assertEqual(response, "Opening Notepad")
        mock_popen.assert_called_once_with("notepad.exe")

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Paris: ⛅️ +15°C"
        mock_get.return_value = mock_response
        
        response = actions.get_weather("weather in Paris")
        self.assertEqual(response, "Paris: ⛅️ +15°C")
        mock_get.assert_called_once_with("https://wttr.in/Paris?format=3", timeout=5)

    @patch('requests.get')
    def test_get_weather_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = actions.get_weather("weather")
        self.assertIn("Could not retrieve weather", response)

    @patch('ctypes.windll.user32.keybd_event')
    def test_control_system_volume_up(self, mock_keybd):
        response = actions.control_system_volume("volume up")
        self.assertEqual(response, "Increased volume.")
        self.assertEqual(mock_keybd.call_count, 10) # 5 key presses * 2 (down and up)

    @patch('ctypes.windll.user32.keybd_event')
    def test_control_system_volume_mute(self, mock_keybd):
        response = actions.control_system_volume("mute")
        self.assertEqual(response, "Muting system volume.")
        self.assertEqual(mock_keybd.call_count, 2)

    @patch('requests.get')
    def test_get_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "articles": [
                {"title": "First Headline - Source 1"},
                {"title": "Second Headline - Source 2"},
                {"title": "Third Headline - Source 3"}
            ]
        }
        mock_get.return_value = mock_response
        
        response = actions.get_news()
        self.assertIn("First Headline", response)
        self.assertIn("Second Headline", response)
        self.assertIn("Third Headline", response)

    @patch('requests.get')
    def test_get_joke_online(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "setup": "Why did the chicken cross the road?",
            "punchline": "To get to the other side!"
        }
        mock_get.return_value = mock_response
        
        response = actions.get_joke()
        self.assertIn("Why did the chicken cross the road?", response)
        self.assertIn("To get to the other side!", response)

    @patch('requests.get')
    def test_get_joke_offline_fallback(self, mock_get):
        mock_get.side_effect = Exception("Connection lost")
        
        response = actions.get_joke()
        self.assertIn("Here is a joke", response) # verifying it returns a joke from the local list

    @patch('subprocess.check_output')
    @patch('ctypes.windll.kernel32.GetSystemPowerStatus')
    def test_get_system_info(self, mock_power, mock_check_output):
        # Mock CPU load percentage
        mock_check_output.side_effect = [
            b"LoadPercentage  \n 45 \n",
            b"FreePhysicalMemory  TotalVisibleMemorySize \n 8388608  16777216 \n" # 8GB free out of 16GB total
        ]
        
        # Mock Battery status structure
        def mock_get_power(ref):
            ref._obj.ACLineStatus = 1
            ref._obj.BatteryLifePercent = 85
            return 1
            
        mock_power.side_effect = mock_get_power
        
        response = actions.get_system_info()
        self.assertIn("CPU load is at 45 percent", response)
        self.assertIn("RAM usage is 8.0 GB out of 16.0 GB total", response)
        self.assertIn("Battery is at 85 percent and is charging", response)

if __name__ == '__main__':
    unittest.main()
