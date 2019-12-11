import itertools
import math


def manhattan_distance(point1, point2):
    return abs(point1[0] - point1[1] + point2[0] + point2[1])


def calculate_distances(asteroid_spaces, coordinate):
    return [
        (ast_coordinate, manhattan_distance(coordinate, ast_coordinate))
        for ast_coordinate
        in asteroid_spaces.keys()
    ]


def print_grid(visability, x_max, y_max):
    for y in range(0, y_max):
        x_str = ""
        for x in range(0, x_max):
            x_str += str(visability.get((x, y), '-'))
        print(x_str)
    print()


def find_direction(coordinate, asteroid_coords):
    x = asteroid_coords[0] - coordinate[0]
    y = asteroid_coords[1] - coordinate[1]
    divider = math.gcd(abs(x), abs(y))
    return x/divider, y/divider


def check_visability(visability, asteroid_spaces):
    asteroid_count = []
    for asteroid in asteroid_spaces.keys():
        if visability[asteroid] == '-':
            asteroid_count.append(asteroid)
    return asteroid_count


def asteroid_visability(asteroid_spaces, coordinate, x_max, y_max):
    permuations = list(itertools.product(*[range(0, x_max), range(0, y_max)]))
    visability = {(x, y): 1 for (x, y) in permuations}
    visability[coordinate] = "S"
    asteroid_distances = calculate_distances(asteroid_spaces, coordinate)
    asteroid_distances.sort(key=lambda x: x[1])
    for asteroid in asteroid_distances:
        asteroid_coords = asteroid[0]
        if visability[asteroid_coords] == 1:
            visability[asteroid_coords] = '-'
            direction = find_direction(coordinate, asteroid_coords)
            current_x, current_y = asteroid_coords
            while True:
                current_x += direction[0]
                current_y += direction[1]
                if current_x > x_max or current_x < 0:
                    break
                if current_y > y_max or current_y < 0:
                    break
                visability[(current_x, current_y)] = 0
    visable_asteroids = check_visability(visability, asteroid_spaces)
    # print_grid(visability, x_max, y_max)
    return visable_asteroids


def parse_input(asteroid_input):
    asteroid_spaces = {}
    for y in range(0, len(asteroid_input)):
        for x in range(0, len(asteroid_input[y])):
            if asteroid_input[y][x] == '#':
                asteroid_spaces[(x, y)] = -1
    return asteroid_spaces


def read_input():
    with open("input", "r") as f:
        return f.read().splitlines()


def remove_asteroids(visable_asteroids, asteroid_spaces):
    for asteroid in visable_asteroids:
        asteroid_spaces.pop(asteroid)


def find_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def determine_order(best_asteroid, order, visable_asteroids):
    asteroid_sines = []
    for asteroids in visable_asteroids:
        r = find_distance(best_asteroid, asteroids)
        x = asteroids[0] - best_asteroid[0]
        y = -1*(asteroids[1] - best_asteroid[1])
        sin = abs(x/r)
        cos = abs(y/r)
        angle = None
        if x >= 0 and y > 0:
            angle = sin
        if x > 0 and y <= 0:
            angle = 1 + cos
        if x <= 0 and y < 0:
            angle = 2 + sin
        if x < 0 and y >= 0:
            angle = 3 + cos
        # cos = x/r
        # tan = y/x if x !=0 else None
        asteroid_sines.append((asteroids, angle))
    asteroid_sines.sort(key=lambda x: x[1])
    i = len(order)
    for asteroid in asteroid_sines:
        order[i] = asteroid[0]
        i += 1
    return order

# (2,0) 0
# (4,2) 1
# (2,4) 2
# (0,2) 3


def main():
    import time
    now = time.time()
    asteroid_input = read_input()
    y_max = len(asteroid_input)
    x_max = len(asteroid_input[0])
    asteroid_spaces = parse_input(asteroid_input)
    counter = {}
    for coordinate in asteroid_spaces.keys():
        count = asteroid_visability(asteroid_spaces, coordinate, x_max, y_max)
        counter[len(count)] = coordinate
    best_asteroid = counter[max(counter)]
    order = {}
    count = len(asteroid_spaces)
    while count != 0:
        visable_asteroids = asteroid_visability(asteroid_spaces, best_asteroid, x_max, y_max)
        order = determine_order(best_asteroid, order, visable_asteroids)
        remove_asteroids(visable_asteroids, asteroid_spaces)
        count = len(asteroid_spaces) - 1
    print(order[199])
    print(time.time() - now)


if __name__ == "__main__":
    main()
