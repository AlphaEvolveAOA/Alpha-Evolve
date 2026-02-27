from core.evolution import run_evolution

if __name__ == "__main__":
    run_evolution(
        "tasks/test_task/initial_program.py",
        "tasks/test_task/evaluator.py",
        generations=3
    )