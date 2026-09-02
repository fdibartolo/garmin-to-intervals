from google import genai
from google.genai import types
from src.helper import Helper

class GenAI:
    """Google GenAI interface"""
    
    CUSTOM_INSTRUCTIONS = 'prompts/instructions.md'

    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
        with open(self.CUSTOM_INSTRUCTIONS, 'r') as f:
            self.instructions = f.read()

    def generate_content(self, prompt):
        response = self.client.models.generate_content(
            model = self.model,
            config = types.GenerateContentConfig(
                system_instruction = self.instructions,
                response_mime_type = "application/json"
            ),
            contents = prompt
        )
        return Helper.strip_markdown(response.text)