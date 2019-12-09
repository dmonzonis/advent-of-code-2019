from itertools import permutations


class IntcodeProgram(list):
    """Automatically growing list of codes used by the Intcode computer."""

    def __getitem__(self, key):
        if isinstance(key, int) and key >= len(self):
            return 0
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        # Grow list with 0s
        if isinstance(key, int) and key >= len(self):
            self.extend([0] * (key + 1 - len(self)))
        return super().__setitem__(key, value)


class Intcode:
    """Modelizes an Intcode computer which can load and run an Intcode program."""

    def __init__(self, program=None):
        self.codes = self.orig_codes = None
        self.restart()
        if program:
            self.load_program(program)

    def load_program(self, program):
        # Make a copy of the program
        self.codes = IntcodeProgram(program[:])
        self.orig_codes = self.codes[:]

    def restart(self):
        if self.orig_codes:
            self.codes = IntcodeProgram(self.orig_codes[:])
        self.instruction_ptr = 0
        self.halted = self.stopped = False
        self.stop_on_output = False
        self.input_stack = []
        self.outputs = []
        self.relative_base = 0

    def get_memory_address(self, n, mode=0):
        """Return the memory address depending on the value and mode."""
        # mode 0: position mode
        if mode == 0:
            return self.codes[n]
        # mode 1: immediate mode
        elif mode == 1:
            return n
        # mode 2: relative mode
        elif mode == 2:
            return self.relative_base + self.codes[n]
        else:
            raise ValueError

    def get_address_value(self, n, mode=0):
        return self.codes[self.get_memory_address(n, mode)]
    
    def set_address_value(self, n, val, mode=0):
        self.codes[self.get_memory_address(n, mode)] = val

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
            result_pos = self.get_memory_address(self.instruction_ptr + 3, self.get_mode(params, 2))
            if opcode == 1:
                self.codes[result_pos] = val1 + val2
            if opcode == 2:
                self.codes[result_pos] = val1 * val2
        elif opcode == 3:  # Get input and store into address
            if self.input_stack:
                inp = self.input_stack.pop(0)
            else:
                inp = int(input("Input a number: "))
            self.set_address_value(self.instruction_ptr + 1, inp, self.get_mode(params, 0))
        elif opcode == 4:  # Output value
            output = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            self.outputs.append(output)
            if self.stop_on_output:
                self.stopped = True
                self.instruction_ptr += num_params + 1
                return
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
            self.set_address_value(self.instruction_ptr + 3, int(val1 < val2), self.get_mode(params, 2))
        elif opcode == 8:  # Equals
            num_params = 3
            val1 = self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
            val2 = self.get_address_value(self.instruction_ptr + 2, self.get_mode(params, 1))
            self.set_address_value(self.instruction_ptr + 3, int(val1 == val2), self.get_mode(params, 2))
        elif opcode == 9:  # Update relative base
            self.relative_base += self.get_address_value(self.instruction_ptr + 1, self.get_mode(params, 0))
        elif opcode == 99:
            # Halt instruction; terminate program
            self.halted = True
            return

        # Move instruction poniter by this opcode + number of params
        self.instruction_ptr += num_params + 1

    def execute(self, inputs=None, stop_on_output=False):
        if not self.codes:
            print("No program loaded!")
            return
        if inputs:
            self.input_stack = inputs[:]
        self.stop_on_output = stop_on_output
        self.stopped = False
        while self.instruction_ptr < len(self.codes) and not self.halted and not self.stopped:
            self._process_instruction()


def main():
    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split(',')]

    # For part 1, give 1 as input
    # For part 2, give 2 as input
    test_comp = Intcode(data)
    test_comp.execute()
    print(test_comp.outputs[0])


if __name__ == "__main__":
    main()
