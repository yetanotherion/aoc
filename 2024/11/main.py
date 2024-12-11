def read_input(fname="input.txt"):
    with open(fname) as f:
        return f.read().strip().split(" ")


def apply_rule(number):
    if number == "0":
        return ("1", None)
    len_number = len(number)
    if len_number % 2 == 0:
        half = len_number // 2
        left = number[:half]
        right = number[half:]
        return (str(int(left)), str(int(right)))
    return str(int(number) * 2024), None


def compress(numbers):
    res = {}
    for n in numbers:
        curr = res.setdefault(n, 0)
        res[n] = curr + 1
    return res


def question_one(numbers, nb_round=25):
    curr = compress(numbers)

    for _ in range(nb_round):
        res = {}
        for k, v in curr.items():
            new_v, optional = apply_rule(k)
            curr = res.setdefault(new_v, 0)
            res[new_v] = curr + v
            if optional is not None:
                curr = res.setdefault(optional, 0)
                res[optional] = curr + v
        curr = res
    return sum(curr.values())


def question_two(numbers):
    return question_one(numbers, nb_round=75)


if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input, nb_round=25))
    print(question_two(game_input))
