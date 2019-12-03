DIRECTIONS = {
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
        d = DIRECTIONS[item[:1]]
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


def find_det_sign(a, b, c):
    det = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
    return 1 if det > 0 else 0


def check_collision(w1, w2):
    a, b = w1
    c, d = w2
    det1 = find_det_sign(a, b, c)
    det2 = find_det_sign(a, b, d)
    det3 = find_det_sign(c, d, a)
    det4 = find_det_sign(c, d, b)
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
        return x, y


def check_distance(lines1, lines2, col_coord):
    len1 = 0
    len2 = 0
    for line in lines1:
        a, b = line
        len1 += abs(a[0] - b[0] + a[1] - b[1])
    for line in lines2:
        a, b = line
        len2 += abs(a[0] - b[0] + a[1] - b[1])
    last_point1 = lines1[-1][1]
    last_point2 = lines2[-1][1]
    len1 += abs(last_point1[0] - col_coord[0] + last_point1[1] - col_coord[1])
    len2 += abs(last_point2[0] - col_coord[0] + last_point2[1] - col_coord[1])
    return len1 + len2


def main():
    wire1, wire2 = read_input_for_wires()
    wire1_cor = parse_input(wire1)
    wire2_cor = parse_input(wire2)
    wire1_lines = generate_lines(wire1_cor)
    wire2_lines = generate_lines(wire2_cor)
    collisions = set()
    distance = []
    i = 0
    for w1 in wire1_lines:
        i += 1
        j = 0
        for w2 in wire2_lines:
            j += 1
            col_coord = check_collision(w1, w2)
            if col_coord:
                collisions.add(col_coord)
                print(w1, w2, col_coord)
                distance.append(check_distance(wire1_lines[:i-1], wire2_lines[:j-1], col_coord))
    print(min(distance))


if __name__ == '__main__':
    main()
