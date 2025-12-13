from itertools import pairwise


def read_input(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def area(l, r):
    return (abs(r[0] - l[0]) + 1) * (abs(r[1] - l[1]) + 1)


def load_coordinates(fname):
    lines = read_input(fname)
    coordinates = []
    for l in lines:
        coordinates.append(tuple(int(x) for x in l.split(",")))
    return coordinates


def question_one(fname):
    coordinates = load_coordinates(fname)
    max_area = 0
    for i, c in enumerate(coordinates[:-1]):
        for j in range(i + 1, len(coordinates)):
            max_area = max(max_area, area(c, coordinates[j]))
    return max_area


def rectangle(l_c, r_c):
    min_x, max_x = min(l_c[0], r_c[0]), max(l_c[0], r_c[0])
    min_y, max_y = min(l_c[1], r_c[1]), max(l_c[1], r_c[1])
    return [(min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)]


def rectangle_inside(l_c, r_c, coordinates):
    rectangle_coord = rectangle(l_c, r_c)
    [(_, _), (max_x, min_y), (min_x, max_y), (max_x, max_y)] = rectangle_coord
    for c in coordinates:
        c_x, c_y = c
        if (
            min_x <= c_x <= max_x and min_y <= c_y <= max_y
        ) and c not in rectangle_coord:
            return False
    return True


def draw_segments(points, chosen_points):
    import matplotlib.pyplot as plt

    closed_points = points + [points[0]]

    xs = [p[0] for p in closed_points]
    ys = [p[1] for p in closed_points]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, marker="o")
    for chosen in chosen_points:
        plt.scatter(
            chosen[0], chosen[1], color="red", s=100, zorder=5, label="Chosen point"
        )
    plt.axis("equal")
    plt.grid(True)

    plt.title("Segments visualization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def question_two(fname):
    coordinates = load_coordinates(fname)
    segments = list(pairwise(coordinates))
    segments.append((coordinates[-1], coordinates[0]))

    biggest = sorted(
        segments,
        key=lambda x: abs(x[0][0] - x[1][0]) + abs(x[0][1] - x[1][1]),
        reverse=True,
    )

    first = sorted(biggest[0])[1]
    first_candidates = [c for c in coordinates if c[1] <= first[1]]
    second = sorted(biggest[1])[1]
    second_candidates = [c for c in coordinates if c[1] >= second[1]]
    candidates = [(first, c) for c in first_candidates]
    candidates.extend([(second, c) for c in second_candidates])

    max_area = 0

    chosen = []
    for a, b in candidates:
        if rectangle_inside(a, b, coordinates):
            curr_area = area(a, b)
            if curr_area > max_area:
                chosen.append(rectangle(a, b))
                max_area = curr_area
    draw_segments(list(coordinates), chosen[-1])
    return max_area


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
