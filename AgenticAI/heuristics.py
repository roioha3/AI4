from color_blocks_state import color_blocks_state

global_goal_blocks = []
global_goal_blocks_set = set()
global_goal_adjacent_pairs = set()


def init_goal_for_heuristics(goal_blocks):

    global global_goal_blocks, global_goal_blocks_set, global_goal_adjacent_pairs

    global_goal_blocks = [int(s) for s in goal_blocks.split(",")]
    global_goal_blocks_set = set(global_goal_blocks)

    adjacent_pairs = set()
    for i in range(len(global_goal_blocks) - 1):
        a = global_goal_blocks[i]
        b = global_goal_blocks[i + 1]
        adjacent_pairs.add((a, b))
        adjacent_pairs.add((b, a))

    global_goal_adjacent_pairs = adjacent_pairs


def is_match(block1, block2, goal_blocks=None):

    # Early-exit as soon as we find a matching pair
    gpairs = global_goal_adjacent_pairs
    for color1 in block1:
        for color2 in block2:
            if (color1, color2) in gpairs:
                return 0
    return 1


def base_heuristic(_color_blocks_state):

    blocks = _color_blocks_state.blocks_states

    # zip(blocks, blocks[1:]) iterates over (blocks[i], blocks[i+1])
    return sum(
        is_match(b1, b2)
        for b1, b2 in zip(blocks, blocks[1:])
    )


def advanced_heuristic(_color_blocks_state):

    h_base = base_heuristic(_color_blocks_state)
    blocks = _color_blocks_state.blocks_states
    goal_set = global_goal_blocks_set

    for block in blocks:
        if block[0] not in goal_set:
            h_base += 1  # Penalty for blocks with colors not in the goal

    return h_base
