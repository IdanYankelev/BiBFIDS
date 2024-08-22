class SlidingTileState:

    def __init__(self, order, ancestor=None, size=3, gF=0, hF=0, gB=0, hB=0):
        self.order = order
        self.gF = gF
        self.hF = hF
        self.fF = self.gF + self.hF
        self.gB = gB
        self.hB = hB
        self.fB = self.gB + self.hB
        self.ancestor = ancestor
        if self.ancestor:
            self.size = self.ancestor.size
        else:
            self.size = size

    def is_goal(self, goal_state):
        """Check if the current state matches the goal state."""
        return self.order == goal_state

    def get_state_as_list(self):
        """Return the current board configuration as a flattened list."""
        return self.order

    def set_ancestor(self, ancestor):
        """Set the ancestor state."""
        self.ancestor = ancestor

    def swap_blank(self, new_pos):
        """Swap the blank tile with the tile at position new_pos."""
        new_order = self.order[:]
        blank_index = self.order.index(0)
        new_blank_index = new_pos[0] * self.size + new_pos[1]
        new_order[blank_index], new_order[new_blank_index] = new_order[new_blank_index], new_order[blank_index]
        return new_order, new_pos

    def get_neighbors(self):
        """Generate neighboring states by sliding the blank tile."""
        neighbors = []
        blank_pos_y = self.order.index(0) // self.size
        if blank_pos_y == 0:
            # add neighbor of move 0 down
            neighbor_down = self.order[:]
            neighbor_down[self.order.index(0)] = neighbor_down[self.order.index(0) + self.size]
            neighbor_down[self.order.index(0) + self.size] = 0
            neighbors.append((neighbor_down, 1))
        elif blank_pos_y == self.size - 1:
            # add neighbor of move 0 up
            neighbor_up = self.order[:]
            neighbor_up[self.order.index(0)] = neighbor_up[self.order.index(0) - self.size]
            neighbor_up[self.order.index(0) - self.size] = 0
            neighbors.append((neighbor_up, 1))
        else:
            # add neighbor of move 0 down
            neighbor_down = self.order[:]
            neighbor_down[self.order.index(0)] = neighbor_down[self.order.index(0) + self.size]
            neighbor_down[self.order.index(0) + self.size] = 0
            neighbors.append((neighbor_down, 1))

            # add neighbor of move 0 up
            neighbor_up = self.order[:]
            neighbor_up[self.order.index(0)] = neighbor_up[self.order.index(0) - self.size]
            neighbor_up[self.order.index(0) - self.size] = 0
            neighbors.append((neighbor_up, 1))

        blank_pos_x = self.order.index(0) % self.size
        if blank_pos_x == 0:
            # add neighbor of move 0 right
            neighbor_right = self.order[:]
            neighbor_right[self.order.index(0)] = neighbor_right[self.order.index(0) + 1]
            neighbor_right[self.order.index(0) + 1] = 0
            neighbors.append((neighbor_right, 1))
        elif blank_pos_x == self.size - 1:
            # add neighbor of move 0 left
            neighbor_left = self.order[:]
            neighbor_left[self.order.index(0)] = neighbor_left[self.order.index(0) - 1]
            neighbor_left[self.order.index(0) - 1] = 0
            neighbors.append((neighbor_left, 1))
        else:
            # add neighbor of move 0 right
            neighbor_right = self.order[:]
            neighbor_right[self.order.index(0)] = neighbor_right[self.order.index(0) + 1]
            neighbor_right[self.order.index(0) + 1] = 0
            neighbors.append((neighbor_right, 1))

            # add neighbor of move 0 left
            neighbor_left = self.order[:]
            neighbor_left[self.order.index(0)] = neighbor_left[self.order.index(0) - 1]
            neighbor_left[self.order.index(0) - 1] = 0
            neighbors.append((neighbor_left, 1))

        return neighbors

    def path_to_state(self):
        """Return the path from the initial state to the current state."""
        path = [self.order]
        ancestor = self.ancestor
        while ancestor is not None:
            path.append(ancestor.order)
            ancestor = ancestor.ancestor
        path.reverse()
        return path

    def __eq__(self, other):
        """Check if two states are equal."""
        return self.order == other.order

    def __hash__(self):
        """Hash function for using states in sets or as dictionary keys."""
        return hash(tuple(self.order))
