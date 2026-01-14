from search_node import search_node
from color_blocks_state import color_blocks_state
import heapq


class OpenSet:

    __slots__ = ("_state_to_node", "_heap", "_counter")

    def __init__(self):
        self._state_to_node = {}
        self._heap = []
        self._counter = 0 

    def add(self, node):
        self._state_to_node[node.state] = node
        heapq.heappush(self._heap, (node.f, node.h, self._counter, node))
        self._counter += 1

    def remove(self, node):
        self._state_to_node.pop(node.state, None)

    def __len__(self):
        return len(self._state_to_node)

    def __iter__(self):
        return iter(self._state_to_node.values())

    def best(self):
        while self._heap:
            _, _, _, node = self._heap[0]
            current = self._state_to_node.get(node.state)
            if current is node:
                return node
            # Stale entry: node was removed or replaced -> discard and continue
            heapq.heappop(self._heap)
        raise KeyError("OpenSet is empty")

    def handle_duplicate(self, vn):
        existing = self._state_to_node.get(vn.state)
        if existing is None:
            return False
        if existing.g <= vn.g:
            # Existing is better or equal; keep it, ignore vn
            return True
        # New node has strictly better g: drop old, let caller add vn
        self._state_to_node.pop(vn.state, None)
        return False



def create_open_set():
    return OpenSet()


def create_closed_set():
    return {}


def add_to_open(vn, open_set):
    open_set.add(vn)


def add_to_closed(vn, closed_set):
    closed_set[vn.state] = vn


def open_not_empty(open_set):
    return len(open_set) > 0


def get_best(open_set):
    if isinstance(open_set, OpenSet):
        return open_set.best()
    # Fallback (should not be used in your setup)
    return min(open_set, key=lambda node: node.f)

def duplicate_in_open(vn, open_set):
    if isinstance(open_set, OpenSet):
        return open_set.handle_duplicate(vn)
    for node in open_set:
        if node.state == vn.state:
            if node.g <= vn.g:
                return True
            else:
                open_set.remove(node)
                return False
    return False



def duplicate_in_closed(vn, closed_set):
    existing = closed_set.get(vn.state)
    if existing is None:
        return False
    if existing.g <= vn.g:
        return True
    else:
        closed_set.pop(vn.state, None)
        return False


def print_path(path):
    for i in range(len(path) - 1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")

    print(path[-1].state.get_state_str())


def search(start_state, heuristic):

    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)
        open_set.remove(current)
        if color_blocks_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None
