# tasks/pacman/source_pacman_agent.py   (or your actual path)

import random
from game import Agent
from pacman import Directions

class EvolvedAgent(Agent):
    def get_action(self, state):
        # EVOLVE-BLOCK-START
        #  IMPORTANT: use the right method name for legal actions:
        #   - If your GameState has get_legal_actions(index) → use that
        #   - If it has getLegalActions(index) → use that instead
        legal = state.get_legal_actions(0)  # or state.getLegalActions(0)
        non_stop = [a for a in legal if a != Directions.STOP]
        if non_stop:
            return random.choice(non_stop)
        return random.choice(legal)
        # EVOLVE-BLOCK-END