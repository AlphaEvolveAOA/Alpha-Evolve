from core.evolution import run_evolution

if __name__ == "__main__":
    run_evolution(
        "tasks/test_task/source.py",
        "tasks/test_task/evaluator.py",
        generations=3,
        population_size=3,
        mode="llm",   # also try: "no_evo", "random"
    )