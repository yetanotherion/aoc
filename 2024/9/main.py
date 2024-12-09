import copy
from dataclasses import dataclass


def read_input(fname="input.txt"):
    with open(fname, "r") as f:
        return f.read().strip()


def batched(iterable, n):
    return zip(*(iter(iterable),) * n)


def parse_input(raw_input):
    file_blocks = []
    free_blocks = []
    if len(raw_input) % 2 == 1:
        raw_input += "0"
    for (occupied, free) in batched(raw_input, n=2):
        nb_occuped, nb_free = int(occupied), int(free)
        file_blocks.append(nb_occuped)
        free_blocks.append(nb_free)
    return file_blocks, free_blocks


def question_one(game_input):
    file_blocks, free_blocks = game_input
    i = 0
    multiplier_idx = 0
    res = 0
    while i < len(file_blocks):
        curr_file, curr_free = file_blocks[i], free_blocks[i]
        for _ in range(curr_file):
            res += i * multiplier_idx
            multiplier_idx += 1
        remaining_free = curr_free
        if i == len(file_blocks) - 1:
            i += 1
            continue
        while remaining_free:
            last_idx = len(file_blocks) - 1
            last_elt = file_blocks.pop(-1)
            taken = min(last_elt, remaining_free)
            if last_elt <= remaining_free:
                remaining_free -= last_elt
            else:
                file_blocks.append(last_elt - remaining_free)
                remaining_free = 0
            for _ in range(taken):
                res += last_idx * multiplier_idx
                multiplier_idx += 1
        i += 1
    return res


@dataclass
class FreeSlot:
    idx: int
    len: int


def question_two(game_input):
    file_blocks, free_blocks = game_input
    moved_slots = [[] for _ in range(len(free_blocks))]
    j = len(file_blocks) - 1
    moved_block = [False for _ in range(len(file_blocks))]
    while j >= 0:
        curr_free_slot_idx = 0
        curr = file_blocks[j]
        while curr_free_slot_idx < j:
            remaining = free_blocks[curr_free_slot_idx]
            if remaining >= curr:
                moved_block[j] = True
                moved_slots[curr_free_slot_idx].append(FreeSlot(idx=j, len=curr))
                new_remaining = remaining - curr
                free_blocks[curr_free_slot_idx] = new_remaining
                break
            else:
                curr_free_slot_idx += 1
        j -= 1
    res = 0
    mult_idx = 0
    for i, file_block in enumerate(file_blocks):
        for _ in range(file_block):
            if not moved_block[i]:
                res += i * mult_idx
            mult_idx += 1
        for moved_slot in moved_slots[i]:
            for _ in range(moved_slot.len):
                res += moved_slot.idx * mult_idx
                mult_idx += 1
        if free_blocks[i] > 0:
            mult_idx += free_blocks[i]
    return res


if __name__ == "__main__":
    raw_input = read_input(fname="input.txt")
    game_input = parse_input(raw_input)
    print(question_one(copy.deepcopy(game_input)))
    print(question_two(copy.deepcopy(game_input)))
