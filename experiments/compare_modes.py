from core.evolution import run_evolution

SOURCE = "tasks/test_task/source.py"
EVAL   = "tasks/test_task/evaluator.py"

def run_all():
    histories = {}

    # 1. No evolution: just measure seed / single-shot
    h_no, _ = run_evolution(
        SOURCE, EVAL,
        generations=0,         # only seed
        population_size=1,
        mode="no_evo",
    )
    histories["no_evo"] = h_no

    # 2. Random mutation
    h_rand, _ = run_evolution(
        SOURCE, EVAL,
        generations=3,
        population_size=3,
        mode="random",
    )
    histories["random"] = h_rand

    # 3. LLM-guided 
    h_llm, _ = run_evolution(
        SOURCE, EVAL,
        generations=3,
        population_size=3,
        mode="llm",
    )
    histories["llm"] = h_llm

    print("\n=== Summary ===")
    for mode, hist in histories.items():
        print(mode, ":", hist)

    return histories

if __name__ == "__main__":
    run_all()