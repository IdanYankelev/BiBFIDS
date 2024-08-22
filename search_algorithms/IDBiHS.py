from puzzles.pancakes import PancakesState
from utils.metrics import set_state, increase_number_nodes, increase_number_expansions, get_state

def updateNextBound(nextT, f, fT):
    if f > fT:
        return min(nextT, f)
    else:
        return nextT

def split(fT):
    return max(int(fT / 2) - 1, 0)

def h(n1, n2):
    return 0

def IDBiHS(s, g, eps=1):
    increase_number_nodes()
    increase_number_nodes()

    # s.hF = h(s, g)
    # s.fF = s.hF
    # g.hB = h(g, s)
    # g.fB = g.hB

    fT = h(s, g)
    nextT = h(s, g)

    while True:
        path = []
        gTF = split(fT)
        res, nextT, path = F_DFS(s, g, fT, gTF, h, nextT, eps, path)
        if res:
            return path
        nextT = nextT + 1
        fT = nextT

def F_DFS(nF, g, fT, gTF, h, nextT, eps, path):
    if nF.fF > fT:
        nextT = updateNextBound(nextT, nF.fF, fT)
        return False, nextT, path

    if nF.gF > gTF:
        gTB = max(fT - nF.gF - eps, 0)
        res, nextT, b_path = B_DFS(nF, g, fT, gTB, h, nextT, eps, path)
        if res:
            return True, nextT, b_path
        return False, nextT, path

    increase_number_expansions()
    for order, c in nF.get_neighbors():
        increase_number_nodes()
        n = get_state(order, nF, gF=nF.gF + 1)
        n.hF = h(n, g)
        n.fF = n.gF + n.hF
        res, nextT, new_path = F_DFS(n, g, fT, gTF, h, nextT, eps, path + [n.order])
        if res:
            return True, nextT, new_path
    return False, nextT, path

def B_DFS(nF, nB, fT, gTB, h, nextT, eps, path):
    if nF.order == nB.order and nF.gF + nB.gB <= fT:
        return True, nextT, path

    if nB.fB > fT or nB.gB > gTB:
        nextT = updateNextBound(nextT, max(nB.fB, nF.gF + nB.gB + eps), fT)
        return False, nextT, path

    increase_number_expansions()
    for order, c in nB.get_neighbors():
        increase_number_nodes()
        n = get_state(order, nB, gB=nB.gB + 1)
        n.hB = h(n, nF)
        n.fB = n.gB + n.hB
        res, nextT, new_path = B_DFS(nF, n, fT, gTB, h, nextT, eps, path + [nB.order])
        if res:
            return True, nextT, new_path
    return False, nextT, path

# if __name__ == "__main__":
#     start_state = [6, 3, 5, 4, 2, 1]
#     goal_state = [1, 2, 3, 4, 5, 6]
#     set_state(PancakesState)
#     start = get_state(start_state)
#     goal = get_state(goal_state)
#     path = IDBiHS(start, goal)
#     if path is not None:
#         for vertex in path:
#             print(vertex)
#     else:
#         print("Unsolvable")


# def h(state, goal_state):
#     def gap_heuristic(s, g):
#         gaps = 0
#         for i in range(len(s) - 1):
#             if abs(s[i] - s[i + 1]) != 1:
#                 gaps += 1
#         if s[0] != 1:
#             gaps += 1
#         return gaps
#
#     # Compute gap heuristic from state to goal_state
#     h1 = gap_heuristic(state.order, goal_state.order)
#
#     # Compute gap heuristic from goal_state to state
#     h2 = gap_heuristic(goal_state.order, state.order)
#
#     # Return the maximum of both heuristic values
#     return max(h1, h2)


