def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(raw_lines):
    game = []
    moves = []
    for l in raw_lines:
        if not l:
            continue
        first = l[0]
        if first in ("#", "O", ".", "@"):
            game.append(l)
        else:
            moves.extend(l)
    return game, moves


def find_start(zone):
    for i, l in enumerate(zone):
        for j, e in enumerate(l):
            if e == "@":
                return (i, j)


UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def question_one(game_input):
    zone, moves = game_input
    curr_zone = [list(l) for l in zone]
    curr = find_start(curr_zone)
    move_coordinates = {">": RIGHT, "<": LEFT, "^": UP, "v": DOWN}
    for move in moves:
        curr_i, curr_j = curr
        coordinates = move_coordinates[move]
        next_i, next_j = curr[0] + coordinates[0], curr[1] + coordinates[1]
        next_elm = curr_zone[next_i][next_j]
        if next_elm == "#":
            continue
        if next_elm == ".":
            curr_zone[next_i][next_j] = "@"
            curr_zone[curr_i][curr_j] = "."
            curr = next_i, next_j
            continue
        start_next_i, start_next_j = next_i, next_j
        while next_elm == "O":
            next_i, next_j = next_i + coordinates[0], next_j + coordinates[1]
            next_elm = curr_zone[next_i][next_j]
        if next_elm == "#":
            continue
        curr_zone[next_i][next_j] = "O"
        curr_zone[start_next_i][start_next_j] = "@"
        curr_zone[curr_i][curr_j] = "."
        curr = start_next_i, start_next_j
    res = 0
    for i, l in enumerate(curr_zone):
        for j, e in enumerate(l):
            if e == "O":
                res += i * 100 + j
    return res


def resize(zone):
    res = []
    for l in zone:
        curr = []
        for e in l:
            if e == "#":
                curr.append("#")
                curr.append("#")
            if e == "O":
                curr.append("[")
                curr.append("]")
            if e == ".":
                curr.append(".")
                curr.append(".")
            if e == "@":
                curr.append("@")
                curr.append(".")
        res.append(curr)
    return res


def question_two(game_input):
    zone, moves = game_input
    new_zone = resize(zone)

    curr_zone = [list(l) for l in new_zone]
    curr = find_start(curr_zone)
    move_coordinates = {">": RIGHT, "<": LEFT, "^": UP, "v": DOWN}
    for i, move in enumerate(moves):
        curr_i, curr_j = curr
        coordinates = move_coordinates[move]
        next_i, next_j = curr[0] + coordinates[0], curr[1] + coordinates[1]
        next_elm = curr_zone[next_i][next_j]
        if next_elm == "#":
            continue
        if next_elm == ".":
            curr_zone[next_i][next_j] = "@"
            curr_zone[curr_i][curr_j] = "."
            curr = next_i, next_j
            continue

        start_next_i, start_next_j = next_i, next_j
        if coordinates in (RIGHT, LEFT):
            expected_next = "["
            if coordinates == LEFT:
                expected_next = "]"
            while next_elm == expected_next:
                next_i, next_j = next_i, next_j + 2 * coordinates[1]
                next_elm = curr_zone[next_i][next_j]
            if next_elm == "#":
                continue
            while next_elm != "@":
                curr_zone[next_i][next_j] = curr_zone[next_i][next_j - coordinates[1]]
                next_j = next_j - coordinates[1]
                next_elm = curr_zone[next_i][next_j]
            curr_zone[start_next_i][start_next_j] = "@"
            curr_zone[curr_i][curr_j] = "."
            curr = start_next_i, start_next_j
        else:
            if next_elm == "]":
                adjacent = [[(next_i, next_j - 1)]]
            else:
                assert next_elm == "["
                adjacent = [[(next_i, next_j)]]
            stop = False
            while not stop:
                last_stage = adjacent[-1]
                new_stage = []
                blocked = False
                for next_i, next_j in last_stage:
                    up_left = next_i + coordinates[0], next_j
                    up_right = next_i + coordinates[0], next_j + 1
                    elm_left = curr_zone[up_left[0]][up_left[1]]
                    elm_right = curr_zone[up_right[0]][up_right[1]]
                    if elm_left == "#" or elm_right == "#":
                        blocked = True
                        stop = True
                        break
                    if elm_left == "[":
                        assert elm_right == "]"
                        new_stage.append(up_left)
                    if elm_left == "]":
                        new_stage.append((up_left[0], up_left[1] - 1))
                    if elm_right == "[":
                        assert curr_zone[up_right[0]][up_right[1] + 1] == "]"
                        new_stage.append(up_right)
                if not new_stage:
                    stop = True
                else:
                    adjacent.append(new_stage)
            if blocked:
                continue
            while adjacent:
                curr = adjacent.pop(-1)
                for (next_i, next_j) in curr:
                    curr_zone[next_i + coordinates[0]][next_j] = "["
                    curr_zone[next_i + coordinates[0]][next_j + 1] = "]"
                    curr_zone[next_i][next_j] = "."
                    curr_zone[next_i][next_j + 1] = "."
            curr_zone[start_next_i][start_next_j] = "@"
            curr_zone[curr_i][curr_j] = "."
            curr = start_next_i, start_next_j

    res = 0
    for i, l in enumerate(curr_zone):
        for j, e in enumerate(l):
            if e == "[":
                res += i * 100 + j
    return res


if __name__ == "__main__":
    raw_input = read_lines("input.txt")
    game_input = parse_input(raw_input)
    print(question_one(game_input))
    print(question_two(game_input))
