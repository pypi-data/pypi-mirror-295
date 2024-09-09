from yta_general_utils.file_processor import get_project_abspath
from dotenv import load_dotenv

import google.generativeai as genai
import os

# We need to load the .env in the project that is
# being executing the code, not this library
dotenv_path = os.path.join(get_project_abspath(), '.env')
load_dotenv(dotenv_path)

class GeminiAI:
    """
    Class that represents the Google Gemini AI generative model
    to work with it.
    """
    MODEL_NAME = 'gemini-1.5-flash'

    def __init__(self):
        genai.configure(api_key = os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(self.MODEL_NAME)

    def ask(self, prompt: str):
        """
        Asks Gemini AI (gemini-1.5-flash) model by using the provided prompt, waits for the response
        and returns it.
        """
        chat = self.model.start_chat()
        response = chat.send_message(
            prompt,
        )

        return response.text