import re


def parse_input(fname="input.txt"):
    with open(fname, "r") as f:
        return f.read()

def question_one(game_input):
    expression = r"mul\((\d{1,3}),(\d{1,3})\)"
    matched = re.findall(expression, game_input)
    res = 0
    for m in matched:
        res += int(m[0]) * int(m[1])
    return res


def question_two(game_input):
    expression = r"(?:mul\((\d{1,3}),(\d{1,3})\))|(don?'?t?\(\))"
    matched = re.findall(expression, game_input)
    res = 0
    enabled = True
    for m in matched:
        print(m)
        if m[2] == "don't()":
            enabled = False
        elif m[2] == "do()":
            enabled = True
        elif enabled:
            res += int(m[0]) * int(m[1])
    return res


if __name__ == "__main__":
    game_input = parse_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))