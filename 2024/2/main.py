from itertools import pairwise


def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        content = f.readlines()
        return [l[:-1] for l in content]


def parse_input(lines):
    res = []
    for l in lines:
        res.append([int(x.strip()) for x in l.split(" ")])
    return res


def question_one(lines):
    res = 0
    for l in lines:
        if is_safe(l):
            res += 1
    return res


def question_two(lines):
    res = 0
    for l in lines:
        if is_safe(l):
            res += 1
            continue
        for idx in range(len(l)):
            new_l = l[:]
            new_l.pop(idx)
            if is_safe(new_l):
                res += 1
                break
    return res


def is_safe(l):
    serie_increasing = None
    for curr, next in pairwise(l):
        delta = curr - next
        increasing = delta < 0
        if abs(delta) < 1 or abs(delta) > 3:
            return False
        if serie_increasing is None:
            serie_increasing = increasing
        elif serie_increasing != increasing:
            return False
    return True


if __name__ == "__main__":
    game_input = parse_input(read_input(fname="input.txt"))
    print(question_one(game_input))
    print(question_two(game_input))