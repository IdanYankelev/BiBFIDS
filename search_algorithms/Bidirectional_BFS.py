from collections import deque
from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def bidirectional_bfs(start, goal):
    increase_number_nodes()
    increase_number_nodes()

    if str(start.order) == str(goal.order):
        return [start.order]

    start_queue = deque([start])
    start_visited = {start}

    goal_queue = deque([goal])
    goal_visited = {goal}

    while start_queue and goal_queue:
        # Expand from start side
        result = bfs_level(start_queue, start_visited, goal_visited, 'F')
        if not isinstance(result, deque):
            return construct_path(result, start_visited, goal_visited, 'F')

        start_queue = result

        # Expand from goal side
        result = bfs_level(goal_queue, goal_visited, start_visited, 'B')
        if not isinstance(result, deque):
            return construct_path(result, start_visited, goal_visited, 'B')

        goal_queue = result

    return None


def bfs_level(queue, visited, other_visited, side):
    other_visited_orders = [node.order for node in other_visited]
    visited_orders = [node.order for node in visited]

    next_queue = deque()
    while queue:
        state = queue.popleft()

        # If this state has been visited from the other side, we found a solution.
        if state.order in other_visited_orders:
            return state

        increase_number_expansions()
        for order, cost in state.get_neighbors():
            if side == 'F':
                neighbor = get_state(order, state, gF=state.gF + 1)
                if neighbor.order not in visited_orders:
                    visited.add(neighbor)
                    next_queue.append(neighbor)
                    increase_number_nodes()
            else:
                neighbor = get_state(order, state, gB=state.gB + 1)
                if neighbor.order not in visited_orders:
                    visited.add(neighbor)
                    next_queue.append(neighbor)
                    increase_number_nodes()
    return next_queue


def construct_path(meeting_point, start_visited, goal_visited, side):
    path = []
    if side == 'F':
        state = meeting_point
        while state:
            path.append(state.order)
            state = state.ancestor
        path.reverse()

        state = next(s for s in goal_visited if s.order == meeting_point.order)
        state = state.ancestor
        while state:
            path.append(state.order)
            state = state.ancestor
    else:
        state = meeting_point
        while state:
            path.append(state.order)
            state = state.ancestor
        state = next(s for s in start_visited if s.order == meeting_point.order)
        state = state.ancestor
        while state:
            path.append(state.order)
            state = state.ancestor
        path.reverse()

    return path
