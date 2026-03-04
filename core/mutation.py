import random

def random_mutation(code_text: str) -> str:
    lines = code_text.splitlines()

    # find EVOLVE block
    start = end = None
    for idx, line in enumerate(lines):
        if "# EVOLVE-BLOCK-START" in line:
            start = idx
        if "# EVOLVE-BLOCK-END" in line:
            end = idx
    if start is None or end is None or end - start <= 2:
        return code_text

    body = lines[start + 1:end]
    if len(body) < 3:
        return code_text

    # 🔹 Do NOT move the line that defines 'legal'
    legal_idx = None
    for i, ln in enumerate(body):
        if "legal" in ln and "=" in ln:
            legal_idx = i
            break

    # if we didn't find it, just bail
    if legal_idx is None:
        return code_text

    mutable_indices = [i for i in range(len(body)) if i != legal_idx]
    if len(mutable_indices) < 2:
        return code_text

    i, j = random.sample(mutable_indices, 2)
    body[i], body[j] = body[j], body[i]
    lines[start + 1:end] = body

    mutated = "\n".join(lines)

    # safety: keep only syntactically valid code
    try:
        compile(mutated, "<mutation_test>", "exec")
    except SyntaxError:
        return code_text

    return mutated