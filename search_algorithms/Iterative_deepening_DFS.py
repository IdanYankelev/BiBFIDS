from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def iterative_deepening_dfs(source, goal):
    increase_number_nodes()

    depth_limit = 0

    while True:
        result = dfs_limit(source, goal, depth_limit)
        if result:
            return result
        depth_limit += 1


def dfs_limit(source, goal, depth_limit):
    if str(source.get_state_as_list()) == str(goal.get_state_as_list()):
        return [source.order]

    stack = [source]

    while stack:
        state = stack.pop()

        if str(state.get_state_as_list()) == str(goal.get_state_as_list()):
            return state.path_to_state()

        increase_number_expansions()
        for order, cost in state.get_neighbors():
            neighbor = get_state(order, state, gF= state.gF + 1)
            if neighbor.gF <= depth_limit:
                stack.append(neighbor)
                increase_number_nodes()

    return None
