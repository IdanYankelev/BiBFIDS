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
    other_bf = None
    max_length = 100

    while queue:
        state = queue.popleft()
        state_list_str = str(state.order)  # Cache this result

        if side == 'F':
            if state.gF == max_depth:
                if bf.check(state_list_str):
                    if len(candidates) < max_length:
                        candidates.append(state)
                    else:
                        if other_bf == None:
                            other_bf = BloomFilter()
                            for candidate in candidates:
                                other_bf.add(str(candidate.get_state_as_list()))
                        other_bf.add(str(state.get_state_as_list()))
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
                    if len(candidates) < max_length:
                        candidates.append(state)
                    else:
                        if other_bf == None:
                            other_bf = BloomFilter()
                            for candidate in candidates:
                                other_bf.add(str(candidate.get_state_as_list()))
                        other_bf.add(str(state.get_state_as_list()))
            else:
                increase_number_expansions()
                for order, c in state.get_neighbors():
                    neighbor = get_state(order, state, gB=state.gB + 1)
                    if neighbor not in visited and neighbor.gB <= max_depth:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        increase_number_nodes()

    if other_bf is None:
        return candidates
    else:
        return other_bf


def get_optimized_candidates_start_side(start, goal, d1, d2, bf2):
    while True:
        res = get_candidates(bf2, goal, d1, 'B')
        if isinstance(res, BloomFilter):
            bf1 = res
        else:
            if not res:
                return []

            bf1 = set_bloom_filter_by_candidates(res)

        res = get_candidates(bf1, start, d2, 'F')
        if isinstance(res, BloomFilter):
            bf2 = res
        else:
            if not res:
                return []

            bf2_new = set_bloom_filter_by_candidates(res)
            if bf2.number_insertions == bf2_new.number_insertions:
                return res
            bf2 = bf2_new

def get_optimized_candidates_goal_side(start, goal, d1, d2, bf1):
    while True:
        res = get_candidates(bf1, start, d2, 'F')
        if isinstance(res, BloomFilter):
            bf2 = res
        else:
            if not res:
                return []

            bf2 = set_bloom_filter_by_candidates(res)

        res = get_candidates(bf2, goal, d1, 'B')
        if isinstance(res, BloomFilter):
            bf1 = res
        else:
            if not res:
                return []

            bf1_new = set_bloom_filter_by_candidates(res)
            if bf1.number_insertions == bf1_new.number_insertions:
                return res
            bf1 = bf1_new



def search_start_side(start, goal, d1, d2):
    bf1 = set_bloom_filter_by_depth(goal, d1, 'B')
    res = get_candidates(bf1, start, d2, 'F')
    if isinstance(res, BloomFilter):
        bf2 = res
    else:
        if not res:
            return []
        bf2 = set_bloom_filter_by_candidates(res)

    return get_optimized_candidates_start_side(start, goal, d1, d2, bf2)


def search_goal_side(start, goal, d1, d2):
    bf2 = set_bloom_filter_by_depth(start, d2, 'F')
    res = get_candidates(bf2, goal, d1, 'B')
    if isinstance(res, BloomFilter):
        bf1 = res
    else:
        if not res:
            return []
        bf1 = set_bloom_filter_by_candidates(res)

    return get_optimized_candidates_goal_side(start, goal, d1, d2, bf1)



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


def bloom_filter_bidirectional_search_V2(start, goal):
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

        d1 += 1
        goal_side_candidates = search_goal_side(start, goal, d1, d2)

        if goal_side_candidates:
            solution_path = get_solution_path_goal_side(goal_side_candidates, start, d2)
            if solution_path:
                return solution_path
