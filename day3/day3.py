def compute_path(path):
    """Return a set with all the visited positions in (x, y) form"""
    current = [0, 0]
    visited = {}
    total_steps = 0
    for move in path:
        if move[0] == 'U':
            pos = 1
            multiplier = 1
        elif move[0] == 'D':
            pos = 1
            multiplier = -1
        elif move[0] == 'R':
            pos = 0
            multiplier = 1
        else:  # 'L'
            pos = 0
            multiplier = -1

        steps = int(move[1:])
        for _ in range(1, steps + 1):
            current[pos] += multiplier
            total_steps += 1
            current_tuple = tuple(current)
            if current_tuple not in visited:
                visited[current_tuple] = total_steps

    return visited


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_intersections(path1, path2):
    """Return a dictionary with the intersecting points as keys and the total steps
    to reach that intersection by both paths, as given by the compute_path method"""
    visited1 = compute_path(path1)
    visited2 = compute_path(path2)
    intersections = set(visited1.keys()).intersection(set(visited2.keys()))
    result = {}
    # Construct the dictionary of intersection: total steps
    for point in intersections:
        result[point] = visited1[point] + visited2[point]
    return result


def find_closest_point(points, origin=(0, 0)):
    closest = None
    closest_distance = float('inf')
    for point in points:
        distance = manhattan_distance(point, origin)
        if distance < closest_distance:
            closest = point
            closest_distance = distance
    return closest


def main():
    with open("input.txt") as f:
        paths = [path.split(',') for path in f.read().splitlines()]

    # Part 1
    intersection_dict = find_intersections(paths[0], paths[1])
    closest = find_closest_point(intersection_dict.keys())
    print(manhattan_distance(closest, (0, 0)))

    # Part 2
    print(min(intersection_dict.values()))


if __name__ == "__main__":
    main()
