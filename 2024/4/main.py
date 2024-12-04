def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines()]


def dfs(grid, curr_coord):
    res = []
    to_explore = []
    for next_move in [(-1, 0), (-1, -1), (-1, 1),
                      (1, 0), (1, 1), (1, -1),
                      (0, -1), (0, 1)]:
        to_explore.append((([curr_coord], next_move),
                           "XMAS"))
    while to_explore:
        ((candidate, next_move), remaining) = to_explore.pop()
        curr_i, curr_j = candidate[-1]
        next_char = grid[curr_i][curr_j]
        if next_char != remaining[0]:
            continue
        if len(remaining) == 1:
            res.append(candidate)
            continue
        (move_i, move_j) = next_move
        next_i, next_j = curr_i + move_i, curr_j + move_j
        if next_i < 0 or next_i >= len(grid) or next_j < 0 or next_j >= len(grid[0]):
            continue
        to_explore.append(((candidate + [(next_i, next_j)], next_move),
                           remaining[1:]))
    return res


def question_one(game_input):
    res = 0
    for i, curr_i in enumerate(game_input):
        for j, curr_j in enumerate(game_input[i]):
            curr_res = dfs(game_input, (i, j))
            res += len(curr_res)
    return res


def is_xmas(grid, curr_coord):
    curr_i, curr_j = curr_coord
    curr_char = grid[curr_i][curr_j]
    if curr_char != "A":
        return False
    min_i, max_i = curr_i - 1, curr_i + 1
    min_j, max_j = curr_j - 1, curr_j + 1
    if min_i < 0 or max_i >= len(grid) or min_j < 0 or max_j >= len(grid[0]):
        return False
    diag_right_down = grid[curr_i + 1][curr_j + 1]
    diag_right_up = grid[curr_i - 1][curr_j + 1]
    diag_left_down = grid[curr_i + 1][curr_j - 1]
    diag_left_up = grid[curr_i - 1][curr_j - 1]

    def diag_ok(left, right):
        return sorted([left, right]) == ["M", "S"]

    return diag_ok(diag_left_up, diag_right_down) and diag_ok(diag_left_down, diag_right_up)


def question_two(game_input):
    res = 0
    for i, curr_i in enumerate(game_input):
        for j, curr_j in enumerate(game_input[i]):
            if is_xmas(game_input, (i, j)):
                res += 1
    return res



if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))