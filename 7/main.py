import itertools


class IntComputer:

    def __init__(self):
        self.i = 0
        self.opcode = [int(x) for x in self.read_input_and_split_by_comma()]
        self.inputs = []
        self.connected_to = None

    def signal_input(self, incoming):
        self.inputs.append(incoming)

    @staticmethod
    def read_input_and_split_by_comma():
        with open('input', 'r') as f:
            return f.read().split(',')

    @staticmethod
    def parse_instruction(instruction):
        operation = instruction % 100
        param_modes = [
            int(int(instruction / 100) / x) % 10
            for x
            in [1, 10, 100]
        ]
        return operation, param_modes

    def get_value(self, mode, i):
        return self.opcode[i] if mode else self.opcode[self.opcode[i]]

    def get_values(self, mode):
        num1 = self.get_value(mode[0], self.i+1)
        num2 = self.get_value(mode[1], self.i+2)
        return num1, num2

    def sum_op(self, param_mode):
        num1, num2 = self.get_values(param_mode)
        return num1 + num2

    def mul_op(self, param_mode):
        num1, num2 = self.get_values(param_mode)
        return num1 * num2

    def output(self, output_pos, data, param_modes=None):
        if data is None:
            out = output_pos if param_modes == 1 else self.opcode[output_pos]
            return out
        else:
            self.opcode[output_pos] = data

    def input_op(self, save_address):
        if not self.inputs:
            print("input:")
            res = int(input())
        else:
            res = self.inputs.pop(0)
        self.output(save_address, res)

    def jump_if_true(self, mode):
        return bool(self.get_value(mode[0], self.i+1))

    def compare_less_than(self, param_modes):
        val1 = self.get_value(param_modes[0], self.i+1)
        val2 = self.get_value(param_modes[1], self.i+2)
        if val1 < val2:
            self.output(self.opcode[self.i + 3], 1)
        else:
            self.output(self.opcode[self.i + 3], 0)

    def compare_equals(self, param_modes, i):
        val1 = self.get_value(param_modes[0], self.i + 1)
        val2 = self.get_value(param_modes[1], self.i + 2)
        if val1 == val2:
            self.output(self.opcode[self.i + 3], 1)
        else:
            self.output(self.opcode[self.i + 3], 0)

    def halted(self):
        return self.opcode[self.i] == 99

    def compute(self):
        while not self.halted():
            instruction = self.opcode[self.i]
            operation, param_modes = self.parse_instruction(instruction)
            if operation == 1:
                res = self.sum_op(param_modes)
                self.output(self.opcode[self.i + 3], res)
                self.i += 4
            elif operation == 2:
                res = self.mul_op(param_modes)
                self.output(self.opcode[self.i + 3], res)
                self.i += 4
            elif operation == 3:
                self.input_op(self.opcode[self.i+1])
                self.i += 2
            elif operation == 4:
                out = self.output(self.opcode[self.i + 1], None, param_modes[0])
                self.i += 2
                return out
            elif operation == 5:
                if self.jump_if_true(param_modes):
                    self.i = self.get_value(param_modes[1], self.i+2)
                else:
                    self.i += 3
            elif operation == 6:
                if not self.jump_if_true(param_modes):
                    self.i = self.get_value(param_modes[1], self.i+2)
                else:
                    self.i += 3
            elif operation == 7:
                self.compare_less_than(param_modes)
                self.i += 4
            elif operation == 8:
                self.compare_equals(param_modes)
                self.i += 4
            else:
                print("Something's wrong:", self.opcode[self.i])
                break


def generate_amplifiers_loop(phases):
    amplifiers_list = []
    for phase in phases:
        computer = IntComputer()
        computer.signal_input(phase)
        amplifiers_list.append(computer)
    return amplifiers_list


def amplify(phases):
    all_phase_perm = list(itertools.permutations(phases))
    final_outputs = []
    for phase_perm in all_phase_perm:
        amplifer_list = generate_amplifiers_loop(phase_perm)
        print("Current phase perm:", phase_perm)
        current_output = 0
        while not amplifer_list[-1].halted():
            for amplifier in amplifer_list:
                amplifier.signal_input(current_output)
                out = amplifier.compute()
                current_output = out
        print("Output", current_output)
        final_outputs.append(current_output)
    return max(final_outputs)


def main():
    out = amplify([5, 6, 7, 8, 9])
    print(out)


if __name__ == '__main__':
    main()
