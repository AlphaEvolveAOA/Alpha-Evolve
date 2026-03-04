from core.evolution import run_evolution

if __name__ == "__main__":
    # run_evolution(
    #     "tasks/test_task/source.py",
    #     "tasks/test_task/evaluator.py",
    #     generations=3,
    #     population_size=3,
    #     mode="llm",   # also try: "no_evo", "random"
    # )

    fitness_history, best_file = run_evolution(
        source_path="tasks/pacman/source_pacman_agent.py",
        evaluator_path="tasks/pacman/evaluator.py",
        generations=3,
        population_size=3,
        mode="random",   # later: "llm" / "no_evo"
    )
    print("Pacman fitness history:", fitness_history)
    print("Best Pacman agent file:", best_file)