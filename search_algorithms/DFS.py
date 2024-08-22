from utils.metrics import increase_number_nodes, increase_number_expansions, get_state

def dfs(source, goal):
    if str(source.get_state_as_list()) == str(goal.get_state_as_list()):
        return [source.order]

    stack = [source]
    visited = set()
    visited.add(source)
    increase_number_nodes()

    while stack:
        current_state = stack.pop()

        if str(current_state.get_state_as_list()) == str(goal.get_state_as_list()):
            return current_state.path_to_state()

        increase_number_expansions()
        for order, cost in current_state.get_neighbors():
            neighbor = get_state(order, current_state)
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                increase_number_nodes()

    return None
