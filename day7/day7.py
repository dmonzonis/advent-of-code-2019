from itertools import permutations


def get_address_value(codes, n, mode=0):
    # mode 0: position mode
    # mode 1: immediate mode
    return codes[codes[n]] if mode == 0 else codes[n]


def get_mode(params, param):
    """Returns the mode for the nth param, where the param is in reading order (0 is the first param)"""
    if param >= len(params):
        return 0
    return params[-param - 1]


def process_opcode(pos, codes, inputs=None):
    """Process the given opcode and return the new position of the instruction pointer after the call.
    If a list of inputs is provided, the first element of the list will be used as input if opcode 3
    is found, and then popped from the list."""
    instruction = str(codes[pos])
    opcode = int(instruction[-2:])  # opcode is always the last 2 digits
    params = [int(x) for x in instruction[:-2]]
    num_params = 1
    output = None

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
        if inputs:
            inp = inputs.pop(0)
        else:
            inp = int(input("Input a number: "))
        codes[codes[pos + 1]] = inp
    elif opcode == 4:  # Output value
        output = get_address_value(codes, pos + 1, get_mode(params, 0))
        # print(output)
    elif opcode == 5 or opcode == 6:  # Jump if true (5) / false (6)
        num_params = 2
        val = get_address_value(codes, pos + 1, get_mode(params, 0))
        if (val != 0 and opcode == 5) or (val == 0 and opcode == 6):
            return get_address_value(codes, pos + 2, get_mode(params, 1)), None
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
        return None, None  # Terminate program

    # Move instruction poniter by this opcode + number of params
    # Also return output, if any
    return pos + num_params + 1, output


def run_program(codes, inputs):
    current = 0
    output = None
    while current < len(codes):
        current, aux = process_opcode(current, codes, inputs)
        if aux is not None:
            output = aux
        if current is None:
            # opcode 99 reached, halt program
            return output  # Return final output


def run_amplifiers(codes, phases):
    output = 0
    # Run amps sequentially
    for phase in phases:
        output = run_program(codes, [phase, output])
    return output


def find_highest_signal_combination(codes):
    phases = list(range(0, 5))
    highest = 0
    for perm in permutations(phases):
        output = run_amplifiers(codes, perm)
        highest = max(output, highest)
    return highest


def main():
    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split(',')]

    print(find_highest_signal_combination(data))


if __name__ == "__main__":
    main()
