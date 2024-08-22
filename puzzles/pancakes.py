class PancakesState:

    def __init__(self, state, ancestor=None, gF=0, hF=0, gB=0, hB=0):
        self.order = state
        self.ancestor = ancestor

        self.gF = gF
        self.hF = hF
        self.fF = self.gF + self.hF

        self.gB = gB
        self.hB = hB
        self.fB = self.gB + self.hB

    def is_goal(self):
        return all(self.order[i] <= self.order[i + 1] for i in range(len(self.order) - 1))

    def get_state_as_list(self):
        return self.order

    def set_ancestor(self, ancestor):
        self.ancestor = ancestor

    def flip(self, k):
        return list(self.order[:k][::-1]) + list(self.order[k:])

    def get_neighbors(self):
        neighbors = []
        for k in range(2, len(self.order) + 1):
            flipped = self.flip(k)
            if not self.ancestor or flipped != self.ancestor.order:
                neighbors.append((flipped, 1))
        return neighbors

    def path_to_state(self):
        path = [self.order]
        ancestor = self.ancestor
        while ancestor is not None:
            path.append(ancestor.order)
            ancestor = ancestor.ancestor
        path.reverse()
        return path
