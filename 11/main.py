from operator import itemgetter


class IntComputer:

    def __init__(self):
        self.i = 0
        inp = self.read_input_and_split_by_comma()
        self.opcode = {i: int(x) for i, x in zip(range(0, len(inp)), inp)}
        self.inputs = []
        self.relative_base = 0

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

    def get_address(self, mode, i):
        if mode == 0:
            address = self.opcode[i]
        elif mode == 1:
            address = i
        else:
            address = self.opcode[i] + self.relative_base
        return address

    def get_value(self, mode, i):
        address = self.get_address(mode, i)
        return self.opcode.get(address, 0)

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

    def output(self, i, data, param_modes=0):
        output_pos = self.get_address(param_modes, i)
        if data is None:
            out = self.opcode[output_pos]
            return out
        else:
            self.opcode[output_pos] = data

    def input_op(self, mode):
        if not self.inputs:
            print("input:")
            res = int(input())
        else:
            res = self.inputs.pop(0)
        self.output(self.i+1, res, mode)

    def jump_if_true(self, mode):
        return bool(self.get_value(mode[0], self.i+1))

    def compare_less_than(self, param_modes):
        val1 = self.get_value(param_modes[0], self.i+1)
        val2 = self.get_value(param_modes[1], self.i+2)
        if val1 < val2:
            self.output(self.i + 3, 1, param_modes[2])
        else:
            self.output(self.i + 3, 0, param_modes[2])

    def compare_equals(self, param_modes):
        val1 = self.get_value(param_modes[0], self.i + 1)
        val2 = self.get_value(param_modes[1], self.i + 2)
        if val1 == val2:
            self.output(self.i + 3, 1, param_modes[2])
        else:
            self.output(self.i + 3, 0, param_modes[2])

    def halted(self):
        return self.opcode[self.i] == 99

    def compute(self):
        while not self.halted():
            instruction = self.opcode[self.i]
            operation, param_modes = self.parse_instruction(instruction)
            if operation == 1:
                res = self.sum_op(param_modes)
                self.output(self.i+3, res, param_modes[2])
                self.i += 4
            elif operation == 2:
                res = self.mul_op(param_modes)
                self.output(self.i+3, res, param_modes[2])
                self.i += 4
            elif operation == 3:
                # self.input_op(self.opcode[self.i+1])
                self.input_op(param_modes[0])
                self.i += 2
            elif operation == 4:
                out = self.output(self.i+1, None, param_modes[0])
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
            elif operation == 9:
                self.relative_base += self.get_value(param_modes[0], self.i+1)
                self.i += 2
            else:
                print("Something's wrong:", self.opcode[self.i])
                break


class Robot:

    def __init__(self, grid: dict):
        self.central_brains = IntComputer()
        self.grid = grid
        self.current_pos = [0, 0]
        self.direction = (0, 1)

    def is_finished(self):
        return self.central_brains.halted()

    def get_current_pos_color(self):
        return self.grid.get(tuple(self.current_pos), 0)

    def get_instructions(self, count):
        output = []
        for n in range(0, count):
            out = self.central_brains.compute()
            if out is None:
                return
            output.append(out)
        return tuple(output)

    def rotate(self, direction):
        if direction == 0:
            direction = -1
        self.direction = (
            self.direction[1] * direction * 1,
            self.direction[0] * direction * -1,
        )

    def paint(self, color):
        self.grid[tuple(self.current_pos)] = color

    def move(self):
        self.current_pos[0] += self.direction[0]
        self.current_pos[1] += self.direction[1]

    def draw(self):
        tile_color = self.get_current_pos_color()
        self.central_brains.signal_input(tile_color)
        instructions = self.get_instructions(2)
        if not instructions:
            return
        self.paint(instructions[0])
        self.rotate(instructions[1])
        self.move()


def draw_grid(grid):
    used_coordinates = grid.keys()
    min_x = min(used_coordinates, key=itemgetter(0))[0]
    max_x = max(used_coordinates, key=itemgetter(0))[0]
    min_y = min(used_coordinates, key=itemgetter(1))[1]
    max_y = max(used_coordinates, key=itemgetter(1))[1]
    for y in range(max_y, min_y-1, -1):
        x_str = ""
        for x in range(min_x, max_x):
            x_str += str(grid.get((x, y), 0))
        print(x_str.replace('0', '.'))


def main():
    grid = {(0, 0): 1}
    robot = Robot(grid)
    while not robot.is_finished():
        robot.draw()
    draw_grid(grid)


if __name__ == '__main__':
    main()
