from openai import OpenAI
from dotenv import load_dotenv
import os
class Agent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_msg = "you are a good and helpful assistant"
        self.messages = [{"role": "system", "content": self.system_msg}]

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=self.messages)
        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        return content
    
if __name__ == "__main__":
    agent = Agent()
    response = agent.send_message("What's the recent research papers in RAG in july 2025")
    print(response)
