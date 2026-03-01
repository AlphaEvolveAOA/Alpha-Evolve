# core/evolution.py
import importlib.util
import os
from core.llm import improve_code
from core.mutation import random_mutation

os.makedirs("generated", exist_ok=True)


def _load_evaluator(evaluator_path: str):
    spec = importlib.util.spec_from_file_location("evaluator", evaluator_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _evaluate(evaluator_module, candidate_path: str) -> float:
    result = evaluator_module.evaluate(candidate_path)
    return result["fitness"]


def run_evolution(
    source_path: str,
    evaluator_path: str,
    generations: int = 5,
    population_size: int = 3,
    mode: str = "llm",
):
    """
    mode:
      - "no_evo"  : single-shot (baseline)
      - "random"  : random mutation
      - "llm"     : LLM-guided mutation (currently stubbed locally)
    """
    # read base code once
    with open(source_path, "r") as f:
        base_code = f.read()

    evaluator_module = _load_evaluator(evaluator_path)

    best_fitness = -1
    best_file = None
    fitness_history = []

    # ---- Generation 0: evaluate base code (no mutation) ----
    base_candidate = "generated/gen_0_seed.py"
    with open(base_candidate, "w") as f:
        f.write(base_code)

    seed_fitness = _evaluate(evaluator_module, base_candidate)
    print(f"\n--- Generation 0 (seed) ---")
    print(f"  fitness={seed_fitness}")
    best_fitness = seed_fitness
    best_file = base_candidate
    fitness_history.append(seed_fitness)
    current_best_code = base_code

    # ---- Subsequent generations ----
    for gen in range(1, generations + 1):
        print(f"\n--- Generation {gen} ({mode}) ---")
        candidates = []

        for i in range(population_size):
            if mode == "no_evo":
                # always keep seed code: no evolution
                code = base_code
            elif mode == "random":
                code = random_mutation(current_best_code)
            elif mode == "llm":
                code = improve_code(current_best_code)
            else:
                code = current_best_code

            path = f"generated/gen_{gen}_{i}.py"
            with open(path, "w") as f:
                f.write(code)

            fitness = _evaluate(evaluator_module, path)
            print(f"  cand {i}: fitness={fitness}")
            candidates.append((fitness, path, code))

        # best in this generation
        gen_best = max(candidates, key=lambda x: x[0])
        fitness_history.append(gen_best[0])

        if gen_best[0] > best_fitness:
            best_fitness, best_file = gen_best[0], gen_best[1]

        # for random/llm, next gen starts from best code of this gen
        current_best_code = gen_best[2]

    print("\nBest Fitness:", best_fitness)
    print("Best File:", best_file)
    print("Fitness history:", fitness_history)
    return fitness_history, best_file