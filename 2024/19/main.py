def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    towels = [x.strip() for x in lines[0].split(",")]
    designs = [x.strip() for x in lines[2:]]
    return towels, designs


def is_possible(towels, design):
    to_browse = [design[:]]
    while to_browse:
        next = to_browse.pop()
        for towel in towels:
            if next.startswith(towel):
                remaining = next[len(towel) :]
                if not remaining:
                    return True
                to_browse.append(remaining)
    return False


def question_one(towels, designs):
    possible = [x for x in designs if is_possible(towels, x)]
    return len(possible)


def question_two(towels, designs):
    res = 0
    for design in designs:
        curr_res = {}
        for i in range(1, len(design) + 1):
            to_see = design[-i:]
            for towel in towels:
                if to_see.startswith(towel):
                    remaining = to_see[len(towel) :]
                    if not remaining:
                        curr = curr_res.setdefault(towel, 0)
                        curr_res[towel] = curr + 1
                    else:
                        existing = curr_res.get(remaining)
                        if not existing:
                            continue
                        curr = curr_res.setdefault(to_see, 0)
                        curr_res[to_see] = curr + existing
        if design in curr_res:
            res += curr_res[design]
    return res


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    towels, designs = parse_input(raw_input)
    print(question_one(towels, designs))
    print(question_two(towels, designs))
