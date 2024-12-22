import copy


def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    registers = {}
    program = []
    for l in lines:
        if not l:
            continue
        if "Register" in l:

            (register, value) = tuple(x.strip() for x in l.split(":"))
            register_name = register[len("Register ") :]
            registers[register_name] = int(value)
        if "Program" in l:
            program.append(l[len("Program: ") :])
    return registers, [int(x) for x in "".join(program).split(",")]


class InvalidProgram(Exception):
    pass


def read_combo_operand(registers, value):
    if value <= 3:
        return value
    if value == 4:
        return registers["A"]
    if value == 5:
        return registers["B"]
    if value == 6:
        return registers["C"]
    raise InvalidProgram(f"Got {value} as combo operand")


def run_program(init_registers, program):
    registers = copy.deepcopy(init_registers)
    curr_idx = 0
    stdout = []
    while curr_idx < len(program) and curr_idx >= 0:
        operand, arg = program[curr_idx], program[curr_idx + 1]
        next_idx = curr_idx + 2
        if operand == 0:  # "adv"
            numerator = registers["A"]
            denominator = read_combo_operand(registers, arg)
            registers["A"] = numerator // (2**denominator)
        if operand == 1:  # bxl
            registers["B"] = registers["B"] ^ arg
        if operand == 2:  #  bst
            registers["B"] = read_combo_operand(registers, arg) % 8
        if operand == 3:  # jnz
            if registers["A"] != 0:
                next_idx = arg
        if operand == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        if operand == 5:  # out
            output = read_combo_operand(registers, arg) % 8
            stdout.append(output)
        if operand == 6:  # bdv
            numerator = registers["A"]
            denominator = read_combo_operand(registers, arg)
            registers["B"] = numerator // (2**denominator)
        if operand == 7:  # cdv
            numerator = registers["A"]
            denominator = read_combo_operand(registers, arg)
            registers["C"] = numerator // (2**denominator)
        curr_idx = next_idx
    return stdout


def test_one():
    registers = {"A": 0, "B": 0, "C": 9}
    res, new_registers = run_program(registers, [2, 6])
    assert new_registers["B"] == 1


def test_two():
    registers = {"A": 10, "B": 0, "C": 0}
    res, new_registers = run_program(registers, [5, 0, 5, 1, 5, 4])
    assert res == "0,1,2"


def test_three():
    registers = {"A": 2024, "B": 0, "C": 0}
    res, new_registers = run_program(registers, [0, 1, 5, 4, 3, 0])
    assert res == "4,2,5,6,7,7,7,7,3,1,0"
    assert new_registers["A"] == 0


def test_four():
    registers = {"A": 0, "B": 29, "C": 0}
    res, new_registers = run_program(registers, [1, 7])
    assert new_registers["B"] == 26


def test_five():
    registers = {"A": 0, "B": 2024, "C": 43690}
    res, new_registers = run_program(registers, [4, 0])
    assert new_registers["B"] == 44354


def question_one(registers, program):
    return ",".join(str(x) for x in run_program(registers, program))


def tests():
    test_one()
    test_two()
    test_three()
    test_four()
    test_five()


def question_two(program):
    to_browse = [[0]]
    res = []
    while to_browse:
        curr = to_browse.pop()
        curr_start = curr[-1] * 8
        for a in range(8):
            new_registers = {"A": curr_start + a, "B": 0, "C": 0}
            output = run_program(new_registers, program)

            if program[-len(output) :] == output:
                if len(output) == len(program):
                    res.append(curr_start + a)
                new_path = curr[:]
                new_path.append(curr_start + a)
                to_browse.append(new_path)
    return min(res)


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    registers, program = parse_input(raw_input)
    print(question_one(registers, program))
    print(question_two(program))
