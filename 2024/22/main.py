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


def question_two(numbers, rounds=2000):
    numbers_keys = []
    for n in numbers:
        next_s = n
        curr_res = []
        before = int(str(next_s)[-1])
        s_codes = {}
        for _ in range(rounds):
            next_s = next_secret_number(next_s)
            curr_digit = int(str(next_s)[-1])
            delta = curr_digit - before
            before = curr_digit
            if len(curr_res) == 4:
                curr_res.pop(0)
            curr_res.append(delta)
            curr_key = tuple(curr_res)
            if curr_key not in s_codes and len(curr_key) == 4:
                s_codes[curr_key] = curr_digit
        numbers_keys.append(s_codes)
    curr_max = 0
    all_keys = set()
    for n in numbers_keys:
        all_keys = all_keys.union(set(n.keys()))
    for k in all_keys:
        all_values = [d.get(k, 0) for d in numbers_keys]
        curr_res = sum(all_values)
        curr_max = max(curr_res, curr_max)
    return curr_max


if __name__ == "__main__":
    game_input = parse_input(read_lines(fname="input.txt"))
    print(question_one(game_input))
    print(question_two(game_input))
