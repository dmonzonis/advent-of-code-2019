from math import sqrt, atan2


EPSILON = 1e-4


def polar_coords(x, y):
    # Convert cartesian coordinates to polar
    return sqrt(x**2 + y**2), atan2(y, x)


def build_coordinate_map(asteroids):
    coordinates = []
    for y in range(len(asteroids)):
        for x in range(len(asteroids[y])):
            if asteroids[y][x] == '#':
                coordinates.append((x, y))
    return coordinates


def count_visible(coordinates, x, y):
    """Get the number of visible asteroids from coordinates (x, y)."""
    count = 0
    angles = []
    for (x1, y1) in coordinates:
        if (x1, y1) == (x, y):
            continue  # Same asteroid
        # Compute polar coords with (x, y) as the center
        dist, angle = polar_coords(x1 - x, y1 - y)
        # Check if a similar angle was already counted, if so only the closest one is visible
        new_angle = True
        for a in angles:
            if abs(a - angle) < EPSILON:
                new_angle = False
                break
        if new_angle:
            count += 1
            angles.append(angle)
    return count


def find_max_visible(coordinates):
    highest = 0
    for (x, y) in coordinates:
        count = count_visible(coordinates, x, y)
        highest = max(count, highest)
    return highest


def main():
    with open('input.txt') as f:
        asteroids = [list(line) for line in f.read().splitlines()]
    
    # Part 1
    coordinates = build_coordinate_map(asteroids)
    print(find_max_visible(coordinates))


if __name__ == "__main__":
    main()
