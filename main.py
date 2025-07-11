from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from calculator import calc
from search import search

class Agent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_msg = open("system_prompt.txt", "r").read()
        self.messages = [{"role": "system", "content": self.system_msg}]

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=self.messages)
        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        return content

def extract_action(text):
    action_match = re.search(r"Action:\s*(.+)", text)
    input_match = re.search(r"Action Input:\s*(.+)", text)
    
    action = action_match.group(1).strip() if action_match else None
    action_input = input_match.group(1).strip() if input_match else None
    
    # Remove quotes from action input if present
    if action_input and action_input.startswith('"') and action_input.endswith('"'):
        action_input = action_input[1:-1]
    
    # Debug prints
    print(f"DEBUG - Extracted action: '{action}'")
    print(f"DEBUG - Extracted action_input: '{action_input}'")
    
    return (action, action_input)

def extract_answer(text):
    answer_match = re.search(r"Answer: (.+)", text)
    return answer_match.group(1) if answer_match else None

def run_agent(query):
    agent = Agent()
    tools = {"search": search, "calc": calc}
    
    current_input = query
    
    for turn in range(10):
        response = agent.send_message(current_input)
        print(f"Turn {turn + 1}:")
        print(response)
        print("-" * 50)
        
        # Check for STOP signal
        if "STOP" in response:
            answer = extract_answer(response)
            if answer:
                print(f"Final Answer: {answer}")
                return answer
            break
        
        action, action_input = extract_action(response)
        
        if action and action in tools:
            result = tools[action](action_input)
            current_input = str(result)
            continue
            
        answer = extract_answer(response)
        if answer:
            print(f"Final Answer: {answer}")
            return answer
    
    print("Max turns reached")
    return None

if __name__ == "__main__":
    print("AI Agent with Search and Calculator")
    print("Enter your question:")
    
    user_query = input("> ")
    run_agent(user_query)