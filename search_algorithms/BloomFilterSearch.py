from collections import deque
from utils.BloomFilter import BloomFilter
from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def set_bloom_filter_by_depth(node, max_depth, side):
    queue = deque([node])
    bf = BloomFilter()
    visited = {node}

    while queue:
        state = queue.popleft()
        state_list_str = str(state.order)  # Cache this result

        if side == 'F':
            if state.gF == max_depth:
                bf.add(state_list_str)
            else:
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gF=state.gF + 1)
                    if neighbor not in visited and neighbor.gF <= max_depth:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        increase_number_nodes()
        else:
            if state.gB == max_depth:
                bf.add(state_list_str)
            else:
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gB=state.gB + 1)
                    if neighbor not in visited and neighbor.gB <= max_depth:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        increase_number_nodes()

    return bf


def set_bloom_filter_by_candidates(candidates):
    bf = BloomFilter()
    for candidate in candidates:
        bf.add(str(candidate.get_state_as_list()))
    return bf


def get_candidates(bf, node, max_depth, side):
    queue = deque([node])
    candidates = []
    visited = {node}

    while queue:
        state = queue.popleft()
        state_list_str = str(state.order)  # Cache this result

        if side == 'F':
            if state.gF == max_depth:
                if bf.check(state_list_str):
                    candidates.append(state)
            else:
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gF=state.gF + 1)
                    if neighbor not in visited and neighbor.gF <= max_depth:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        increase_number_nodes()
        else:
            if state.gB == max_depth:
                if bf.check(state_list_str):
                    candidates.append(state)
            else:
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gB=state.gB + 1)
                    if neighbor not in visited and neighbor.gB <= max_depth:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        increase_number_nodes()

    return candidates


def get_optimized_candidates_start_side(start, goal, d1, d2, candidates_2):
    candidates_1 = None
    bf1 = None
    while candidates_2:
        bf2 = set_bloom_filter_by_candidates(candidates_2)

        if candidates_1:
            candidates_1.clear()
        candidates_1 = get_candidates(bf2, goal, d1, 'B')

        if not candidates_1:
            return []

        if bf1:
            bf1.clear()
        bf1 = set_bloom_filter_by_candidates(candidates_1)

        candidates_2_new = get_candidates(bf1, start, d2, 'F')

        if len(candidates_2) == len(candidates_2_new):
            return candidates_2
        else:
            candidates_2.clear()
            candidates_2 = candidates_2_new


def get_optimized_candidates_goal_side(start, goal, d1, d2, candidates_1):
    candidates_2 = None
    bf2 = None
    while candidates_1:
        bf1 = set_bloom_filter_by_candidates(candidates_1)

        if candidates_2:
            candidates_2.clear()
        candidates_2 = get_candidates(bf1, start, d2, 'F')

        if not candidates_2:
            return []

        if bf2:
            bf2.clear()
        bf2 = set_bloom_filter_by_candidates(candidates_2)

        candidates_1_new = get_candidates(bf2, goal, d1, 'B')

        if len(candidates_1) == len(candidates_1_new):
            return candidates_1
        else:
            candidates_1.clear()
            candidates_1 = candidates_1_new


def search_start_side(start, goal, d1, d2):
    bf1 = set_bloom_filter_by_depth(goal, d1, 'B')
    candidates_2 = get_candidates(bf1, start, d2, 'F')

    if candidates_2:
        return get_optimized_candidates_start_side(start, goal, d1, d2, candidates_2)
    else:
        return []


def search_goal_side(start, goal, d1, d2):
    bf2 = set_bloom_filter_by_depth(start, d2, 'F')
    candidates_1 = get_candidates(bf2, goal, d1, 'B')

    if candidates_1:
        return get_optimized_candidates_goal_side(start, goal, d1, d2, candidates_1)
    else:
        return []


def limited_dfs(start, goal, max_depth, side):
    visited = set()
    stack = [start]

    while stack:
        state = stack.pop()
        state_list_str = str(state.order)  # Cache this result

        if side == 'F':
            if state.gF == start.gF + max_depth:
                if state_list_str == str(goal.order):
                    return state.path_to_state()
            elif state not in visited:
                visited.add(state)
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gF=state.gF + 1)
                    if neighbor.gF <= start.gF + max_depth:
                        stack.append(neighbor)
                        increase_number_nodes()
        else:
            if state.gB == start.gB + max_depth:
                if state_list_str == str(goal.order):
                    return state.path_to_state()
            elif state not in visited:
                visited.add(state)
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gB=state.gB + 1)
                    if neighbor.gB <= start.gB + max_depth:
                        stack.append(neighbor)
                        increase_number_nodes()
    return None


def get_solution_path_start_side(start_side_candidates, goal, d1):
    for candidate in start_side_candidates:
        path = limited_dfs(candidate, goal, d1, 'F')
        if path:
            return path
    return None


def get_solution_path_goal_side(goal_side_candidates, start, d2):
    for candidate in goal_side_candidates:
        path = limited_dfs(candidate, start, d2, 'B')
        if path:
            path.reverse()
            return path
    return None


def bloom_filter_bidirectional_search(start, goal):
    increase_number_nodes()
    increase_number_nodes()

    if str(start.get_state_as_list()) == str(goal.get_state_as_list()):
        return [start.order]

    d1 = 0
    d2 = 0
    while True:
        d2 += 1

        start_side_candidates = search_start_side(start, goal, d1, d2)
        if start_side_candidates:
            solution_path = get_solution_path_start_side(start_side_candidates, goal, d1)
            if solution_path:
                return solution_path

        start_side_candidates = []
        d1 += 1

        goal_side_candidates = search_goal_side(start, goal, d1, d2)
        if goal_side_candidates:
            solution_path = get_solution_path_goal_side(goal_side_candidates, start, d2)
            if solution_path:
                return solution_path
