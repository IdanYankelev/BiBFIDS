import os
import csv
import time
import random
import tracemalloc
from tqdm import tqdm
from puzzles.pancakes import PancakesState
from puzzles.topspin import TopSpinState
from puzzles.slidingtiles import SlidingTileState
from search_algorithms.BFS import bfs
from search_algorithms.Iterative_deepening_DFS import iterative_deepening_dfs
from search_algorithms.Bidirectional_BFS import bidirectional_bfs
from search_algorithms.IDBiHS import IDBiHS
from search_algorithms.BloomFilterSearch_DFS import bloom_filter_bidirectional_search_DFS
from utils.BloomFilter import set_bf_size
from utils.metrics import set_state, get_state, set_search, start_search, get_number_expansions, get_percentage, \
    reset_metrics


# Define bloom filter search variants
def bloom_filter_search_10_4_DFS(start, goal):
    set_bf_size(10 ** 4)
    return bloom_filter_bidirectional_search_DFS(start, goal)


def bloom_filter_search_10_5_DFS(start, goal):
    set_bf_size(10 ** 5)
    return bloom_filter_bidirectional_search_DFS(start, goal)


def bloom_filter_search_10_6_DFS(start, goal):
    set_bf_size(10 ** 6)
    return bloom_filter_bidirectional_search_DFS(start, goal)


# Function to load states from file
def load_states_from_file(filename):
    states = []
    with open(filename, 'r') as file:
        for line in file:
            state_order = list(map(int, line.strip('[]\n').split(',')))
            states.append(state_order)
    return states


# Function to apply search algorithms and calculate mean results
def apply_search_and_save_results(states,output_filename):
    search_functions = {
        "BFS": bfs,
        "IDS": iterative_deepening_dfs,
        "BiBFS": bidirectional_bfs,
        "IDBiHS": IDBiHS,
        "BiBFIDS (10K)": bloom_filter_search_10_4_DFS,
        "BiBFIDS (100K)": bloom_filter_search_10_5_DFS,
        "BiBFIDS (1M)": bloom_filter_search_10_6_DFS,
    }

    # Initialize accumulators for each search function
    accumulators = {name: {"expansions": 0, "percentage": 0, "time": 0, "memory": 0} for name in search_functions}
    total_states = len(states)

    for state_order in tqdm(states, desc="Applying search algorithms"):
        start = get_state(state_order)
        goal = get_state(sorted(state_order))

        for search_name, search_fn in tqdm(search_functions.items()):
            tqdm.write(f"Running {search_name}")
            reset_metrics()
            set_search(search_fn)

            start_time = time.time()
            tracemalloc.start()
            path = start_search(start, goal)
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()
            time_taken = end_time - start_time

            if path is not None:
                expansions = get_number_expansions()
                percentage = get_percentage()
            else:
                expansions = 0
                percentage = 0

            # Accumulate the results
            accumulators[search_name]["expansions"] += expansions
            accumulators[search_name]["percentage"] += percentage
            accumulators[search_name]["time"] += time_taken
            accumulators[search_name]["memory"] += peak_memory / 10 ** 6  # Convert memory to MB

    # Calculate the mean values
    mean_results = {}
    for search_name, metrics in accumulators.items():
        mean_results[search_name] = {
            "mean_expansions": metrics["expansions"] / total_states,
            "mean_percentage": metrics["percentage"] / total_states,
            "mean_time": metrics["time"] / total_states,
            "mean_memory": metrics["memory"] / total_states
        }

    header = ["Search Algorithm", "Mean Expansions", "Mean Percentage", "Mean Time (s)", "Mean Memory (MB)"]

    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for search_name, metrics in mean_results.items():
            writer.writerow([
                search_name,
                round(metrics["mean_expansions"], 2),
                round(metrics["mean_percentage"], 2),
                round(metrics["mean_time"], 3),
                round(metrics["mean_memory"], 3)
            ])


if __name__ == "__main__":
    input_folder = "D:\\courses\\fourth_year\\שיטות חיפוש\\Felner\\exps"  # Folder containing the initial states files
    output_folder = "D:\\courses\\fourth_year\\שיטות חיפוש\\Felner\\results"  # Folder to save the results CSV files
    os.makedirs(output_folder, exist_ok=True)

    game_state_classes = {
        "Pancakes": PancakesState,
        "TopSpin": TopSpinState,
        "SlidingTile": SlidingTileState
    }

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith("_states.txt"):
            filepath = os.path.join(input_folder, filename)

            # Determine game type and order length from the filename
            game_name = filename.split('_')[0]
            order_length = filename.split('[')[1][:2]
            order_length = int(order_length)  # Convert order length to an integer

            game_state_class = game_state_classes[game_name]
            set_state(game_state_class)
            output_filename = os.path.join(output_folder, f"{filename[:-11]}_results.csv")

            states = load_states_from_file(filepath)
            apply_search_and_save_results(states, output_filename)
