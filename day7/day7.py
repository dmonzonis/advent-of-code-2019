from itertools import permutations


class Intcode:
    """Modelizes an Intcode computer which can load and run an Intcode program."""
    def __init__(self, program=None):
        self.codes = self.orig_codes = None
        self.input_stack = []
        if program:
            self.load_program(program)
        self.outputs = []
        self.instruction_ptr = 0
        self.halted = False
    
    def load_program(self, program):
        # Make a copy of the program
        self.codes = program[:]
        self.orig_codes = self.codes[:]
    
    def restart(self):
        if self.orig_codes:
            self.codes = self.orig_codes[:]
        self.instruction_ptr = 0
        self.halted = False
        self.input_stack = []
        self.outputs = []

    def get_address_value(self, n, mode=0):
        # mode 0: position mode
        # mode 1: immediate mode
        return self.codes[self.codes[n]] if mode == 0 else self.codes[n]

    def get_mode(self, params, param):
        """Return the mode for the nth param, where the param is in reading order (0 is the first param)"""
        if param >= len(params):
            return 0
        return params[-param - 1]

    def _process_instruction(self):
        """Process the next instruction, given by the position of the instruction pointer."""
        instruction = str(self.codes[self.instruction_ptr])
        opcode = int(instruction[-2:])
        params = [int(x) for x in instruction[:-2]]
        num_params = 1

        if opcode == 1 or opcode == 2:
            # Sum or multiply and store result into address
            num_params = 3
            val1 = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            val2 = self.get_address_value(self.instruction_ptr + 2, self.get_mode(params, 1))
            result_pos = self.codes[self.instruction_ptr + 3]
            if opcode == 1:
                self.codes[result_pos] = val1 + val2
            if opcode == 2:
                self.codes[result_pos] = val1 * val2
        elif opcode == 3:  # Get input and store into address
            if self.input_stack:
                inp = self.input_stack.pop(0)
            else:
                inp = int(input("Input a number: "))
            self.codes[self.codes[self.instruction_ptr + 1]] = inp
        elif opcode == 4:  # Output value
            output = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            self.outputs.append(output)
            # print(output)
        elif opcode == 5 or opcode == 6:  # Jump if true (5) / false (6)
            num_params = 2
            val = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            if (val != 0 and opcode == 5) or (val == 0 and opcode == 6):
                self.instruction_ptr = self.get_address_value(self.instruction_ptr + 2, self.get_mode(params, 1))
                return
        elif opcode == 7:  # Less than
            num_params = 3
            val1 = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            val2 = self.get_address_value(self.instruction_ptr + 2, self.get_mode(params, 1))
            self.codes[self.codes[self.instruction_ptr + 3]] = int(val1 < val2)
        elif opcode == 8:  # Equals
            num_params = 3
            val1 = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            val2 = self.get_address_value(self.instruction_ptr + 2, self.get_mode(params, 1))
            self.codes[self.codes[self.instruction_ptr + 3]] = int(val1 == val2)
        elif opcode == 99:
            # Halt instruction; terminate program
            self.halted = True
            return

        # Move instruction poniter by this opcode + number of params
        self.instruction_ptr += num_params + 1
    
    def execute(self, inputs=None):
        if not self.codes:
            print("No program loaded!")
            return
        if inputs:
            self.input_stack = inputs[:]
        self.instruction_ptr = 0
        while self.instruction_ptr < len(self.codes) and not self.halted:
            self._process_instruction()
    
    def pop_output(self):
        if self.outputs:
            return self.outputs.pop(0)


def run_amplifiers(codes, phases):
    output = 0
    # Run amps sequentially
    for phase in phases:
        amp = Intcode(codes)
        amp.execute([phase, output])
        output = amp.pop_output()
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

    # Part 1
    print(find_highest_signal_combination(data))
    

if __name__ == "__main__":
    main()
