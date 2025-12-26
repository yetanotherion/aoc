def read_input(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def find_start(lines):
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "S":
                return i, j


def question_one(fname):
    lines = read_input(fname)
    start_i, start_j = find_start(lines)
    max_i = len(lines)
    max_j = len(lines[0])
    curr_beams, next_level = [(start_i, start_j)], 1
    nb_split = 0
    while next_level < max_j:
        next_beams = set()
        while curr_beams:
            curr_i, curr_j = curr_beams.pop()
            next_i = curr_i + 1
            next_j = curr_j
            if next_i >= max_i:
                continue
            if lines[next_i][next_j] != "^":
                next_beams.add((next_i, next_j))
                continue
            nb_split += 1
            left_j = next_j - 1
            right_j = next_j + 1
            new_candidates = [(next_i, left_j), (next_i, right_j)]
            for ni, nj in new_candidates:
                if not (0 <= nj < max_j):
                    continue
                if (ni, nj) in next_beams:
                    continue
                next_beams.add((ni, nj))
        curr_beams = list(next_beams)
        next_level += 1
    return nb_split


def question_two(fname):
    lines = read_input(fname)
    start_i, start_j = find_start(lines)
    max_i = len(lines)
    max_j = len(lines[0])
    memory = [[0 for _ in range(max_j)] for _ in range(max_i)]
    memory[-1] = [1 for _ in range(max_j)]
    for i in range(max_i - 2, -1, -1):
        for j in range(0, max_j):
            n_i = i + 1
            if lines[n_i][j] != "^":
                memory[i][j] = memory[n_i][j]
                continue
            l_j = j - 1
            r_j = j + 1
            if l_j >= 0:
                memory[i][j] += memory[i + 1][l_j]
            if r_j < max_j:
                memory[i][j] += memory[i + 1][r_j]
    return memory[start_i][start_j]


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
