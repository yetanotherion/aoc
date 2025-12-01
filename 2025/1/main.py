def readlines(fname):
    with open(fname) as f:
        return f.readlines()


def question_one(fname):
    lines = readlines(fname)
    curr = 50
    nb = 0
    for l in lines:
        r, number = l[0], int(l[1:])
        if r == "L":
            curr -= number
        else:
            curr += number
        curr = curr % 100
        if curr == 0:
            nb += 1
    return nb


def question_two(fname):
    lines = readlines(fname)
    curr = 50
    nb = 0
    for l in lines:
        r, number = l[0], int(l[1:])
        nb += number // 100
        number %= 100
        before = curr
        if r == "L":
            curr -= number
        else:
            curr += number
        if (before != 0 and curr <= 0) or curr >= 100:
            nb += 1
        curr = curr % 100
    return nb


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
