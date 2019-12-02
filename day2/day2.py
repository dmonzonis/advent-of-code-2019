from copy import deepcopy


def process_opcode(pos, codes):
    opcode = codes[pos]
    if opcode == 1 or opcode == 2:
        # Assuming positions are well behaved (within bounds)
        val1 = codes[codes[pos + 1]]
        val2 = codes[codes[pos + 2]]
        result_pos = codes[pos + 3]
        if opcode == 1:
            codes[result_pos] = val1 + val2
        if opcode == 2:
            codes[result_pos] = val1 * val2
        return True
    if opcode == 99:
        return False  # Terminate program


def process_program(codes):
    current = 0
    while current < len(codes):
        if not process_opcode(current, codes):
            # opcode 99 reached, halt program
            return
        current += 4


def find_input_matching_output(output, codes):
    orig = deepcopy(codes)
    for noun in range(100):
        for verb in range(100):
            codes[1] = noun
            codes[2] = verb
            process_program(codes)
            if codes[0] == output:
                return noun, verb  # Match found
            # Reset program state
            codes = deepcopy(orig)


def main():
    with open("input.txt") as f:
        codes = [int(x) for x in f.read().split(',')]

    orig = deepcopy(codes)

    # Part 1
    codes[1] = 12
    codes[2] = 2
    process_program(codes)
    print(codes[0])

    # Part 2
    noun, verb = find_input_matching_output(19690720, orig)
    print(100 * noun + verb)


if __name__ == "__main__":
    main()
