def compute_path(path):
    """Return a set with all the visited positions in (x, y) form"""
    current = [0, 0]
    visited = set()
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
        for step in range(1, steps + 1):
            current[pos] += multiplier
            visited.add(tuple(current))
    
    return visited


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_intersections(path1, path2):
    return compute_path(path1).intersection(compute_path(path2))


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
    
    closest = find_closest_point(find_intersections(paths[0], paths[1]))
    print(manhattan_distance(closest, (0, 0)))


if __name__ == "__main__":
    main()
