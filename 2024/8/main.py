import itertools


def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines()]


def antinode(l, r):
    l_i, l_j = l
    r_i, r_j = r
    delta_i = l_i - r_i
    delta_j = l_j - r_j
    return l_i + delta_i, l_j + delta_j


def inside(point, game_input):
    i, j = point
    return 0 <= i < len(game_input) and 0 <= j < len(game_input[0])


def question_one(game_input):
    res = {}
    antinodes = set()

    for i, l in enumerate(game_input):
        for j, e in enumerate(l):
            if e != ".":
                res.setdefault(e, []).append((i, j))
    for k, v in res.items():
        for left, right in itertools.combinations(v, 2):
            antinode_left = antinode(left, right)
            antinode_right = antinode(right, left)
            if inside(antinode_left, game_input):
                antinodes.add(antinode_left)
            if inside(antinode_right, game_input):
                antinodes.add(antinode_right)
    return len(antinodes)


def question_two(game_input):
    res = {}
    antinodes = set()

    for i, l in enumerate(game_input):
        for j, e in enumerate(l):
            if e != ".":
                res.setdefault(e, []).append((i, j))
    for k, v in res.items():
        for l in v:
            antinodes.add(l)
        for left, right in itertools.combinations(v, 2):
            curr_right, curr_left = left, right
            antinode_left = antinode(curr_left, curr_right)
            while inside(antinode_left, game_input):
                antinodes.add(antinode_left)
                curr_right = curr_left
                curr_left = antinode_left
                antinode_left = antinode(curr_left, curr_right)
            curr_right, curr_left = left, right
            antinode_right = antinode(curr_right, curr_left)
            while inside(antinode_right, game_input):
                antinodes.add(antinode_right)
                curr_left = curr_right
                curr_right = antinode_right
                antinode_right = antinode(curr_right, curr_left)
    return len(antinodes)


if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))
