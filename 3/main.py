directions = {
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0),
}

def read_input_for_wires():
    with open('input', 'r') as f:
        wire1 = f.readline().split(',')
        wire2 = f.readline().split(',')
        return wire1, wire2


def parse_input(wire_input):
    coordinates = [(0, 0)]
    current = coordinates[0]
    for item in wire_input:
        d = directions[item[:1]]
        count = int(item[1:])
        new_cord = (current[0] + count * d[0], current[1] + count * d[1])
        coordinates.append(new_cord)
        current = new_cord
    return coordinates


def generate_lines(coordinates):
    lines = []
    current_cord = None
    for item in coordinates:
        if not current_cord:
            current_cord = item
            continue
        lines.append((current_cord, item))
        current_cord = item
    return lines

def check_collision(w1, w2):
    a, b = w1
    c, d = w2
    det1 = 1 if (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0]) > 0 else 0
    det2 = 1 if (a[0] - d[0]) * (b[1] - d[1]) - (a[1] - d[1]) * (b[0] - d[0]) > 0 else 0
    det3 = 1 if (c[0] - a[0]) * (d[1] - a[1]) - (c[1] - a[1]) * (d[0] - a[0]) > 0 else 0
    det4 = 1 if (c[0] - b[0]) * (d[1] - b[1]) - (c[1] - b[1]) * (d[0] - b[0]) > 0 else 0
    if det1 != det2 and det3 != det4:
        x = 0
        y = 0
        if a[0] - b[0] == 0:
            x = a[0]
        elif a[1] - b[1] == 0:
            y = a[1]
        if c[0] - d[0] == 0:
            x = c[0]
        elif c[1] - d[1] == 0:
            y = d[1]
        return (x, y,)


def main():
    wire1, wire2 = read_input_for_wires()
    wire1_cor = parse_input(wire1)
    wire2_cor = parse_input(wire2)
    wire1_lines = generate_lines(wire1_cor)
    wire2_lines = generate_lines(wire2_cor)
    print(wire1_lines)
    print(wire2_lines)
    collisions = set()
    for w1 in wire1_lines:
        for w2 in wire2_lines:
            col_coord = check_collision(w1, w2)
            if col_coord:
                collisions.add(col_coord)
    distances = [abs(x) + abs(y) for x, y in collisions]
    print(min(distances))
    print(collisions)
    print(distances)


if __name__ == '__main__':
    main()
