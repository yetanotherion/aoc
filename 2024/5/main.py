def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    constraints = {}
    updates = []
    for l in lines:
        if not l:
            continue
        if "|" in l:
            left_s, right_s = l.split("|")
            left, right = int(left_s), int(right_s)
            constraints.setdefault(left, []).append(right)
        else:
            update = [int(x) for x in l.split(",")]
            updates.append(update)
    return constraints, updates


def find_incorrect(i, constraints, update):
    curr = update[i]
    related_constraints = set(constraints.get(curr, []))
    for i, other in enumerate(update[:i]):
        if other in related_constraints:
            return i
    return None


def is_correct(i, constraints, update):
    return find_incorrect(i, constraints, update) is None


def is_update_correct(update, constraints):
    return all(is_correct(i, constraints, update) for i in range(len(update)))


def question_one(game_input):
    constraints, updates = game_input

    correct_updates = []
    for update in updates:
        if is_update_correct(update, constraints):
            correct_updates.append(update)
    return sum(update[len(update) // 2] for update in correct_updates)


def sort_if_necessary(constraints, update):
    curr_idx = 0
    while curr_idx < len(update):
        curr_element = update[curr_idx]
        wrong_idx = find_incorrect(curr_idx, constraints, update)
        if wrong_idx is not None:
            new_update = update[:wrong_idx]
            new_update.append(curr_element)
            update.pop(curr_idx)
            new_update.extend(update[wrong_idx:])
            update = new_update
        else:
            curr_idx += 1
    return update


def question_two(game_input):
    constraints, updates = game_input
    res = []
    for update in updates:
        sorted_update = sort_if_necessary(constraints, update)
        if sorted_update != update:
            res.append(sorted_update)

    return sum(update[len(update) // 2] for update in res)


if __name__ == "__main__":
    raw_input = read_input(fname="input.txt")
    game_input = parse_input(raw_input)
    print(question_one(game_input))
    print(question_two(game_input))
