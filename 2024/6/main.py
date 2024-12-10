import copy


def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines()]


def find_starting_point(grid):
    for i, line in enumerate(grid):
        for j, elt in enumerate(line):
            if elt == "^":
                return (i, j)


UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def rotate(curr_dir):
    if curr_dir == UP:
        return RIGHT
    if curr_dir == RIGHT:
        return DOWN
    if curr_dir == DOWN:
        return LEFT
    if curr_dir == LEFT:
        return UP


def browse_all(grid):
    curr_i, curr_j = find_starting_point(grid)
    curr_dir = UP
    visited = set([((curr_i, curr_j), UP)])
    while True:
        next_i, next_j = curr_i + curr_dir[0], curr_j + curr_dir[1]
        if next_i < 0 or next_i >= len(grid) or next_j < 0 or next_j >= len(grid[0]):
            return visited
        next_elt = grid[next_i][next_j]
        if next_elt == "#":
            curr_dir = rotate(curr_dir)
            continue
        curr_i, curr_j = next_i, next_j
        visited.add(((curr_i, curr_j), curr_dir))


def question_one(grid):
    visited = browse_all(grid)
    return len(set(x[0] for x in visited))


def browse_until_cycle(grid, start, visited, fake):
    ((curr_i, curr_j), curr_dir) = start
    new_visited = copy.deepcopy(visited)
    new_visited.add(start)
    while True:
        next_i, next_j = curr_i + curr_dir[0], curr_j + curr_dir[1]
        if next_i < 0 or next_i >= len(grid) or next_j < 0 or next_j >= len(grid[0]):
            return False
        next_elt = grid[next_i][next_j]
        if next_elt == "#" or (next_i, next_j) == fake:
            curr_dir = rotate(curr_dir)
            continue
        curr_i, curr_j = next_i, next_j
        if ((curr_i, curr_j), curr_dir) in new_visited:
            return True
        new_visited.add(((curr_i, curr_j), curr_dir))


def question_two(grid):
    curr_i, curr_j = find_starting_point(grid)
    curr_dir = UP
    visited = set(((curr_i, curr_j), UP))
    obstacles = set()
    seen = set((curr_i, curr_j))
    while True:
        next_i, next_j = curr_i + curr_dir[0], curr_j + curr_dir[1]
        if next_i < 0 or next_i >= len(grid) or next_j < 0 or next_j >= len(grid[0]):
            return len(obstacles)
        next_elt = grid[next_i][next_j]
        if next_elt == "#":
            curr_dir = rotate(curr_dir)
            continue
        if (next_i, next_j) not in seen and browse_until_cycle(
            grid, ((curr_i, curr_j), rotate(curr_dir)), visited, (next_i, next_j)
        ):
            obstacles.add((next_i, next_j))
        curr_i, curr_j = next_i, next_j
        seen.add((curr_i, curr_j))
        visited.add(((curr_i, curr_j), curr_dir))


if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))
