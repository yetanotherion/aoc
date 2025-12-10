def read_input(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def parse_targets(targets):
    res = []
    for t in targets[1:-1]:
        if t == ".":
            res.append(False)
        else:
            res.append(True)
    return res


def parse_buttons(buttons):
    return [int(x) for x in str(buttons[1:-1]).split(",")]


def parse_voltage(voltage):
    return parse_buttons(voltage)


def press_button(curr_button, buttons):
    new_button = list(curr_button)
    for b in buttons:
        curr_value = curr_button[b]
        if curr_value:
            new_button[b] = False
        else:
            new_button[b] = True
    return tuple(new_button)


def solve(targets, buttons):
    targets = tuple(targets)
    curr_button = tuple(False for _ in range(len(targets)))
    states = [(curr_button, 0)]
    seen_states = {curr_button}
    while True:
        states = sorted(states, key=lambda x: x[1])
        curr_state, curr_number = states.pop(0)
        diff = [i for i, v in enumerate(curr_state) if v != targets[i]]
        for button_to_switch in diff:
            candidate_buttons = [
                v for b, v in enumerate(buttons) if button_to_switch in v
            ]
            for v in candidate_buttons:
                new_button = press_button(curr_state, v)
                if new_button == targets:
                    return curr_number + 1
                if new_button not in seen_states:
                    states.append((new_button, curr_number + 1))
                    seen_states.add(new_button)


def solve_two(targets, buttons):
    import numpy as np
    from scipy.optimize import linprog

    c = [1 for _ in range(len(buttons))]
    b_eq = np.array(list(targets))
    a_array = []
    for i in range(len(targets)):
        curr_a = [0 for _ in range(len(buttons))]
        for j, b in enumerate(buttons):
            if i in b:
                curr_a[j] = 1
        a_array.append(curr_a)
    bounds = [(0, None) for _ in range(len(buttons))]
    result = linprog(
        c,
        A_eq=a_array,
        b_eq=b_eq,
        bounds=bounds,
        integrality=[1 for _ in range(len(buttons))],
    )
    assert result.success
    return int(sum(round(x) for x in result.x))


def question_one(fname):
    num_press = 0
    for line in read_input(fname):
        splitted = line.split()
        targets = parse_targets(splitted[0])
        buttons = [parse_buttons(s) for s in splitted[1:-1]]
        solved = solve(targets, buttons)
        num_press += solved
    return num_press


def question_two(fname):
    num_press = 0
    for line in read_input(fname):
        splitted = line.split()
        targets = tuple(parse_buttons(splitted[-1]))
        buttons = [parse_buttons(s) for s in splitted[1:-1]]
        solved = solve_two(targets, buttons)
        num_press += solved
    return num_press


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
