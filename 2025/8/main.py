def read_input(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def compute_distances(fname):
    lines = read_input(fname)
    coord = []
    for l in lines:
        coord.append(tuple(int(x) for x in l.split(",")))
    distances = []
    for i, c in enumerate(coord[:-1]):
        xi, yi, zi = c
        for j in range(i + 1, len(coord)):
            xj, yj, zj = coord[j]
            distances.append((i, j, (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2))
    return coord, sorted(distances, key=lambda x: x[2])


def connect(i, j, circuits, nb_elm_in_circuit, nxt_circuit_idx):
    if i in circuits and j in circuits:
        root_i = circuits[i]
        root_j = circuits[j]
        if root_i == root_j:
            return circuits, nxt_circuit_idx
        next_root = min(root_i, root_j)
        to_replace = max(root_i, root_j)
        nb_elm_in_circuit[next_root] += nb_elm_in_circuit[to_replace]
        nb_elm_in_circuit.pop(to_replace)
        new_circuits = {}
        for k, v in circuits.items():
            new_v = v
            if v == to_replace:
                new_v = next_root
            new_circuits[k] = new_v
        circuits = new_circuits
    if i not in circuits and j not in circuits:
        circuits[i] = nxt_circuit_idx
        circuits[j] = nxt_circuit_idx
        nb_elm_in_circuit[nxt_circuit_idx] = 2
        nxt_circuit_idx += 1

    if i not in circuits and j in circuits:
        circuits[i] = circuits[j]
        nb_elm_in_circuit[circuits[j]] += 1
    if i in circuits and j not in circuits:
        circuits[j] = circuits[i]
        nb_elm_in_circuit[circuits[i]] += 1
    return circuits, nxt_circuit_idx


def question_one(fname, max_nb_connections=10):
    circuits = {}
    nb_elm_in_circuit = {}
    nxt_circuit_idx = 0
    _, distances = compute_distances(fname)
    for i, j, _ in distances[:max_nb_connections]:
        circuits, nxt_circuit_idx = connect(
            i, j, circuits, nb_elm_in_circuit, nxt_circuit_idx
        )
    circuit_sizes = list(reversed(sorted(nb_elm_in_circuit.values())))
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def question_two(fname):
    circuits = {}
    nb_elm_in_circuit = {}
    nxt_circuit_idx = 0
    coord, distances = compute_distances(fname)
    for i, j, _ in distances:
        circuits, nxt_circuit_idx = connect(
            i, j, circuits, nb_elm_in_circuit, nxt_circuit_idx
        )
        if len(circuits) == len(coord) and len(set(circuits.values())) == 1:
            return coord[i][0] * coord[j][0]


if __name__ == "__main__":
    print(question_one("input.txt", max_nb_connections=1000))
    print(question_two("input.txt"))
