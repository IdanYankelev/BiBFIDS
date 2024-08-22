import random
from tqdm import tqdm
import os
from puzzles.pancakes import PancakesState
from puzzles.topspin import TopSpinState
from puzzles.slidingtiles import SlidingTileState

def generate_initial_states(game_state, order_length, change_dist, num_states=100):
    states = []
    for _ in tqdm(range(num_states), desc=f"Generating states for P[{order_length}][{change_dist}]"):
        start = game_state(list(range(order_length)))
        for _ in range(change_dist):
            neighbors = [n[0] for n in start.get_neighbors()]
            start = game_state(random.choice(neighbors))
        states.append(start)
    return states

def save_states_to_file(states, filename):
    folder = "D:\\courses\\fourth_year\\שיטות חיפוש\\Felner\\exps"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        for state in states:
            file.write(f"{state.order}\n")

if __name__ == "__main__":
    problem_sizes = [25,36,49]
    dists = [5,7,10,12,15]  # Set your desired change distance here
    num_states = 100  # Number of initial states to generate for each order length

    for game_state, game_name in [(SlidingTileState, "SlidingTile")]:
        for order_length in problem_sizes:
            for change_dist in dists:
                initial_states = generate_initial_states(game_state, order_length, change_dist, num_states)
                save_states_to_file(initial_states, f"{game_name}_P[{order_length}][{change_dist}]_states.txt")
