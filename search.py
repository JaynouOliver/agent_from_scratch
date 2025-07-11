from exa_py import Exa
from dotenv import load_dotenv
import os

def search(question):
    load_dotenv()
    exa = Exa(api_key=os.getenv("EXA_API_KEY"))

    result = exa.answer(
        question
    )

    return result

search("who is the president of USA")