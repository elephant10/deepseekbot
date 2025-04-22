from openai import OpenAI
from openai import AsyncOpenAI 
from dotenv import load_dotenv
load_dotenv()
import os

class Deepseek :
    
    base_url = "https://api.deepseek.com"
    def __init__(self, api_key =  None):
        api_key = api_key or os.environ.get("deepseek_key")
        if api_key is None:
            raise ValueError("API key is required")
        self.client = AsyncOpenAI(api_key=api_key, base_url=Deepseek.base_url)

    async def chat(self, message: list, model:str="deepseek-chat"):
        system_prompt = ""
        with open(r"system_prompt.txt", "r") as f:
                    system_prompt = f.read()
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt}] +
                    message,
            stream=False,
            temperature=0.9,
            max_tokens=8192

        )
        return response.choices[0].message

#test
if __name__ == "__main__":
    print(Deepseek().chat("Hello, how are you?"))
