def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return f.readlines()


def parse_input(game_input):
    return [(int(l[0:5]), int(l[8:-1]))
            for l in game_input]

def question_one(tuples):
    left = sorted([x[0] for x in tuples])
    right = sorted(x[1] for x in tuples)
    return sum(abs(x - y) for (x, y) in zip(left, right))

def question_two(tuples):
    left = sorted([x[0] for x in tuples])
    right = sorted(x[1] for x in tuples)
    left_idx, right_idx = 0, 0
    res = 0
    while left_idx < len(left) and right_idx < len(right):
        right_element = right[right_idx]
        left_element = left[left_idx]
        if left_element == right_element:
            res += left_element
            right_idx += 1
        elif left_element < right_element:
            left_idx += 1
        else:
            right_idx += 1
    return res

    return sum(abs(x - y) for (x, y) in zip(left, right))

if __name__ == "__main__":
    game_input = parse_input(read_input())
    print(question_one(game_input))
    print(question_two(game_input))