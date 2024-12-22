def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


first_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]


snd_keypad = [[None, "^", "A"], ["<", "v", ">"]]


def keypad_coordinates(keypad):
    res = {}
    for i, l in enumerate(keypad):
        for j, e in enumerate(l):
            if e is not None:
                res[e] = (i, j)
    return res


first_keypad_coordinates = keypad_coordinates(first_keypad)
snd_keypad_coordinates = keypad_coordinates(snd_keypad)

UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def move_symbol(move):
    return {UP: "^", RIGHT: ">", LEFT: "<", DOWN: "v"}[move]


def shortest_path(grid, start, end):
    to_browse = [[(start, None)]]
    min_length = abs(end[0] - start[0]) + abs(end[1] - start[1])
    res = []
    while to_browse:
        curr_path_and_move = to_browse.pop(0)
        seen_coord = [x[0] for x in curr_path_and_move]
        (curr_i, curr_j), _ = curr_path_and_move[-1]
        if (curr_i, curr_j) == end and len(curr_path_and_move) == min_length + 1:
            res.append([move_symbol(x[1]) for x in curr_path_and_move[1:]])
            continue
        for move in [UP, RIGHT, LEFT, DOWN]:
            next_i, next_j = curr_i + move[0], curr_j + move[1]
            if (
                next_i < 0
                or next_i >= len(grid)
                or next_j < 0
                or next_j >= len(grid[0])
            ):
                continue
            next_elm = grid[next_i][next_j]
            if next_elm is None:
                continue
            if (next_i, next_j) in seen_coord:
                continue
            new_path = curr_path_and_move[:]
            new_path.append(((next_i, next_j), move))
            to_browse.append(new_path)
    return res


def compute_shortest_path(grid, mem, start, end):
    if (start, end) in mem:
        return mem[(start, end)]
    computed = shortest_path(grid, start, end)
    mem[(start, end)] = computed
    return computed


def resolve_sequence(sequence, mem, keypad, keypad_coordinates, one_only=False):
    to_browse = [([], keypad_coordinates["A"], sequence)]
    res = []
    while to_browse:
        curr_path, curr_coord, remaining = to_browse.pop()
        if not remaining:
            res.append(curr_path)
            continue
        d, new_remaining = remaining[0], remaining[1:]
        target_coordinate = keypad_coordinates[d]
        targets = compute_shortest_path(keypad, mem, curr_coord, target_coordinate)
        if one_only:
            targets = [targets[0]]
        for target in targets:
            next_path = curr_path[:]
            next_path.extend(target)
            next_path.append("A")
            to_browse.append((next_path, target_coordinate, new_remaining))
    return res


def resolve_first(sequence, mem):
    return resolve_sequence(sequence, mem, first_keypad, first_keypad_coordinates)


def resolve_snd(sequence, mem, one_only=False):
    return resolve_sequence(
        sequence, mem, snd_keypad, snd_keypad_coordinates, one_only=one_only
    )


def question_one(codes):
    mem_first = {}
    mem_snd = {}
    res = []
    for digit in codes:
        first_code = resolve_first(digit, mem_first)
        to_browse = []
        for f in first_code:
            snd_code = resolve_snd(f, mem_snd)
            to_browse.extend(snd_code)
        curr_res = []
        for s in to_browse:
            snd_code = resolve_snd(s, mem_snd, one_only=True)
            curr_res.extend(snd_code)
        shortest = sorted(curr_res, key=lambda x: len(x))[0]
        complexity = int("".join(x for x in digit if x != "A"))
        res.append(len(shortest) * complexity)
    return sum(res)


if __name__ == "__main__":
    codes = read_lines(fname="input.txt")
    print(question_one(codes))
