def read_input(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def dfs(grid, start):
    to_browse = [start]
    region_element = grid[start[0]][start[1]]
    seen = set()
    fences = set()
    while to_browse:
        curr_i, curr_j = to_browse.pop()
        for move in [UP, RIGHT, LEFT, DOWN]:
            next_i, next_j = curr_i + move[0], curr_j + move[1]
            fence = (move, (next_i, next_j))
            if (
                next_i < 0
                or next_i >= len(grid)
                or next_j < 0
                or next_j >= len(grid[0])
            ):
                if fence not in fences:
                    fences.add(fence)
                continue
            if (next_i, next_j) in seen:
                continue
            next_element = grid[next_i][next_j]
            if next_element != region_element:
                if fence not in fences:
                    fences.add(fence)
                continue
            to_browse.append((next_i, next_j))
        seen.add((curr_i, curr_j))
    return seen, fences


def question_one(grid):
    seen = set()
    price = 0
    for i, l in enumerate(grid):
        for j, e in enumerate(l):
            if (i, j) in seen:
                continue
            curr_seen, fences = dfs(grid, (i, j))
            area, perimeter = len(curr_seen), len(fences)
            price += area * perimeter
            seen = seen.union(curr_seen)
    return price


def side_moves(curr_dir):
    if curr_dir in (UP, DOWN):
        return (LEFT, RIGHT)
    return (UP, DOWN)


def follow_fence_side(fence, fences):
    seen = set()
    to_browse = [fence]
    while to_browse:
        curr_dir, curr_fence = to_browse.pop()
        for curr_move in side_moves(curr_dir):
            next_i, next_j = curr_fence[0] + curr_move[0], curr_fence[1] + curr_move[1]
            next_fence = (curr_dir, (next_i, next_j))
            if next_fence in seen:
                continue
            if next_fence in fences:
                to_browse.append(next_fence)
        seen.add((curr_dir, curr_fence))
    return seen


def nb_sides(fences):
    curr = 0
    seen = set()
    remaining = list(fences)
    while remaining:
        next_fence = remaining.pop()
        if next_fence in seen:
            continue
        new_seen = follow_fence_side(next_fence, fences)
        seen = seen.union(new_seen)
        curr += 1
    return curr


def question_two(grid):
    seen = set()
    price = 0
    for i, l in enumerate(grid):
        for j, e in enumerate(l):
            if (i, j) in seen:
                continue
            curr_seen, fences = dfs(grid, (i, j))
            area, perimeter = len(curr_seen), nb_sides(fences)
            price += area * perimeter
            seen = seen.union(curr_seen)
    return price


if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))
