def read_input(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    db_started = False
    food_ids = []
    ranges = []
    for l in lines:
        line = l[:-1]
        if not line:
            db_started = True
            continue
        if db_started:
            food_ids.append(int(line))
        else:
            [start, end] = line.split("-")
            ranges.append((int(start), int(end)))
    return food_ids, ranges


def question_one(fname):
    food_ids, ranges = read_input(fname)
    counter = 0
    for f in food_ids:
        for start, end in ranges:
            if start <= f <= end:
                counter += 1
                break
    return counter


def no_overlap(f_start, f_end, o_start, o_end):
    # invariant:
    # f_start <= f_end
    # f_start <= o_start <= o_end
    return f_end < o_start  # no need: or o_end < f_start


def merge(f_start, f_end, o_start, o_end):
    # invariant: f_end >= o_start:
    return f_start, max(f_end, o_end)


def question_two(fname):
    _, ranges = read_input(fname)
    curr_list = sorted(ranges, key=lambda x: x[0])
    curr_idx = 0
    while curr_idx < len(curr_list):
        curr_start, curr_end = curr_list[curr_idx]
        for j in range(curr_idx + 1, len(curr_list)):
            o_start, o_end = curr_list[j]
            if no_overlap(curr_start, curr_end, o_start, o_end):
                curr_idx += 1
                break
            curr_list[curr_idx] = merge(curr_start, curr_end, o_start, o_end)
            curr_list.pop(j)
            break
        else:
            curr_idx += 1
    return sum([end - start + 1 for (start, end) in curr_list])


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
