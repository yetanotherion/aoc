def read_lines(fname):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines() if l[:-1]]


def all_paths(
    graph,
    memory=None,
    start="you",
    out="out",
    skip=(),
):
    if memory is None:
        memory = {}
    if start == out:
        return 1
    next = graph.get(start, [])
    for n in next:
        if n not in memory:
            memory[n] = all_paths(graph, memory=memory, start=n, out=out, skip=skip)
    return sum(memory[n] for n in next)


def load_graph(fname):
    lines = read_lines(fname)
    graph = {}
    for l in lines:
        origin, destination = l.split(":")
        destinations = [x.strip() for x in destination.split(" ") if x.strip()]
        graph[origin] = destinations
    return graph


def question_one(fname):
    graph = load_graph(fname)
    return all_paths(graph, start="you")


def question_two(fname):
    graph = load_graph(fname)
    res_svr_fft = all_paths(graph, start="svr", out="fft", skip=("dac", "out"))
    res_fft_dac = all_paths(graph, start="fft", out="dac", skip=("svr", "out"))
    res_dac_fft = all_paths(graph, start="dac", out="fft", skip=("svr", "out"))
    res_svr_dac = all_paths(graph, start="svr", out="dac", skip=("fft", "out"))
    res_fft_out = all_paths(graph, start="fft", out="out", skip=("svr", "dac"))
    res_dac_out = all_paths(graph, start="dac", out="out", skip=("svr", "fft"))
    return (
        res_svr_fft * res_fft_dac * res_dac_out
        + res_svr_dac * res_dac_fft * res_fft_out
    )


if __name__ == "__main__":
    print(question_one("input.txt"))
    print(question_two("input.txt"))
