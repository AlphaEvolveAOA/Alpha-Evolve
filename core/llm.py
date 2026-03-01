# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import yaml
# import re


# load_dotenv()
# genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

# with open("core/config.yaml", "r") as f:
#     config = yaml.safe_load(f)
    
# model = genai.GenerativeModel(config["llm"]["model"])

# def _strip_code_fences(text: str) -> str:
#     if "```" in text:
#         parts = text.split("```")
#         if len(parts) >= 3:
#             # parts[1] might start with "python\n"
#             code_block = parts[1]
#             # remove "python" language tag if present
#             code_block = re.sub(r"^python\s*", "", code_block.lstrip(), flags=re.IGNORECASE)
#             return code_block
#     return text

# def improve_code(code_text):
#     prompt = f"""
# You are improving a Python program.

# Only modify the code between:
# # EVOLVE-BLOCK-START
# and
# # EVOLVE-BLOCK-END

# Goal: modify the code so that it increases the program's fitness.
# Try to return output that contains the word "AI".

# Here is the full program:

# {code_text}

# Return the full modified program.
# """
    
#     response = model.generate_content(prompt)
#     raw = response.text or ""
#     cleaned = _strip_code_fences(raw)
#     return cleaned

def improve_code(code_text: str) -> str:
    """
    TEMP: simulate LLM mutation locally.
    Operates only inside the EVOLVE block.
    """
    start = code_text.find("# EVOLVE-BLOCK-START")
    end = code_text.find("# EVOLVE-BLOCK-END")
    if start == -1 or end == -1:
        return code_text

    before = code_text[:start]
    after = code_text[end + len("# EVOLVE-BLOCK-END"):]

    new_block = """# EVOLVE-BLOCK-START
    return "Greetings from an AI!"
    # EVOLVE-BLOCK-END
"""
    return before + new_block + after