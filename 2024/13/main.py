import re


def read_input(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_coordinates(button_param):
    pattern = re.compile(r"X\+(\d+), Y\+(\d+)")
    m = pattern.search(button_param)
    return (int(m.group(1)), int(m.group(2)))


def parse_prize(prize_param):
    pattern = re.compile(r"X=(\d+), Y=(\d+)")
    m = pattern.search(prize_param)
    return (int(m.group(1)), int(m.group(2)))


def parse_input(raw_input):
    res = []
    for group in [raw_input[i : i + 4] for i in range(0, len(raw_input), 4)]:
        a, b, prize = group[0], group[1], group[2]
        a, b, prize = a.strip(), b.strip(), prize.strip()
        parsed_a = parse_coordinates(a)
        parsed_b = parse_coordinates(b)
        parsed_prize = parse_prize(prize)
        res.append((parsed_a, parsed_b, parsed_prize))
    return res


def resolve_one(p_input):
    ((a_i, a_j), (b_i, b_j), (prize_i, prize_j)) = p_input
    # prize_i = token_a * a_i + token_b * b_i
    # prize_j = token_a * a_j + token_b * b_j
    assert b_i != 0
    assert b_j != 0
    # token_b = (prize_j / b_j) - token_a * a_j / b_j
    # token_b = (prize_i / b_i) - token_a * a_i / b_i

    # 0 = (prize_j / b_j) - (prize_i / b_i) + token_a * (a_i / b_i - a_j / b_j)
    coeff = a_i / b_i - a_j / b_j
    if coeff == 0:
        return None
    coeff_bis = prize_i / b_i - prize_j / b_j
    token_a = coeff_bis / coeff
    token_b = prize_j / b_j - token_a * a_j / b_j
    check_a, check_b = round(token_a), round(token_b)
    if prize_i != check_a * a_i + check_b * b_i:
        return None
    if prize_j != check_a * a_j + check_b * b_j:
        return None
    return check_a, check_b


def question_one(game_input):
    token = 0
    for equation in game_input:
        curr_res = resolve_one(equation)
        if curr_res is not None:
            token_a, token_b = curr_res
            token += token_a * 3 + token_b
    return token


def question_two(game_input):
    token = 0
    for equation in game_input:
        button_a, button_b, prize = equation
        increase = 10000000000000
        new_prize = prize[0] + increase, prize[1] + increase
        new_equation = (button_a, button_b, new_prize)
        curr_res = resolve_one(new_equation)
        if curr_res is not None:
            token_a, token_b = curr_res
            token += token_a * 3 + token_b
    return token


if __name__ == "__main__":
    raw_input = read_input(fname="input.txt")
    game_input = parse_input(raw_input)
    print(question_one(game_input))
    print(question_two(game_input))
