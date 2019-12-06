def get_address_value(codes, n, mode=0):
    # mode 0: position mode
    # mode 1: immediate mode
    return codes[codes[n]] if mode == 0 else codes[n]


def get_mode(params, param):
    """Returns the mode for the nth param, where the param is in reading order (0 is the first param)"""
    if param >= len(params):
        return 0
    return params[-param - 1]


def process_opcode(pos, codes):
    """Process the given opcode and return the new position of the instruction pointer after the call."""
    instruction = str(codes[pos])
    opcode = int(instruction[-2:])  # opcode is always the last 2 digits
    params = [int(x) for x in instruction[:-2]]
    num_params = 1

    if opcode == 1 or opcode == 2:  # Sum or multiply and store result into address
        num_params = 3
        val1 = get_address_value(codes, pos + 1, get_mode(params, 0))
        val2 = get_address_value(codes, pos + 2, get_mode(params, 1))
        result_pos = codes[pos + 3]
        if opcode == 1:
            codes[result_pos] = val1 + val2
        if opcode == 2:
            codes[result_pos] = val1 * val2
    elif opcode == 3:  # Get input and store into address
        inp = int(input("Input a number: "))
        codes[codes[pos + 1]] = inp
    elif opcode == 4:  # Output value
        print(get_address_value(codes, pos + 1, get_mode(params, 0)))
    elif opcode == 5 or opcode == 6:  # Jump if true (5) / false (6)
        num_params = 2
        val = get_address_value(codes, pos + 1, get_mode(params, 0))
        if (val != 0 and opcode == 5) or (val == 0 and opcode == 6):
            return get_address_value(codes, pos + 2, get_mode(params, 1))
    elif opcode == 7:  # Less than
        num_params = 3
        val1 = get_address_value(codes, pos + 1, get_mode(params, 0))
        val2 = get_address_value(codes, pos + 2, get_mode(params, 1))
        codes[codes[pos + 3]] = int(val1 < val2)
    elif opcode == 8:  # Equals
        num_params = 3
        val1 = get_address_value(codes, pos + 1, get_mode(params, 0))
        val2 = get_address_value(codes, pos + 2, get_mode(params, 1))
        codes[codes[pos + 3]] = int(val1 == val2)
    elif opcode == 99:
        return None  # Terminate program

    # Move instruction poniter by this opcode + number of params
    return pos + num_params + 1


def run_program(codes):
    current = 0
    while current < len(codes):
        current = process_opcode(current, codes)
        if current is None:
            # opcode 99 reached, halt program
            return


def main():
    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split(',')]

    # For part 1, provide 1 as input
    # For part 2, provide 5 as input
    run_program(data)


if __name__ == "__main__":
    main()
