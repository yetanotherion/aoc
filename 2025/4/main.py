def read_input(fname):
    with open(fname, "r") as f:
        return [list(l[:-1]) for l in f.readlines() if l[:-1]]


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)

moves = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def adjacent(i, j, lines):
    res = []
    for (di, dj) in moves:
        ni = i + di
        nj = j + dj
        if not (0 <= ni < len(lines) and 0 <= nj < len(lines[0])):
            continue
        res.append((ni, nj))
    return res


def can_be_removed(i, j, lines):
    num_adjacent = 0
    if lines[i][j] != "@":
        return False
    for ni, nj in adjacent(i, j, lines):
        elmt = lines[ni][nj]
        if elmt == "@":
            num_adjacent += 1
    return num_adjacent < 4


def question_one(fname):
    lines = read_input(fname)
    ok_pos = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if can_be_removed(i, j, lines):
                ok_pos += 1
    return ok_pos


def question_two(fname):
    lines = read_input(fname)
    ok_pos = 0
    to_browse = []
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "@":
                to_browse.append((i, j))
    while to_browse:
        (i, j) = to_browse.pop(0)
        if can_be_removed(i, j, lines):
            lines[i][j] = "0"
            ok_pos += 1
            for ni, nj in adjacent(i, j, lines):
                if lines[ni][nj] == "@":
                    to_browse.append((ni, nj))
    return ok_pos


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
