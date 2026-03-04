# tasks/pacman/evaluator.py

import importlib.util
import os
import sys

# --- Make env/ act like top-level modules: game, pacman, layout, etc. ---
ENV_DIR = os.path.join(os.path.dirname(__file__), "env")
if ENV_DIR not in sys.path:
    sys.path.insert(0, ENV_DIR)
    
from pacman import run_games
from layout import get_layout
from ghost_agent import RandomGhost
from textDisplay import NullGraphics

def _load_candidate(program_path):
    spec = importlib.util.spec_from_file_location("candidate_agent", program_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_single_game(agent_cls, layout_name="small_classic"):
    curdir = os.getcwd()
    try:
        os.chdir(ENV_DIR)
        layout = get_layout(layout_name)
    finally:
        os.chdir(curdir)

    if layout is None:
        raise ValueError(f"Layout not found: {layout_name}")

   
    display = NullGraphics()
    ghosts = [RandomGhost(i + 1) for i in range(2)]

    # CS188-style API: runGames(layout, pacman, ghosts, display, numGames, record, numTraining, catchExceptions, timeout)
    games = run_games(
        layout=layout,
        pacman=agent_cls(),
        ghosts=ghosts,
        display=display,
        num_games=1,
        record=False,
        num_training=0,
        catch_exceptions=True,
        timeout=30,
    )

    game = games[0]
    state = game.state
    return state.get_score(), state.is_win()

CRASH_PENALTY = -1_000.0

def evaluate(program_path):
    try:
        module = _load_candidate(program_path)
        agent_cls = getattr(module, "EvolvedAgent")

        NUM_GAMES = 3
        total_score = 0.0
        wins = 0

        for _ in range(NUM_GAMES):
            score, is_win = _run_single_game(agent_cls)
            total_score += score
            wins += int(is_win)

        avg_score = total_score / NUM_GAMES
        fitness = avg_score + 200 * wins

        return {"fitness": float(fitness)}

    except Exception as e:
        print("Evaluation error in Pacman task:", e)
        return {"fitness": CRASH_PENALTY}