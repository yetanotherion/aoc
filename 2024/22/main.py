def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(l):
    return [int(x) for x in l]


def mix(x, initial):
    return x ^ initial


def prune(x):
    return x % 16777216


def next_secret_number(secret_number):
    secret_number = prune(mix(secret_number * 64, secret_number))
    secret_number = prune(mix(secret_number // 32, secret_number))
    return prune(mix(secret_number * 2048, secret_number))


def question_one(numbers):
    res = []
    for n in numbers:
        next_s = n
        for _ in range(2000):
            next_s = next_secret_number(next_s)
        res.append(next_s)
    return sum(res)


if __name__ == "__main__":
    game_input = parse_input(read_lines(fname="input.txt"))
    print(question_one(game_input))
