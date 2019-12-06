def read_input_and_split_by_comma():
    with open('input', 'r') as f:
        return f.read().split(',')


def get_value(opcode, mode, i):
    return opcode[i] if mode else opcode[opcode[i]]


def get_values(opcode, mode, i):
    num1 = get_value(opcode, mode[0], i+1)
    num2 = get_value(opcode, mode[1], i+2)
    return num1, num2


def sum_op(opcode, param_mode, i):
    num1, num2 = get_values(opcode, param_mode, i)
    return num1 + num2


def mul_op(opcode, param_mode, i):
    num1, num2 = get_values(opcode, param_mode, i)
    return num1 * num2


def output(opcode, output_pos, data, param_modes=None):
    if data is None:
        out = output_pos if param_modes == 1 else opcode[output_pos]
        print("output:", out)
    else:
        opcode[output_pos] = data


def input_op(opcode, save_address):
    print("input:")
    res = int(input())
    output(opcode, save_address, res)


def parse_instruction(instruction):
    operation = instruction % 100
    param_modes = [
        int(int(instruction / 100) / x) % 10
        for x
        in [1, 10, 100]
    ]
    return operation, param_modes


def jump_if_true(opcode, mode, i):
    return bool(get_value(opcode, mode[0], i+1))


def compare_less_than(opcode, param_modes, i):
    val1 = get_value(opcode, param_modes[0], i+1)
    val2 = get_value(opcode, param_modes[1], i+2)
    if val1 < val2:
        output(opcode, opcode[i + 3], 1)
    else:
        output(opcode, opcode[i + 3], 0)


def compare_equals(opcode, param_modes, i):
    val1 = get_value(opcode, param_modes[0], i + 1)
    val2 = get_value(opcode, param_modes[1], i + 2)
    if val1 == val2:
        output(opcode, opcode[i+3], 1)
    else:
        output(opcode, opcode[i+3], 0)


def main():
    opcode = [int(x) for x in read_input_and_split_by_comma()]
    i = 0
    while opcode[i] != 99:
        operation, param_modes = parse_instruction(opcode[i])
        if operation == 1:
            res = sum_op(opcode, param_modes, i)
            output(opcode, opcode[i + 3], res)
            i += 4
        elif operation == 2:
            res = mul_op(opcode, param_modes, i)
            output(opcode, opcode[i + 3], res)
            i += 4
        elif operation == 3:
            input_op(opcode, opcode[i+1])
            i += 2
        elif operation == 4:
            output(opcode, opcode[i + 1], None, param_modes[0])
            i += 2
        elif operation == 5:
            if jump_if_true(opcode, param_modes, i):
                i = get_value(opcode, param_modes[1], i+2)
            else:
                i += 3
        elif operation == 6:
            if not jump_if_true(opcode, param_modes, i):
                i = get_value(opcode, param_modes[1], i+2)
            else:
                i += 3
        elif operation == 7:
            compare_less_than(opcode, param_modes, i)
            i += 4
        elif operation == 8:
            compare_equals(opcode, param_modes, i)
            i += 4
        else:
            print("Something's wrong:", opcode[i])
            break


if __name__ == '__main__':
    main()
