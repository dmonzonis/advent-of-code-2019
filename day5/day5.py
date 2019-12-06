def add_trailing_zeros(params, n):
    return [0] * (n - len(params)) + params


def get_address_value(codes, n, mode=0):
    # mode 0: position mode
    # mode 1: immediate mode
    return codes[codes[n]] if mode == 0 else codes[n]


def process_opcode(pos, codes):
    """Process the given opcode and return the instruction pointer shift required after the call."""
    instruction = str(codes[pos])
    opcode = int(instruction[-2:])  # opcode is always the last 2 digits
    params = [int(x) for x in instruction[:-2]]
    num_params = 1

    if opcode == 1 or opcode == 2:
        num_params = 3
        params = add_trailing_zeros(params, num_params)
        val1 = get_address_value(codes, pos + 1, params[-1])
        val2 = get_address_value(codes, pos + 2, params[-2])
        result_pos = codes[pos + 3]
        if opcode == 1:
            codes[result_pos] = val1 + val2
        if opcode == 2:
            codes[result_pos] = val1 * val2
    elif opcode == 3:
        # TODO: Error handling
        inp = int(input("Input a number: "))
        codes[codes[pos + 1]] = inp
    elif opcode == 4:  # Output value
        params = add_trailing_zeros(params, num_params)
        print(get_address_value(codes, pos + 1, params[-1]))
    elif opcode == 99:
        return None  # Terminate program

    # Move instruction poniter by this opcode + number of params
    return num_params + 1


def run_program(codes):
    current = 0
    while current < len(codes):
        shift = process_opcode(current, codes)
        if shift is None:
            # opcode 99 reached, halt program
            return
        current += shift


def main():
    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split(',')]

    # Part 1
    run_program(data)


if __name__ == "__main__":
    main()
