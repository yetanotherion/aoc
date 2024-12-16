def read_input(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    res = []
    for l in lines:
        [p, v] = l.split(" ")
        (x, y) = (int(x) for x in p[len("p=") :].split(","))
        v_x, v_y = (int(x) for x in v[len("v=") :].split(","))
        res.append(((x, y), (v_x, v_y)))
    return res


def do_modulo(coord, max_coord):
    return coord % max_coord


def question_one(lines, max_tiles=(11, 7), num_simu=100):
    max_x, max_y = max_tiles
    last_point = {}
    for ((start_x, start_y), (v_x, v_y)) in lines:
        next_x = (start_x + v_x * num_simu) % max_x
        next_y = (start_y + v_y * num_simu) % max_y
        key = (next_x, next_y)
        last_point.setdefault((next_x, next_y), 0)
        last_point[key] += 1
    up_left, up_right, down_left, down_right = 0, 0, 0, 0
    half_x = (max_x - 1) // 2
    half_y = (max_y - 1) // 2
    for k, v in last_point.items():
        x, y = k
        if x == half_x or y == half_y:
            continue
        if x < half_x:
            if y < half_y:
                up_left += v
            else:
                down_left += v
        else:
            if y < half_y:
                up_right += v
            else:
                down_right += v
    return up_right * up_left * down_right * down_left


def question_two(lines, max_tiles=(101, 103)):
    max_x, max_y = max_tiles
    curr_lines = lines
    all_max_aligned = 0
    all_max_simu = 0
    for num_simu in range(max_x * max_y):
        new_lines = []
        for ((start_x, start_y), (v_x, v_y)) in curr_lines:
            next_x = (start_x + v_x) % max_x
            next_y = (start_y + v_y) % max_y
            new_lines.append(((next_x, next_y), (v_x, v_y)))
        curr_lines = new_lines
        all_points = [x[0] for x in curr_lines]
        all_y = sorted(all_points, key=lambda x: (-x[1], -x[0]))
        max_aligned = 0
        before = all_y[0]
        curr_aligned = 0
        for other in all_y[1:]:
            if before[1] == other[1] and before[0] - other[0] == 1:
                curr_aligned += 1
            else:
                max_aligned = max(max_aligned, curr_aligned)
                curr_aligned = 0
            before = other
        if max_aligned > all_max_aligned:
            all_max_aligned = max_aligned
            all_max_simu = num_simu + 1

    for num_simu in range(all_max_simu):
        new_lines = []
        for ((start_x, start_y), (v_x, v_y)) in curr_lines:
            next_x = (start_x + v_x) % max_x
            next_y = (start_y + v_y) % max_y
            new_lines.append(((next_x, next_y), (v_x, v_y)))
        curr_lines = new_lines

    new_res = [["." for _ in range(max_x)] for _ in range(max_y)]
    for ((start_x, start_y), _) in curr_lines:
        new_res[start_y][start_x] = "X"
    for l in new_res:
        print("".join(l))
    return all_max_simu


if __name__ == "__main__":
    raw_input = read_input(fname="input.txt")
    game_input = parse_input(raw_input)
    print(question_one(game_input, (101, 103)))
    print(question_two(game_input, (101, 103)))
