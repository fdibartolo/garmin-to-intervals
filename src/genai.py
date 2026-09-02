from google import genai
from google.genai import types
from src.constants import RESET, GREY, ITALIC_FONT, NORMAL_FONT
from src.helper import Helper

class GenAI:
    """Google GenAI interface"""
    
    CUSTOM_INSTRUCTIONS = 'prompts/instructions.md'
    PROMPT_CONTEXT = """
        you are an expert software developer who specializes in building JSON objects for the Garmin Training API.
        use the provided system_instructions to complement your knowledge and understand the Garmin Training API schema, field names, etc.
        you are instructed to build a JSON object for the Garmin Training API based on the following workout steps:
        {prompt}
        you MUST respond ONLY with valid JSON that complies with the Garmin Training API schema definition, no explanation
    """

    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
        with open(self.CUSTOM_INSTRUCTIONS, 'r') as f:
            self.instructions = f.read()

    def generate_content(self, prompt):
        content = self.__build_prompt(prompt)
        print(f"{GREY}{ITALIC_FONT}{content}{RESET}{NORMAL_FONT}")
        response = self.client.models.generate_content(
            model = self.model,
            config = types.GenerateContentConfig(
                system_instruction = self.instructions,
                response_mime_type = "application/json"
            ),
            contents = content
        )
        return Helper.strip_markdown(response.text)
    
    def __build_prompt(self, prompt):
        return self.PROMPT_CONTEXT.replace("{prompt}", prompt)