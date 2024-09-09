from yta_multimedia.experimental.text.gemini_ai import GeminiAI

class AIPromptHandler:
    def __init__(self):
        pass

    def generate_youtube_video_title(self, idea: str):
        """
        Generates a Youtube video title from a prompt idea.
        """
        gemini = GeminiAI()

        prompt = 'Quiero crear un vídeo que hable sobre las criptomonedas y su influencia en las elecciones de Venezuela. Necesito que generes un título que sea llamativo para que yo pueda utilizarlo en Youtube para este vídeo. El título debe atraer la atención del público, y debe tener como máximo 60 caracteres.'
        gemini.ask(prompt)