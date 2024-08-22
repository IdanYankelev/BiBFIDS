from collections import deque
from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def iterative_deepening_bfs(source, goal):
    depth_limit = 0

    while True:
        result = bfs_limit(source, goal, depth_limit)
        if result:
            return result
        depth_limit += 1


def bfs_limit(source, goal, depth_limit):
    if str(source.get_state_as_list()) == str(goal.get_state_as_list()):
        return [source.order]

    queue = deque([(source, 0)])
    visited = set()
    visited.add(source)
    increase_number_nodes()

    while queue:
        current_state, current_depth = queue.popleft()

        if current_depth > depth_limit:
            continue

        if str(current_state.get_state_as_list()) == str(goal.get_state_as_list()):
            return current_state.path_to_state()

        increase_number_expansions()
        for order, cost in current_state.get_neighbors():
            neighbor = get_state(order, current_state)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, current_depth + 1))
                increase_number_nodes()

    return None
