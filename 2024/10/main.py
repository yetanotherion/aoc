def read_input(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def find_all_nines(grid):
    res = []
    for i, l in enumerate(grid):
        for j, e in enumerate(l):
            if e == "9":
                res.append((i, j))
    return res


UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def dfs(grid, start):
    to_browse = [(start, [])]
    res = []
    while to_browse:
        (curr_i, curr_j), path = to_browse.pop()
        curr_elm = int(grid[curr_i][curr_j])
        for move in [UP, RIGHT, LEFT, DOWN]:
            next_i, next_j = curr_i + move[0], curr_j + move[1]
            if (
                next_i < 0
                or next_i >= len(grid)
                or next_j < 0
                or next_j >= len(grid[0])
            ):
                continue
            if (next_i, next_j) in path:
                continue
            next_elm = int(grid[next_i][next_j])
            if next_elm != curr_elm - 1:
                continue
            if next_elm == 0:
                res.append((next_i, next_j))
                continue
            new_path = path[:]
            new_path.append((curr_i, curr_j))
            to_browse.append(((next_i, next_j), path))
    return res


def question_one(grid):
    all_nines = find_all_nines(grid)
    res = {}
    for nine in all_nines:
        curr_res = dfs(grid, nine)
        for (i, j) in set(curr_res):
            curr = res.setdefault((i, j), 0)
            res[(i, j)] = curr + 1
    return sum(res.values())


def question_two(grid):
    all_nines = find_all_nines(grid)
    res = {}
    for nine in all_nines:
        curr_res = dfs(grid, nine)
        for (i, j) in curr_res:
            curr = res.setdefault((i, j), 0)
            res[(i, j)] = curr + 1
    return sum(res.values())


if __name__ == "__main__":
    grid = read_input(fname="input.txt")
    print(question_one(grid))
    print(question_two(grid))
