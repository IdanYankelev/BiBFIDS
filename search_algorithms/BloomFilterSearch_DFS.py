from utils.BloomFilter import BloomFilter
from utils.metrics import increase_number_nodes, increase_number_expansions, get_state


def set_bloom_filter_by_depth(node, max_depth, side):
    stack = [node]
    bf = BloomFilter()

    while stack:
        state = stack.pop()
        state_list_str = str(state.order)  # Cache this result

        if (side == 'F' and state.gF == max_depth) or (side == 'B' and state.gB == max_depth):
            bf.add(state_list_str)
        else:
            increase_number_expansions()
            for order, c in state.get_neighbors():
                if side == 'F':
                    neighbor = get_state(order, state, gF=state.gF + 1)
                else:
                    neighbor = get_state(order, state, gB=state.gB + 1)

                if (side == 'F' and neighbor.gF <= max_depth) or (side == 'B' and neighbor.gB <= max_depth):
                    stack.append(neighbor)
                    increase_number_nodes()

    return bf


def set_bloom_filter_by_candidates(candidates):
    bf = BloomFilter()
    for candidate in candidates:
        bf.add(str(candidate.get_state_as_list()))
    return bf


def get_candidates(bf, node, max_depth, side):
    stack = [node]
    candidates = []
    other_bf = None
    max_length = 100

    while stack:
        state = stack.pop()
        state_list_str = str(state.order)  # Cache this result

        if (side == 'F' and state.gF == max_depth) or (side == 'B' and state.gB == max_depth):
            if bf.check(state_list_str):
                if len(candidates) < max_length:
                    candidates.append(state)
                else:
                    if other_bf is None:
                        other_bf = BloomFilter()
                        for candidate in candidates:
                            other_bf.add(str(candidate.get_state_as_list()))
                    other_bf.add(str(state.get_state_as_list()))
        else:
            increase_number_expansions()
            for order, c in state.get_neighbors():
                if side == 'F':
                    neighbor = get_state(order, state, gF=state.gF + 1)
                else:
                    neighbor = get_state(order, state, gB=state.gB + 1)

                if (side == 'F' and neighbor.gF <= max_depth) or (side == 'B' and neighbor.gB <= max_depth):
                    stack.append(neighbor)
                    increase_number_nodes()

    if other_bf is None:
        return candidates
    else:
        return other_bf


def get_optimized_candidates(start, goal, d1, d2, bf, side):
    if side == 'F':
        while True:
            res = get_candidates(bf, goal, d2, 'B')
            if isinstance(res, BloomFilter):
                other_bf = res
            else:
                return res


            if bf.number_insertions <= other_bf.number_insertions:
                return bf

            res = get_candidates(other_bf, start, d1, 'F')
            if isinstance(res, BloomFilter):
                bf = res
            else:
                return res

            if other_bf.number_insertions <= bf.number_insertions:
                return other_bf
    else:
        while True:
            res = get_candidates(bf, start, d1, 'F')
            if isinstance(res, BloomFilter):
                other_bf = res
            else:
                return res

            if bf.number_insertions <= other_bf.number_insertions:
                return bf

            res = get_candidates(other_bf, goal, d2, 'B')
            if isinstance(res, BloomFilter):
                bf = res
            else:
                return res

            if other_bf.number_insertions <= bf.number_insertions:
                return other_bf


def search(start, goal, d1, d2, side):
    # Get candidates from the other side's bloom filter
    if side == 'F':
        bf = set_bloom_filter_by_depth(goal, d2, 'B')
        res = get_candidates(bf, start, d1, 'F')
    else:
        bf = set_bloom_filter_by_depth(start, d1, 'F')
        res = get_candidates(bf, goal, d2, 'B')

    if isinstance(res, BloomFilter):
        other_bf = res
    else:
        return res

    return get_optimized_candidates(start, goal, d1, d2, other_bf, side)


def limited_dfs_with_candidate(candidate, start, goal, d1, d2, side):
    stack = [candidate]

    while stack:
        state = stack.pop()
        state_list_str = str(state.order)  # Cache this result

        if (side == 'F' and state_list_str == str(goal.order)) or (side == 'B' and state_list_str == str(start.order)):
            return state.path_to_state()
        else:
            increase_number_expansions()
            for order, c in state.get_neighbors():
                if side == 'F':
                    neighbor = get_state(order, state, gF=state.gF + 1)
                else:
                    neighbor = get_state(order, state, gB=state.gB + 1)

                if (side == 'F' and neighbor.gF <= d1 + d2) or (side == 'B' and neighbor.gB <= d1 + d2):
                    stack.append(neighbor)
                    increase_number_nodes()
    return None

def limited_dfs_with_bf(bf, start, goal, d1, d2, side):
    if side == 'F':
        stack = [start]
    else:
        stack = [goal]

    while stack:
        state = stack.pop()
        if (side == 'F' and state.gF == d1) or (side == 'B' and state.gB == d2):
            if bf.check(str(state.order)):
                res = limited_dfs_with_candidate(state, start, goal, d1, d2, side)
                if res:
                    return res

        increase_number_expansions()
        for order, c in state.get_neighbors():
            if side == 'F':
                neighbor = get_state(order, state, gF=state.gF + 1)
            else:
                neighbor = get_state(order, state, gB=state.gB + 1)

            if (side == 'F' and neighbor.gF <= d1) or (side == 'B' and neighbor.gB <= d2):
                stack.append(neighbor)
                increase_number_nodes()
    return None


def get_solution_path(res, start, goal, d1, d2, side):
    if isinstance(res, BloomFilter):
        bf = res
        path = limited_dfs_with_bf(bf, start, goal, d1, d2, side)
        if path:
            return path
    else:
        candidates = res
        for candidate in candidates:
            path = limited_dfs_with_candidate(candidate, start, goal, d1, d2, side)
            if path:
                return path
    return None


def bloom_filter_bidirectional_search_DFS(start, goal):
    increase_number_nodes()
    increase_number_nodes()

    if str(start.get_state_as_list()) == str(goal.get_state_as_list()):
        return [start.order]

    d1 = 0
    d2 = 0
    while True:

        # Increase depth from goal and search start-side candidates
        d2 += 1
        res = search(start, goal, d1, d2, 'F')

        # If any candidates were returned, attempt to connect both sides.
        if res:
            solution_path = get_solution_path(res, start, goal, d1, d2, 'F')
            if solution_path:
                return solution_path

        # Increase depth from start and search goal-side candidates
        d1 += 1
        res = search(start, goal, d1, d2, 'B')

        # If any candidates were returned, attempt to connect both sides.
        if res:
            solution_path = get_solution_path(res, start, goal, d1, d2, 'B')
            if solution_path:
                return solution_path
