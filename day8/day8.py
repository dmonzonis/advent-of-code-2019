import numpy as np


WIDTH = 25
HEIGHT = 6


def fill_matrix(data):
    num_layers = len(data) // (WIDTH * HEIGHT)
    return np.asarray(data).reshape(num_layers, HEIGHT, WIDTH)


def part1(matrix):
    # Find layer with most 0s
    layer = np.argmin([(matrix[l, :, :] == 0).sum() for l in range(0, matrix.shape[0])])
    # Count 1s and 2s in that layer and multiply them
    return (matrix[layer, :, :] == 1).sum() * (matrix[layer, :, :] == 2).sum()


def main():
    with open('input.txt') as f:
        data = [int(x) for x in list(f.read().strip())]
    
    # Part 1
    matrix = fill_matrix(data)
    print(part1(matrix))


if __name__ == "__main__":
    main()
