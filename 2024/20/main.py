def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def find(game_input, target="S"):
    for i, l in enumerate(game_input):
        for j, e in enumerate(l):
            if e == target:
                return (i, j)


def shortest_path(grid):
    start_i, start_j = find(grid, target="S")
    to_browse = [[(start_i, start_j)]]
    seen = set()
    while to_browse:
        curr_path = to_browse.pop(0)
        curr_i, curr_j = curr_path[-1]
        if grid[curr_i][curr_j] == "E":
            return curr_path
        if (curr_i, curr_j) in seen:
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
            if next_elm == "#":
                continue
            new_path = curr_path[:]
            new_path.append((next_i, next_j))
            to_browse.append(new_path)
        seen.add((curr_i, curr_j))


def distance(left, right):
    l_i, l_j = left
    r_i, r_j = right
    return abs(l_i - r_i) + abs(l_j - r_j)


def find_cheats(grid, cheat_distance=2, threshold=100):
    shortest = shortest_path(grid)
    path_distance = {k: (i, len(shortest) - i) for i, k in enumerate(shortest)}
    cheats = set()
    for p, (done, remaining) in path_distance.items():
        close_enough = [x for x in path_distance if distance(p, x) <= cheat_distance]
        for next_i, next_j in close_enough:
            if (next_i, next_j) in path_distance:
                new_distance = (
                    done
                    + distance(p, (next_i, next_j))
                    + path_distance[(next_i, next_j)][1]
                )
                diff = len(shortest) - new_distance
                if diff >= threshold:
                    cheats.add((p, (next_i, next_j), diff))
    return len(cheats)


def question_one(grid):
    return find_cheats(grid, cheat_distance=2, threshold=100)


def question_two(grid):
    return find_cheats(grid, cheat_distance=20, threshold=100)


if __name__ == "__main__":
    grid = read_lines(fname="input.txt")
    print(question_one(grid))
    print(question_two(grid))
