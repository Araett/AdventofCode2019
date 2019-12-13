from operator import itemgetter
from pynput.keyboard import Key, Listener
import sys
import time


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


class ArcadeCabinet:

    def __init__(self):
        self.loading = None
        self.grid = {}
        self.central = IntComputer()
        intab = '01234'
        outtab = '.+#_o'
        self.trantab = str.maketrans(intab, outtab)
        self.current_input = 1
        self.frames_per_second = 60
        self.score = 0
        self.ball_present = False
        self.pad_present = False

    def give_current_input(self):
        return self.current_input

    def get_instructions(self, count):
        output = []
        for n in range(0, count):
            out = self.central.compute()
            if out is None:
                return
            output.append(out)
        return tuple(output)

    def put_object(self, x, y, obj):
        self.grid[(x, y)] = obj

    def draw_grid(self):
        used_coordinates = self.grid.keys()
        min_x = min(used_coordinates, key=itemgetter(0))[0]
        max_x = max(used_coordinates, key=itemgetter(0))[0]
        min_y = min(used_coordinates, key=itemgetter(1))[1]
        max_y = max(used_coordinates, key=itemgetter(1))[1]
        for y in range(min_y, max_y + 1):
            x_str = ""
            for x in range(min_x, max_x + 1):
                x_str += str(self.grid.get((x, y), '.'))
            print(x_str.translate(self.trantab))

    def load(self):
        while True:
            draw_inst = self.get_instructions(3)
            if draw_inst[0] == -1:
                return
            self.put_object(*draw_inst)

    def render_screen(self):
        while True:
            draw_inst = self.get_instructions(3)
            if draw_inst is None:
                return
            elif draw_inst[0] == -1 and draw_inst[1] == 0:
                self.score = draw_inst[2]
                print(draw_inst)
            self.put_object(*draw_inst)
            if draw_inst[2] == 4:
                break
            # if self.ball_and_pad_present():
            #     print('break')
            #     break
        print('\033c')
        self.draw_grid()

    def blocks_exist(self):
        return list(self.grid.values()).count(2) > 0

    def ball_and_pad_present(self):
        ball = list(self.grid.values()).count(3)
        pad = list(self.grid.values()).count(4)
        # print(ball, pad)
        return ball & pad

    def determine_input(self):
        if self.ball_and_pad_present():
            ball_x = list(self.grid.keys())[list(self.grid.values()).index(4)][0]
            pad_x = list(self.grid.keys())[list(self.grid.values()).index(3)][0]
            joy_input = 0
            if ball_x > pad_x:
                joy_input = 1
            if ball_x < pad_x:
                joy_input = -1
            if len(self.central.inputs) == 0:
                self.central.signal_input(joy_input)

    def play_game(self):
        self.central.opcode[0] = 2
        self.load()
        self.draw_grid()
        self.central.signal_input(1)
        while True:
            time.sleep(1 / self.frames_per_second)
            if self.blocks_exist():
                self.render_screen()
                self.determine_input()

            else:
                print(self.score)


def main():
    arcade = ArcadeCabinet()
    print(arcade.play_game())





if __name__ == '__main__':
    main()
