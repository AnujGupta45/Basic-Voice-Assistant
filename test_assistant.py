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

if __name__ == '__main__':
    unittest.main()
