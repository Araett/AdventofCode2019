import math

class Moon:

    def __init__(self):
        self.pos = {'x': 0, 'y': 0, 'z': 0}
        self.initial_pos = {}
        self.velocity = {'x': 0, 'y': 0, 'z': 0}

    def apply_gravity_to_one_axis(self, axis, other_moons):
        for other_moon in other_moons:
            if self.pos[axis] > other_moon.pos[axis]:
                velocity = -1
            elif self.pos[axis] == other_moon.pos[axis]:
                velocity = 0
            else:
                velocity = 1
            self.velocity[axis] += velocity

    def apply_gravity(self, other_moons):
        for other_moon in other_moons:
            for axis, position in other_moon.pos.items():
                if self.pos[axis] > position:
                    velocity = -1
                elif self.pos[axis] == position:
                    velocity = 0
                else:
                    velocity = 1
                self.velocity[axis] += velocity

    def apply_velocity(self):
        for axis in self.pos.keys():
            self.pos[axis] += self.velocity[axis]

    def print_stats(self):
        print(
            f"pos=<x={self.pos['x']}, "
            f"y={self.pos['y']}, "
            f"z={self.pos['z']}>, "
            f"vel=<x={self.velocity['x']}, "
            f"y={self.velocity['y']}, "
            f"z={self.velocity['z']}>"
        )

    def parse_input(self, input_coord):
        coords = input_coord[1:-2].split(', ')
        for dimension in coords:
            axis, value = dimension.split('=')
            self.pos[axis] = int(value)
        self.initial_pos = {**self.pos}

    def calc_energy(self):
        potential_energy = sum([abs(x) for x in self.pos.values()])
        kinetic_energy = sum([abs(x) for x in self.velocity.values()])
        return potential_energy * kinetic_energy

    def same_position(self):
        if self.pos == self.initial_pos and self.velocity == {'x': 0, 'y': 0, 'z': 0}:
            return True
        return False


def get_energy(list_of_moons):
    s = 0
    for moon in list_of_moons:
        s += moon.calc_energy()
    return s


def read_input():
    with open('input', 'r') as f:
        return f.readlines()


def try_equality(list_of_moons):
    for moon in list_of_moons:
        if not moon.same_position():
            return False
    return True


def step(list_of_moons):
    for moon in list_of_moons:
        other_moons = [x for x in list_of_moons if x is not moon]
        moon.apply_gravity(other_moons)
    for moon in list_of_moons:
        moon.apply_velocity()


def step_one_axis(axis, list_of_moons):
    for moon in list_of_moons:
        other_moons = [x for x in list_of_moons if x is not moon]
        moon.apply_gravity_to_one_axis(axis, other_moons)
    for moon in list_of_moons:
        moon.apply_velocity()


def find_cycle(moon_list):
    axies = ['x', 'y', 'z']
    cycles = {'x': 0, 'y': 0, 'z': 0}
    for axis in axies:
        i = 0
        while True:
            step_one_axis(axis, moon_list)
            i += 1
            if try_equality(moon_list):
                break
        cycles[axis] = i
        print(cycles)
    lcm = int((cycles['x'] * cycles['y']) / math.gcd(cycles['x'], cycles['y']))
    return int((lcm * cycles['z']) / math.gcd(lcm, cycles['z']))


def find_energy(list_of_moons):
    steps = 1000
    for i in range(0, steps):
        step(list_of_moons)
    return get_energy(list_of_moons)


def get_moon_list(moon_input):
    list_of_moons = []
    for moon in moon_input:
        new_moon = Moon()
        new_moon.parse_input(moon)
        list_of_moons.append(new_moon)
    return list_of_moons


def main():
    import time
    now = time.time()
    moons_coords = read_input()
    list_of_moons = get_moon_list(moons_coords)
    print(find_energy(list_of_moons))
    list_of_moons = get_moon_list(moons_coords)
    print(find_cycle(list_of_moons))
    print(time.time() - now)





if __name__ == "__main__":
    main()
