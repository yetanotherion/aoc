def read_input(fname):
    with open(fname, "r") as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def parse_region(l):
    [header, other] = l.split(":")
    [i, j] = [int(x) for x in header.split("x")]
    nb_presents = [int(x.strip()) for x in other.split() if x.strip()]
    return ((i, j), nb_presents)


def number_holes_in_shape(shape):
    res = 0
    for l in shape:
        for c in l:
            if c == ".":
                res += 1
    return res


def parse_input(fname):
    lines = read_input(fname)
    presents = []
    curr_present = []
    regions = []
    for l in lines:
        if "x" in l:
            regions.append(parse_region(l))
            continue
        if ":" in l:
            if curr_present:
                presents.append(curr_present)
                curr_present = []
                continue
            continue
        curr_present.append(l)
    if curr_present:
        presents.append(curr_present)
    holes_in_present = [number_holes_in_shape(p) for p in presents]
    res = 0
    for r in regions:
        (height, width), constraints = r
        number_pixels = height * width
        total_pixel, total_holes = 0, 0
        for nb_hole, c in zip(holes_in_present, constraints):
            total_pixel += 9 * c
            total_holes += nb_hole * c
        if total_pixel - total_holes > number_pixels:
            continue
        if number_pixels >= total_pixel:
            res += 1
            continue
        assert False
    return res


if __name__ == "__main__":
    print(parse_input("input.txt"))
