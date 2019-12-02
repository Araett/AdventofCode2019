import math


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def read_input_and_split_lines():
    with open('input', 'r') as f:
        return f.read().splitlines()


def find_fuel_required(mass):
    return round_down(mass / 3) - 2


def main():
    data = read_input_and_split_lines()
    s = 0
    for item in data:
        s += find_fuel_required(int(item))
    print(s)


if __name__ == '__main__':
    main()
