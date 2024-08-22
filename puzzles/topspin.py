class TopSpinState:

    def __init__(self, order, ancestor=None, gF=0, hF=0, gB=0, hB=0, k=4):
        self.order = order
        self.ancestor = ancestor
        if ancestor:
            self.k = ancestor.k
        else:
            self.k = k
        
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

    def spin(self):
        return list(self.order[:self.k][::-1]) + list(self.order[self.k:])

    def rotate_clockwise(self):
        temp = [self.order[-1]]
        return temp + self.order[:-1]

    def rotate_counterclockwise(self):
        temp = self.order.copy()[1:]
        temp.append(self.order[0])
        return temp

    def get_neighbors(self):
        if not self.ancestor:
            return [(self.spin(), 1), (self.rotate_clockwise(), 1), (self.rotate_counterclockwise(), 1)]
        elif self.ancestor.spin() == self.order:
            return [(self.rotate_clockwise(), 1), (self.rotate_counterclockwise(), 1)]
        elif self.ancestor.rotate_clockwise() == self.order:
            return [(self.spin(), 1), (self.rotate_clockwise(), 1)]
        elif self.ancestor.rotate_counterclockwise() == self.order:
            return [(self.spin(), 1), (self.rotate_counterclockwise(), 1)]


    def path_to_state(self):
        path = [self.order]
        ancestor = self.ancestor
        while ancestor is not None:
            path.append(ancestor.order)
            ancestor = ancestor.ancestor
        path.reverse()
        return path
