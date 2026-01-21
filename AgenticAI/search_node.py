class search_node:

    def __init__(self, state, g=0, h=0, prev=None):
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.prev = prev

    def __lt__(self, other):
        # Same logic as:
        # (self.f < other.f) or (self.f == other.f and self.h < other.h)
        # but lets Python do tuple-lexicographic comparison.
        return (self.f, self.h) < (other.f, other.h)

    def get_neighbors(self):
        # Delegates to the state object
        return self.state.get_neighbors()

    def __str__(self):
        return f"State: {self.state.get_state_str()}, g: {self.g}, h: {self.h}, f: {self.f}"

    def __eq__(self, other):
        if not isinstance(other, search_node):
            return NotImplemented
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)
