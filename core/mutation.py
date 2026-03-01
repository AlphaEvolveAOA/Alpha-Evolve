import random

def random_mutation(code_text: str) -> str:
    lines = code_text.splitlines()
    if len(lines) < 3:
        return code_text
    i, j = random.sample(range(1, len(lines)-1), 2)
    lines[i], lines[j] = lines[j], lines[i]
    return "\n".join(lines)