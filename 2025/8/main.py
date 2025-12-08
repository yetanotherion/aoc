from functools import reduce


def read_input(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def question_one(fname, max_nb_connections=10):
    lines = read_input(fname)
    coord = []
    for l in lines:
        coord.append(tuple(int(x) for x in l.split(",")))
    distances = []
    for i, c in enumerate(coord):
        xi, yi, zi = c
        for j in range(i+1, len(coord)):
            xj, yj, zj = coord[j]
            distances.append((i, j, (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2))
    distances = sorted(distances, key=lambda x: x[2])
    circuits = {}
    nb_elm_in_circuit = {}
    nxt_circuit_idx = 0
    nb_connect = 0
    while nb_connect < max_nb_connections:
        i, j, e = distances.pop(0)
        #print(f"Handling {coord[i]} - {coord[j]}")
        if i in circuits and j in circuits:
            root_i = circuits[i]
            root_j = circuits[j]
            if root_i == root_j:
                #print(f"skip {coord[i]} - {coord[j]}")
                continue
            next_root = min(root_i, root_j)
            to_replace = max(root_i, root_j)
            #print(f"merging {to_replace} into {next_root}")
            nb_elm_in_circuit[next_root] += nb_elm_in_circuit[to_replace] - 1
            #print(f"merging {to_replace} into {next_root}= {nb_elm_in_circuit[next_root]} elts")
            nb_elm_in_circuit.pop(to_replace)
            new_circuits = {}
            for k, v in circuits.items():
                new_v = v
                if v == to_replace:
                    new_v = next_root
                new_circuits[k] = new_v
            circuits = new_circuits
            nb_connect += 1
            #print("circuits", circuits)
            continue
        if i not in circuits and j not in circuits:
            circuits[i] = nxt_circuit_idx
            circuits[j] = nxt_circuit_idx
            nb_elm_in_circuit[nxt_circuit_idx] = 2
            nxt_circuit_idx += 1
            #print(f"wire {coord[i]} - {coord[j]} into {nxt_circuit_idx - 1}. {nb_elm_in_circuit}")

        elif i not in circuits:
            circuits[i] = circuits[j]
            nb_elm_in_circuit[circuits[j]] += 1
            #print(f"wire {coord[i]} into {circuits[j]}. {nb_elm_in_circuit}")
        else:
            circuits[j] = circuits[i]
            nb_elm_in_circuit[circuits[i]] += 1
            #print(f"wire {coord[j]} into {circuits[i]}. {nb_elm_in_circuit}")
        #print("circuits", circuits)
        nb_connect += 1
    #print(nb_elm_in_circuit)
    #for k in nb_elm_in_circuit.keys():
        #print(f"{k}: {[i for i,v in circuits.items() if v == k]}")
    circuit_sizes = list(reversed(sorted(nb_elm_in_circuit.values())))
    top_three = circuit_sizes[:3]
    return reduce(lambda accum, x: accum * x, top_three)


if __name__ == "__main__":
    print(question_one("input.txt", max_nb_connections=1000))