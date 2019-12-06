def read_input_and_split_by_comma():
    with open('input', 'r') as f:
        return f.read().split(',')


def sum_op(opcode, pos1, pos2):
    print("sum", opcode[pos1], opcode[pos2])
    return opcode[pos1] + opcode[pos2]


def mul_op(opcode, pos1, pos2):
    print("mul", opcode[pos1], opcode[pos2])
    return opcode[pos1] * opcode[pos2]


def output(opcode, output_pos, data):
    print("ouput", output_pos, data)
    opcode[output_pos] = data


def main():
    opcode = [int(x) for x in read_input_and_split_by_comma()]
    i = 0
    opcode[1] = 12
    opcode[2] = 2
    while opcode[i] != 99:
        res = 0
        if opcode[i] == 1:
            res = sum_op(opcode, opcode[i+1], opcode[i+2])
        elif opcode[i] == 2:
            res = mul_op(opcode, opcode[i+1], opcode[i+2])
        else:
            break
        output(opcode, opcode[i+3], res)
        i += 4
    print(opcode[0])



if __name__ == '__main__':
    print(main())
