from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

class Deepseek :
    
    base_url = "https://api.deepseek.com"
    def __init__(self, api_key =  None):
        api_key = api_key or os.environ.get("deepseek_key")
        if api_key is None:
            raise ValueError("API key is required")
        self.client = OpenAI(api_key=api_key, base_url=Deepseek.base_url)

    def chat(self, message: str, model:str="deepseek-chat"):
        system_prompt = ""
        with open(r"system_prompt.txt", "r") as f:
                    system_prompt = f.read()
                    
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": 
                   system_prompt
               },
                {"role": "user", "content": message},
            ],
            stream=False,
            temperature=2
        )
        return response.choices[0].message

#test
if __name__ == "__main__":
    print(Deepseek().chat("Hello, how are you?"))
