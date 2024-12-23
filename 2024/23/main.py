def read_lines(fname="input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def parse_input(lines):
    res = {}
    for l in lines:
        n1, n2 = l.split("-")
        res.setdefault(n1, set([])).add(n2)
        res.setdefault(n2, set([])).add(n1)
    return res


def question_one(graph):
    clusters = set()
    for n, edges in graph.items():
        for n2 in edges:
            next_n2 = graph[n2]
            for n3 in next_n2:
                if n3 in edges:
                    normalised = tuple(sorted([n, n2, n3]))
                    if normalised not in clusters:
                        clusters.add(normalised)
    with_t = [
        (n1, n2, n3)
        for (n1, n2, n3) in clusters
        if any(x[0] == "t" for x in (n1, n2, n3))
    ]
    return len(with_t)


def question_two(graph):
    max_cluster = []
    to_see = [[n] for n in graph.keys()]
    seen = set()
    while to_see:
        curr = to_see.pop()
        if tuple(sorted(curr)) in seen:
            continue
        if len(curr) > len(max_cluster):
            max_cluster = curr
        last = curr[-1]
        for o in graph[last]:
            if all(o in graph[n] for n in curr):
                new_curr = curr[:]
                new_curr.append(o)
                to_see.append(new_curr)
        seen.add(tuple(sorted(curr)))
    return ",".join(sorted(max_cluster))


if __name__ == "__main__":
    raw_input = read_lines(fname="input.txt")
    graph = parse_input(raw_input)
    print(question_one(graph))
    print(question_two(graph))
