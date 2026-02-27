import importlib.util
import shutil
from core.llm import improve_code


def run_evolution(program_path, evaluator_path, generations=5):

    best_fitness = -1
    best_code = None

    for gen in range(generations):
        print(f"\n--- Generation {gen} ---")

        with open(program_path, "r") as f:
            code_text = f.read()

        # LLM mutation
        new_code = improve_code(code_text)

        if fitness >= best_fitness: # Gatekeeper
            best_fitness = fitness
            best_code = new_code
            with open(program_path, "w") as f:
                f.write(new_code) # Only update the file if it's an improvement

        # Load evaluator dynamically
        spec = importlib.util.spec_from_file_location("evaluator", evaluator_path)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)

        result = evaluator.evaluate(program_path)
        fitness = result["fitness"]

        print("Fitness:", fitness)

        if fitness > best_fitness:
            best_fitness = fitness
            best_code = new_code

    # Save best
    with open("best_program.py", "w") as f:
        f.write(best_code)

    print("\nBest Fitness Achieved:", best_fitness)