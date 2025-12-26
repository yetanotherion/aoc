import functools


def read_input(fname):
    with open(fname) as f:
        return f.read()


def invalid_digit_one(x):
    if len(x) % 2 != 0:
        return False
    middle = len(x) // 2

    return int(x[0:middle]) == int(x[middle:])


def invalid_digit_two(x):
    for l in range(1, len(x) // 2 + 1):
        seq_start = range(0, len(x), l)
        sequences = [x[s : s + l] for s in seq_start]
        if any(not x for x in sequences):
            continue
        sequences = set(int(x) for x in sequences)
        if len(sequences) == 1:
            return True
    return False


def run(invalid, fname):
    content = read_input(fname)
    ranges = content.split(",")
    sum = 0
    for r in ranges:
        [first, second] = [int(x) for x in r.split("-")]
        numbers = range(first, second + 1)
        for n in numbers:
            if invalid(str(n)):
                sum += n
    return sum


question_one = functools.partial(run, invalid_digit_one)
question_two = functools.partial(run, invalid_digit_two)

if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
