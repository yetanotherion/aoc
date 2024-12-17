from heapq import heappop, heappush

UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)


def read_input(fname="small_input.txt"):
    with open(fname) as f:
        return [l[:-1] for l in f.readlines()]


def find(game_input, target="S"):
    for i, l in enumerate(game_input):
        for j, e in enumerate(l):
            if e == target:
                return (i, j)


def dijkstra(grid):
    end_i, end_j = find(grid, target="E")
    start_i, start_j = find(grid, target="S")
    target = (start_i, start_j, RIGHT)
    distance = {}
    dirs = [UP, RIGHT, LEFT, DOWN]
    h = []
    prev = {}
    visited = set()
    for i, l in enumerate(grid):
        for j, e in enumerate(l):
            for curr_dir in dirs:
                if e != "#" and (i, j) != (end_i, end_j):
                    distance[(i, j, curr_dir)] = float("inf")
                    heappush(h, (float("inf"), (i, j, curr_dir)))

    for curr_dir in dirs:
        distance[(end_i, end_j, curr_dir)] = 0
        heappush(h, (0, (end_i, end_j, curr_dir)))

    def generate_rotations(curr_dir):
        if curr_dir == UP:
            return [(RIGHT, 1000), (LEFT, 1000), (DOWN, 2000)]
        if curr_dir == DOWN:
            return [(RIGHT, 1000), (LEFT, 1000), (UP, 2000)]
        if curr_dir == LEFT:
            return [(UP, 1000), (DOWN, 1000), (RIGHT, 2000)]
        if curr_dir == RIGHT:
            return [(UP, 1000), (DOWN, 1000), (LEFT, 2000)]

    def generate_neighbors(curr_i, curr_j, curr_dir):
        res = [(curr_i - curr_dir[0], curr_j - curr_dir[1], curr_dir, 1)]
        for rot, weight in generate_rotations(curr_dir):
            res.append((curr_i, curr_j, rot, weight))
        return res

    while h:
        curr_node_distance, curr_node = heappop(h)
        if curr_node in visited:
            continue
        visited.add(curr_node)
        if curr_node == target:
            break
        curr_i, curr_j, curr_dir = curr_node
        for neighbor in generate_neighbors(curr_i, curr_j, curr_dir):
            next_i, next_j, next_dir, next_distance = neighbor
            neighbor_v = (next_i, next_j, next_dir)
            if neighbor_v not in distance:
                continue
            new_distance = curr_node_distance + next_distance
            if new_distance == distance[neighbor_v]:
                prev.setdefault(neighbor_v, set([])).add((curr_i, curr_j, curr_dir))
            if new_distance < distance[neighbor_v]:
                prev[neighbor_v] = set([(curr_i, curr_j, curr_dir)])
                distance[neighbor_v] = new_distance
                heappush(h, (new_distance, neighbor_v))
    min_distance = distance[target]
    all_nodes = set()
    to_browse = [target]
    seen = set()
    while to_browse:
        curr = to_browse.pop()
        if curr[0] == end_i and curr[1] == end_j:
            all_nodes.add((end_i, end_j))
            continue
        if curr in seen:
            continue
        all_nodes.add((curr[0], curr[1]))
        for x in prev[curr]:
            to_browse.append(x)
        seen.add(curr)

    return min_distance, len(all_nodes)


def question_one(grid):
    return dijkstra(grid)[0]


def question_two(grid):
    return dijkstra(grid)[1]


if __name__ == "__main__":
    game_input = read_input(fname="input.txt")
    print(question_one(game_input))
    print(question_two(game_input))
