from itertools import repeat


def init_goal_for_search(goal_blocks: str):

    cleaned = goal_blocks.replace(" ", "")
    color_blocks_state.global_goal_blocks = [int(s) for s in cleaned.split(",")]


class color_blocks_state:
    # you can add global params
    global_goal_blocks = None

    def __init__(self, blocks_str=None, blocks_list=None, **kwargs):
        if blocks_str is not None:

            s = blocks_str.replace(" ", "")

            inner = s[1:-1] 
            parts = inner.split("),(")
            self.blocks_states = [
                tuple(map(int, p.split(","))) for p in parts
            ]
        elif blocks_list is not None:
            self.blocks_states = list(blocks_list)
        else:
            self.blocks_states = []

    def clone(self):
        return color_blocks_state(blocks_list=self.blocks_states)

    @staticmethod
    def is_goal_state(_color_blocks_state):

        goal = color_blocks_state.global_goal_blocks
        blocks = _color_blocks_state.blocks_states
        return all(blocks[i][0] == goal[i] for i in range(len(goal)))

    def flip(self, start_index: int):

        blocks = self.blocks_states
        # prefix unchanged, suffix reversed
        new_blocks = blocks[:start_index] + list(reversed(blocks[start_index:]))
        return color_blocks_state(blocks_list=new_blocks)

    def spin(self, block_index: int):
        
        blocks = self.blocks_states
        a, b = blocks[block_index]
        new_blocks = blocks.copy()
        new_blocks[block_index] = (b, a)
        return color_blocks_state(blocks_list=new_blocks)

    def get_neighbors(self):

        blocks_count = len(self.blocks_states)

        spin_neighbors = [self.spin(i) for i in range(blocks_count)]
        flip_neighbors = [self.flip(i) for i in range(blocks_count - 1)]
        neighbors = spin_neighbors + flip_neighbors

        return zip(neighbors, repeat(1))

    # for debugging states
    def get_state_str(self):
        return ",".join(f"({a} ,{b})" for a, b in self.blocks_states)

    def __hash__(self):
        return hash(self.get_state_str())

    def __eq__(self, other):
        if not isinstance(other, color_blocks_state):
            return NotImplemented

        return all(
            c[0] == o[0] and c[1] == o[1]
            for c, o in zip(self.blocks_states, other.blocks_states)
        )
