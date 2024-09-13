import os 
from groq import Groq

os.environ['GROQ_API_KEY'] = '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'

class BaseAssistant:
    """
    BaseAssistant serves as a base class for various assistant functionalities, such as code reviewing, documentation generation, and more.

    Attributes:
        model (str): The model name used for generating completions.
        temperature (float): Sampling temperature for generating responses.
        max_tokens (int): Maximum number of tokens for generating responses.
        top_p (float): Controls diversity via nucleus sampling.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=1000, top_p=1):
        """
        Initializes the BaseAssistant class with model, temperature, max_tokens, and top_p attributes.

        Args:
            model (str): The model name for generating responses.
            temperature (float): The sampling temperature.
            max_tokens (int): The maximum number of tokens.
            top_p (float): The nucleus sampling value.
        """
        self.client = Groq()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def _get_completion(self, prompt):
        """
        Internal method to generate a completion response based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating a completion.

        Returns:
            str: The generated completion response.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            stream=True,
            stop=None,
        )

        response = ''
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response.strip()