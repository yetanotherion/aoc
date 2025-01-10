def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


AND, XOR, OR = range(3)


def parse_input(lines):
    gate_values = {}
    operators = []
    for l in lines:
        if ":" in l:
            name, raw_value = l.split(":")
            value = int(raw_value.strip())
            gate_values[name] = value
            continue
        if not l:
            continue
        left, right = l.split("->")
        target = right.strip()
        left_name, raw_op, right_name = left.strip().split(" ")
        op = AND
        if raw_op == "AND":
            op = AND
        if raw_op == "OR":
            op = OR
        if raw_op == "XOR":
            op = XOR
        operators.append((left_name, op, right_name, target))
    return gate_values, operators


def build_gate_circuit(wires):
    res = {}
    for left_name, op, right_name, target in wires:
        res.setdefault(left_name, []).append((left_name, op, right_name, target))
        res.setdefault(right_name, []).append((left_name, op, right_name, target))
    return res


def build_dependencies(wires):
    res = {}
    for left_name, op, right_name, target in wires:
        res[target] = [left_name, right_name]
    return res


def build_transitive_dependencies(dependencies, label):
    res = set()
    to_explore = [[label]]
    while to_explore:
        curr_path = to_explore.pop()
        curr = curr_path[-1]
        curr_deps = dependencies.get(curr, [])
        for dep in curr_deps:
            res.add(dep)
            if dep in curr_path:
                return None
            new_path = curr_path + [dep]
            to_explore.append(new_path)
    return res


def eval(left, op, right):
    if op == AND:
        return left & right
    if op == OR:
        return left | right
    if op == XOR:
        return left ^ right


def compute_z(gate_values, prefix="z"):
    z_names = [k for k in gate_values if k.startswith(prefix)]
    sorted_z_names = sorted(z_names, key=lambda x: int(x[1:]))
    res = 0
    curr_mult = 1
    for s in sorted_z_names:
        res += gate_values[s] * curr_mult
        curr_mult *= 2
    return res


def compute_all(init_gate_values, wires):
    gate_values = {k: v for k, v in init_gate_values.items()}
    gate_circuits = build_gate_circuit(wires)
    new_inputs = list(gate_values.keys())
    while new_inputs:
        next_input = new_inputs.pop(0)
        if next_input not in gate_circuits:
            continue
        for left, op, right, target in gate_circuits[next_input]:
            if target in gate_values:
                continue
            left_v, right_v = gate_values.get(left), gate_values.get(right)
            if left_v is None or right_v is None:
                continue
            new_v = eval(left_v, op, right_v)
            gate_values[target] = new_v
            new_inputs.append(target)
    return gate_values


def question_one(init_gate_values, operators):
    gate_values = compute_all(init_gate_values, operators)
    return compute_z(gate_values)


def swap(curr_value, left, right):
    if curr_value == left:
        return right
    if curr_value == right:
        return left
    return curr_value


def rewire(wires, left_wire, right_wire):
    new_wires = []
    for left, op, right, target in wires:
        new_wires.append((left, op, right, swap(target, left_wire, right_wire)))
    return new_wires


def validate(wires, i):
    curr_x_l = f"x{i:02}"
    curr_y_l = f"y{i:02}"
    before_x_l = f"x{i-1:02}"
    before_y_l = f"y{i-1:02}"
    expected_z_l = f"z{i:02}"
    tests = [
        ((0, 0, 0, 0), 0),
        ((0, 0, 0, 1), 0),
        ((0, 0, 1, 0), 0),
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), 1),
        ((0, 1, 1, 0), 1),
        ((0, 1, 1, 1), 0),
        ((1, 0, 0, 0), 1),
        ((1, 0, 0, 1), 1),
        ((1, 0, 1, 0), 1),
        ((1, 0, 1, 1), 0),
        ((1, 1, 0, 0), 0),
        ((1, 1, 0, 1), 0),
        ((1, 1, 1, 0), 0),
        ((1, 1, 1, 1), 1),
    ]
    i_gate_values = {}
    for before in range(i - 1):
        i_gate_values[f"x{before:02}"] = 0
        i_gate_values[f"y{before:02}"] = 0
    for (curr_x, curr_y, before_x, before_y), expected_z in tests:
        gate_values = i_gate_values.copy()
        gate_values.update(
            {
                curr_x_l: curr_x,
                curr_y_l: curr_y,
                before_x_l: before_x,
                before_y_l: before_y,
            }
        )
        new_gate_values = compute_all(gate_values, wires)

        z_val = new_gate_values.get(expected_z_l)
        if z_val != expected_z:
            return False
    return True


def question_two(wires, max_i=45):
    swaps = []
    curr_wire = wires
    dependencies = build_dependencies(wires)
    candidates = [
        k for k in dependencies.keys() if not (k.startswith("x") or k.startswith("y"))
    ]
    for i in range(1, max_i):
        if validate(curr_wire, i):
            transitive = build_transitive_dependencies(dependencies, f"z{i:02}")
            candidates = [k for k in candidates if k not in transitive]
            continue
        swap_candidates = [
            (a, b) for idx, a in enumerate(candidates) for b in candidates[idx + 1 :]
        ]
        for a, b in swap_candidates:
            new_wire = rewire(curr_wire, a, b)
            if validate(new_wire, i):
                curr_wire = new_wire
                swaps.append((a, b))
                transitive = build_transitive_dependencies(dependencies, f"z{i:02}")
                candidates = [k for k in candidates if k not in transitive]
                break
    for i in range(1, max_i):
        assert validate(curr_wire, i)
    res = []
    for a, b in swaps:
        res.append(a)
        res.append(b)
    return ",".join(sorted(res))


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    gate_values, wires = parse_input(raw_input)
    print(question_one(gate_values, wires))
    print(question_two(wires))
