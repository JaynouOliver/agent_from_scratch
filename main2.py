from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import logging
from calculator import calc
from search import search

# ANSI Color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

# Configure logging without timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    
    return (action, action_input)

def extract_answer(text):
    answer_match = re.search(r"Answer: (.+)", text)
    return answer_match.group(1) if answer_match else None

def run_agent(query):
    agent = Agent()
    tools = {"search": search, "calc": calc}
    
    print(f"{Colors.CYAN}INFO{Colors.RESET} - Starting agent session with query: {Colors.WHITE}{query}{Colors.RESET}")
    current_input = query
    
    for turn in range(10):
        print(f"{Colors.CYAN}INFO{Colors.RESET} - Turn {turn + 1}: Agent reasoning...")
        
        response = agent.send_message(current_input)
        
        # Show only the key parts of agent thinking
        lines = response.split('\n')
        thinking_lines = [line for line in lines if line.strip() and not line.startswith('Action')]
        if thinking_lines:
            print(f"{Colors.BLUE}Agent:{Colors.RESET} {thinking_lines[0]}")
        
        # Check for completion
        if "STOP" in response:
            answer = extract_answer(response)
            if answer:
                print(f"{Colors.CYAN}INFO{Colors.RESET} - Agent completed task successfully")
                print(f"\n{Colors.GREEN}{Colors.BOLD}Final Answer:{Colors.RESET} {answer}")
                return answer
            break
        
        # Extract and execute actions
        action, action_input = extract_action(response)
        
        if action and action in tools:
            print(f"{Colors.CYAN}INFO{Colors.RESET} - Executing {action} tool")
            print(f"{Colors.YELLOW}Using {action}:{Colors.RESET} {action_input[:50]}{'...' if len(action_input) > 50 else ''}")
            
            try:
                result = tools[action](action_input)
                print(f"{Colors.CYAN}INFO{Colors.RESET} - {action} tool executed successfully")
                print(f"{Colors.GREEN}{action.capitalize()} completed{Colors.RESET}")
                current_input = f"Observation: {result}"
            except Exception as e:
                print(f"{Colors.RED}ERROR{Colors.RESET} - {action} tool failed: {str(e)}")
                print(f"{Colors.RED}{action.capitalize()} failed: {str(e)}{Colors.RESET}")
                current_input = f"Observation: Error executing {action}: {str(e)}"
            continue
            
        elif action:
            print(f"{Colors.YELLOW}WARNING{Colors.RESET} - Unknown action requested: {action}")
            current_input = f"Observation: Unknown action '{action}'. Available actions: search, calc"
            continue
            
        # Check for final answer
        answer = extract_answer(response)
        if answer:
            print(f"{Colors.CYAN}INFO{Colors.RESET} - Agent provided final answer")
            print(f"\n{Colors.GREEN}{Colors.BOLD}Final Answer:{Colors.RESET} {answer}")
            return answer
        
        # Request clarification if needed
        print(f"{Colors.YELLOW}WARNING{Colors.RESET} - Agent response unclear, requesting clarification")
        current_input = "Please provide either an Action: search/calc or Answer: with your final response."
    
    print(f"{Colors.RED}ERROR{Colors.RESET} - Maximum turns reached without completion")
    print(f"{Colors.RED}Agent reached maximum turns without completing the task{Colors.RESET}")
    return None

if __name__ == "__main__":
    print(f"{Colors.PURPLE}{Colors.BOLD}AI Agent with Search and Calculator{Colors.RESET}")
    print("Enter your question:")
    
    user_query = input(f"{Colors.WHITE}> {Colors.RESET}")
    result = run_agent(user_query)