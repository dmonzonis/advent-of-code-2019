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


def decode_image(matrix):
    # There's probably a more elegant and efficient way to do this with numpy but fuck that
    image = np.ndarray((matrix.shape[1], matrix.shape[2]), dtype=int)
    image.fill(-1)
    
    for layer in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            for x in range(matrix.shape[2]):
                if image[y, x] == -1 and matrix[layer, y, x] != 2:
                    image[y, x] = matrix[layer, y, x]
    return image


def print_image(image):
    buffer = ""
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            buffer += "." if image[y, x] == 0 else "#"
        print(buffer)
        buffer = ""


def main():
    with open('input.txt') as f:
        data = [int(x) for x in list(f.read().strip())]
    
    # Part 1
    matrix = fill_matrix(data)
    print(part1(matrix))

    # Part 2
    print_image(decode_image(matrix))


if __name__ == "__main__":
    main()
