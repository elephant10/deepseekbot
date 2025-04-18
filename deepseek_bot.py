from openai import OpenAI

class Deepseek :
    api_key = None
    base_url = "https://api.deepseek.com"
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, model: str, messages: list, stream: bool = False):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
        return response
    


response = client.chat.completions.create(
    model="deepseek-chat",
    #deepseek-reasoner # Reasoner model
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)