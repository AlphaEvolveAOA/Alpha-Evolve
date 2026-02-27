import os
import google.generativeai as genai
from dotenv import load_dotenv
import yaml

load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

with open("core/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
model = genai.GenerativeModel(config["llm"]["model"])

def improve_code(code_text):
    prompt = f"""
You are improving a Python program.

Only modify the code between:
# EVOLVE-BLOCK-START
and
# EVOLVE-BLOCK-END

Goal: modify the code so that it increases the program's fitness.
Try to return output that contains the word "AI".

Here is the full program:

{code_text}

Return the full modified program.
"""
    
    response = model.generate_content(prompt)
    return response.text