def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_lines(raw_input):
    res = []
    for l in raw_input:
        x, y = tuple(int(x) for x in l.split(","))
        res.append((x, y))
    return res


UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)


def question_one(game_input, grid_size=(70, 70)):
    start_x, start_y = (0, 0)
    end_x, end_y = (grid_size[1], grid_size[0])
    to_browse = [(start_x, start_y, 0)]
    obstacles = set(game_input)
    seen = set()
    res = 0
    while to_browse:
        curr_x, curr_y, curr_dist = to_browse.pop(0)
        curr = (curr_x, curr_y)
        if curr == (end_x, end_y):
            res = curr_dist
            break
        if curr in seen:
            continue
        for move in [UP, RIGHT, LEFT, DOWN]:
            next_x, next_y = curr_x + move[0], curr_y + move[1]
            if (
                next_x < 0
                or next_x > grid_size[1]
                or next_y < 0
                or next_y > grid_size[0]
            ):
                continue
            if (next_x, next_y) in obstacles:
                continue
            to_browse.append((next_x, next_y, curr_dist + 1))
        seen.add(curr)

    return res


def question_two(game_input, grid_size=(70, 70)):
    num_obstacles = len(game_input)
    for i in range(num_obstacles):
        shortest = question_one(game_input[: i + 1], grid_size=grid_size)
        if shortest == 0:
            return game_input[i]


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    game_input = parse_lines(raw_input)
    print(question_one(game_input[:1024], grid_size=(70, 70)))
    print(question_two(game_input, grid_size=(70, 70)))
