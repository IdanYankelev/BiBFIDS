from collections import deque
from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def bfs(source, goal):
    if str(source.order) == str(goal.order):
        return [source.order]

    queue = deque([source])
    visited = set()
    visited.add(str(source.order))
    increase_number_nodes()

    while queue:
        current_state = queue.popleft()

        if str(current_state.order) == str(goal.order):
            return current_state.order

        increase_number_expansions()
        for order, cost in current_state.get_neighbors():
            neighbor = get_state(order, current_state)
            if str(neighbor.order) not in visited:
                visited.add(str(neighbor.order))
                queue.append(neighbor)
                increase_number_nodes()

    return None
