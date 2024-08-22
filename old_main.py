import time
import tracemalloc
import random
import csv
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


# Define three variants of bloom_filter_bidirectional_search with different sizes
def bloom_filter_search_10_4_DFS(start, goal):
    set_bf_size(10 ** 4)
    return bloom_filter_bidirectional_search_DFS(start, goal)


def bloom_filter_search_10_5_DFS(start, goal):
    set_bf_size(10 ** 5)
    return bloom_filter_bidirectional_search_DFS(start, goal)

def bloom_filter_search_10_6_DFS(start, goal):
    set_bf_size(10 ** 6)
    return bloom_filter_bidirectional_search_DFS(start, goal)


def run_experiments(game_state, order_lengths, num_variations):
    set_state(game_state)

    search_functions = {
        "BFS": bfs,
        "IDS": iterative_deepening_dfs,
        "BiBFS": bidirectional_bfs,
        "IDBiHS": IDBiHS,
        "BiBFIDS (10K)": bloom_filter_search_10_4_DFS,
        "BiBFIDS (100K)": bloom_filter_search_10_5_DFS,
        "BiBFIDS (1M)": bloom_filter_search_10_6_DFS,
    }

    results = []

    # Outer loop with progress bar for problem sizes
    for order_length in tqdm(order_lengths, desc="Problem Sizes"):
        all_metrics = {search: {"expansions": [], "percentage": [], "time": [], "memory": []} for search in
                       search_functions.keys()}

        # Inner loop with progress bar for variations
        for _ in tqdm(range(num_variations), desc=f"Variations (P[{order_length}])", leave=False):
            # start_order = random.sample(range(order_length), order_length)
            start = get_state(list(range(order_length)))
            for i in range(10):
                neighbors = [n[0] for n in start.get_neighbors()]
                start = get_state(random.sample(neighbors, 1)[0])
            goal = get_state(sorted(start.order))

            for search_name, search_fn in search_functions.items():
                reset_metrics()
                set_search(search_fn)

                start_time = time.time()
                tracemalloc.start()
                path = start_search(start, goal)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                end_time = time.time()
                time_taken = end_time - start_time

                if path is not None:
                    all_metrics[search_name]["expansions"].append(get_number_expansions())
                    all_metrics[search_name]["percentage"].append(get_percentage())
                    all_metrics[search_name]["time"].append(time_taken)
                    all_metrics[search_name]["memory"].append(peak / 10 ** 6)

        expansions_list = []
        time_avg_list = []
        memory_list = []
        for search_name in all_metrics.keys():
            metrics = all_metrics[search_name]
            expansions_list.append(
                f"{round(sum(metrics['expansions']) / num_variations)} ({round(100 * sum(metrics['percentage']) / num_variations, 1)}%)" if
                metrics['expansions'] and metrics['percentage'] else '0')
            time_avg_list.append(f"{round(sum(metrics['time']) / num_variations, 3)}" if metrics['time'] else "0")
            memory_list.append(f"{round(sum(metrics['memory']) / num_variations, 3)}" if metrics['memory'] else "0")

        # Each metric type gets its own row
        results.append([f"P[{order_length}]", "Mean Expansions"] + expansions_list)
        results.append([f"P[{order_length}]", "Mean Runtime"] + time_avg_list)
        results.append([f"P[{order_length}]", "Mean Memory"] + memory_list)
    return results


def save_results_to_csv(results, filename):
    # header = ["Domain", "Metrics", "BiBFS", "IDBiHS", "BF-BiBFS (10K)", "BF-BiBFS (100K)", "BF-BiBFS (1M)"]
    # header = ["Domain", "Metrics", "BiBFS", "BF-BiBFS (10K)", "BF-BiBFS (100K)", "BF-BiBFS (1M)", "BF-BiBFS_V2 (10K)", "BF-BiBFS_V2 (100K)", "BF-BiBFS_V2 (1M)"]
    header = ["Domain", "Metrics", "BiBFS", "IDBiHS", "BF-BiBFS (10K)", "BF-BiBFS (100K)", "BF-BiBFS (1M)",
              "BF-BiBFS_V2 (10K)", "BF-BiBFS_V2 (100K)", "BF-BiBFS_V2 (1M)", "BF-BiBFS_DFS (10K)",
              "BF-BiBFS_DFS (100K)", "BF-BiBFS_DFS (1M)"]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in results:
            writer.writerow(row)


if __name__ == "__main__":
    problem_sizes = list(range(5, 8))  # , 11, 12, 13, 14, 15,
    num_variations = 100
    results = run_experiments(PancakesState, problem_sizes, num_variations)
    save_results_to_csv(results, "puzzle_search_metrics_pancakes.csv")
