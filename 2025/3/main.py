import functools


def read_input(fname):
    with open(fname) as f:
        return f.readlines()


def find_max(chars):
    max_idx = 0
    for i in range(1, len(chars)):
        if chars[i] > chars[max_idx]:
            max_idx = i
    return max_idx


def run(nb_digit, fname):
    lines = read_input(fname)
    res = 0

    for line in lines:
        chars = [int(x) for x in line[:-1]]
        idxes = []
        for i in range(nb_digit - 1, -1, -1):
            if not idxes:
                last_idx = -1
            else:
                last_idx = idxes[-1]
            next_start = last_idx + 1
            if i != 0:
                next_candidates = chars[next_start:-i]
            else:
                next_candidates = chars[next_start:]
            idxes.append(next_start + find_max(next_candidates))
        curr = 0
        for i, v in enumerate(idxes):
            curr += 10 ** (nb_digit - i - 1) * chars[v]
        res += curr
    return res


question_one = functools.partial(run, 2)
question_two = functools.partial(run, 12)

if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
