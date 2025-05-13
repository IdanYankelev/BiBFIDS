# BiBFIDS: Memory-Efficient Bidirectional Bloom Filter-Based Search

## 📘 Abstract

**BiBFIDS** is a novel search algorithm that integrates **Bidirectional Search**, **Bloom Filters**, and **Iterative Deepening Search (IDS)** to provide an optimal solution path while drastically reducing memory consumption. This approach is particularly suited for solving complex combinatorial problems like the **Sliding Tile Puzzle**, **Pancake Sorting**, and **TopSpin Puzzle**, especially in memory-restricted environments.

Developed by **Idan Yankelev** and **Yarin Yerushalmi Levi**, BiBFIDS is evaluated against classical and advanced search algorithms such as BFS, IDS, BiBFS, and IDBiHS, demonstrating comparable or superior performance in memory usage and scalability.

## 📄 Paper

You can find a full explanation of the project in the paper:
**[BiBFIDS.pdf](./BiBFIDS.pdf)**

---

## 🧠 Key Concepts

### 🔁 Bidirectional Search
- Starts search from both the start and goal nodes.
- Meets in the middle to reduce search depth and number of expansions.

### 🌱 Bloom Filters
- Probabilistic data structures to test set membership efficiently.
- Reduces memory usage with a small chance of false positives.
- Guarantees no false negatives — a major advantage in search frontier comparison.

### ⬇️ Iterative Deepening Search (IDS)
- Repeated depth-limited DFS.
- Combines space efficiency of DFS with completeness of BFS.

---

## 🧪 Methodology

### Main Algorithm (BiBFIDS)
- Alternates between forward and backward IDS with increasing depth limits.
- Uses Bloom Filters to represent frontier nodes.
- Prunes non-overlapping paths efficiently based on filter matches.
- Optimizes candidate lists with a "ping-pong" filtering mechanism when too many candidates are found.

### Components:
1. `search()`: Performs forward or backward DFS with Bloom filter frontier comparison.
2. `get_candidates()`: Gathers viable nodes at the frontier based on filter matches.
3. `get_optimized_candidates()`: Re-applies filtering from the opposite direction to minimize the candidate set size.

---

## 📊 Evaluation

### Domains
- **Sliding Tile Puzzle**: 3x3, 5x5, 7x7
- **Pancake Sorting**: 5, 7, 9 elements
- **TopSpin Puzzle**: 10, 15, 20 disks

### Metrics
- Number of Node Expansions
- Runtime (Seconds)
- Memory Usage (MB)

### Results Summary
- BiBFIDS (especially 100K variant) showed:
  - 📉 Lower memory usage
  - 🏃 Comparable or better runtimes
  - 🔁 Scalability to large search spaces
- BiBFIDS outperforms IDBiHS on larger instances while using similar or less memory.

---

## 🔧 Installation & Usage

### Requirements
- Python 3.7+
- Optional: NumPy, tqdm, argparse

### Setup
```bash
git clone https://github.com/yourusername/bibfids.git
cd bibfids
pip install -r requirements.txt
```

### Running an Example
```bash
python src/bibfids.py --problem sliding_tile --size 3x3 --variant 100K
```

### Example Options
- `--problem`: sliding_tile | pancake | topspin
- `--size`: 3x3, 5x5, etc.
- `--variant`: 10K | 100K | 1M (Bloom Filter size)

---

## 🔮 Future Work

- Incorporate heuristic estimates (e.g., Manhattan Distance) to make BiBFIDS heuristic-aware.
- Adaptive bloom filter sizing based on problem complexity.
- Use in robotics, path planning, and AI agents in games.

---

## 👨‍💻 Authors

- **Idan Yankelev** – [idanyan@post.bgu.ac.il](mailto:idanyan@post.bgu.ac.il)
- **Yarin Yerushalmi Levi** – [yarinye@post.bgu.ac.il](mailto:yarinye@post.bgu.ac.il)

---

## 📂 Repo Structure

```
├── BiBFIDS.pdf            # Project paper
├── README.md              # Project documentation
├── src/
│   ├── bifbids.py         # Core algorithm
│   └── utils.py           # Helper functions and data structures
└── data/
    └── problems/          # Puzzle definitions
```
