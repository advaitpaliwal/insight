import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class GenerativeAI:
    def __init__(self):
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    def generate_content(self, prompt, files=[]):
        print("prompt", prompt)
        print("files", files)
        if files:
            response = self.model.generate_content([prompt] + files)
        else:
            response = self.model.generate_content(prompt)

        return response.text


if __name__ == "__main__":
    generative_ai = GenerativeAI()
    prompt = "The opposite of hot is"
    output = generative_ai.generate_content(prompt)
    print(output)
