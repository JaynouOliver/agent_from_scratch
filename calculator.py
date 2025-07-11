import os
from dotenv import load_dotenv

def calc(question):
    """
    Solves mathematical and scientific problems using natural language input.
    Args:
        question (str): Natural language question/problem to solve
    Returns:
        str: Solution to the problem in natural language
    """
    load_dotenv()
    os.environ["WOLFRAM_ALPHA_APPID"] = os.getenv("WOLFRAM_ALPHA_APPID")

    from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
    wolfram = WolframAlphaAPIWrapper()
    
    try:
        result = wolfram.run(question)
        return result
    except Exception as e:
        return f"Error solving the problem: {str(e)}"

# if __name__ == "__main__":
#     # Test the calculator function
#     result = calc("solve x^4 - 5x^3 + 6x^2 + 4x - 8 = 0")
#     print(result)