def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


LOCK, KEY = range(2)


def parse_input(lines):
    i = 0
    curr_number = [-1 for _ in range(len(lines[0]))]
    kind = None
    keys = []
    locks = []
    for curr in lines:
        if not curr:
            if kind == LOCK:
                locks.append(curr_number)
            else:
                keys.append(curr_number)
            curr_number = [-1 for _ in range(len(lines[0]))]
            kind = None
            continue
        if kind is None:
            if curr[0] == "#":
                kind = LOCK
            else:
                kind = KEY
        for i, e in enumerate(curr):
            if e == "#":
                curr_number[i] += 1
    if kind == LOCK:
        locks.append(curr_number)
    else:
        keys.append(curr_number)
    return locks, keys


def question_one(locks, keys):
    number_fit = 0
    for key in keys:
        for lock in locks:
            fit = all(a + b <= 5 for a, b in zip(key, lock))
            if fit:
                number_fit += 1
    return number_fit


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    locks, keys = parse_input(raw_input)
    print(question_one(locks, keys))
