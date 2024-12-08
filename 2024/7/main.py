def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    equations = []
    for l in lines:
        left, right = l.split(":")
        goal = int(left)
        numbers = [int(x) for x in right.split(" ") if x]
        equations.append((goal, numbers))
    return equations


def is_solvable(equation):
    goal, operations = equation
    possibilities = [(goal, operations)]
    while possibilities:
        next_goal, next_op = possibilities.pop()
        if len(next_op) == 1:
            if next_goal == next_op[0]:
                return True
            else:
                continue
        last = next_op[-1]
        if next_goal % last == 0:
            remaining = next_goal // last
            possibilities.append((remaining, next_op[:-1]))
        possibilities.append((next_goal - last, next_op[:-1]))


def is_solvable_two(equation):
    goal, operations = equation
    possibilities = [(goal, operations)]
    while possibilities:
        next_goal, next_op = possibilities.pop()
        if len(next_op) == 1:
            if next_goal == next_op[0]:
                return True
            else:
                continue
        last = next_op[-1]
        if next_goal % last == 0:
            remaining = next_goal // last
            possibilities.append((remaining, next_op[:-1]))
        if next_goal < 0:
            continue
        next_goal_str, last_str = str(next_goal), str(last)
        if next_goal_str.endswith(last_str):
            remaining_len = len(next_goal_str) - len(last_str)
            if remaining_len == 0:
                new_remaining = 0
            else:
                new_remaining = int(next_goal_str[:remaining_len])
            possibilities.append((new_remaining, next_op[:-1]))
        possibilities.append((next_goal - last, next_op[:-1]))


def question_one(equations):
    res = 0
    for equation in equations:
        if is_solvable(equation):
            res += equation[0]
    return res


def question_two(equations):
    res = 0
    for equation in equations:
        if is_solvable_two(equation):
            res += equation[0]
    return res


if __name__ == "__main__":
    raw_input = read_input(fname="input.txt")
    game_input = parse_input(raw_input)
    print(question_one(game_input))
    print(question_two(game_input))
