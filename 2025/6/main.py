import functools


def read_input(fname):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines() if l[:-1].strip()]


def f_from_op(operation):
    if operation == "+":
        return lambda x, y: x + y
    return lambda x, y: x * y


def question_one(fname):
    raw_lines = read_input(fname)
    lines = [[x.strip() for x in l.split()] for l in raw_lines]
    res = 0
    for j in range(len(lines[0])):
        f = f_from_op(lines[-1][j])
        numbers = [int(lines[i][j]) for i in range(len(lines) - 1)]
        curr_result = functools.reduce(lambda acc, x: f(acc, x), numbers)
        res += curr_result
    return res


def question_two(fname):
    lines = read_input(fname)
    res = 0
    curr_numbers = []
    for j in range(len(lines[0]) - 1, -1, -1):
        curr_digits = []
        for i in range(len(lines) - 1):
            if lines[i][j].strip():
                curr_digits.append(lines[i][j])
        if not curr_digits:
            continue
        curr_number = int("".join(curr_digits))
        curr_numbers.append(curr_number)
        if not lines[-1][j]:
            continue
        operation = lines[-1][j]
        if not operation.strip():
            continue
        f = f_from_op(operation)
        curr_result = functools.reduce(lambda acc, x: f(acc, x),
                                       curr_numbers)
        res += curr_result
        curr_numbers = []
    return res


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))