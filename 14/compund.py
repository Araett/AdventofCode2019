class Compound:

    def __init__(self, transformation):
        self.input = {}
        self.output = {}
        self.parse_transformation(transformation)

    def parse_transformation(self, transformation):
        inp, out = transformation.split('=>')
        out_count, out_compound = out.strip().split(' ')
        self.output[out_compound] = int(out_count)
        for input_component in inp.split(','):
            in_count, in_compound = input_component.strip().split(' ')
            self.input[in_compound] = int(in_count)

    def is_linear_transformable(self):
        return len(self.input) == 1

    def is_ore_transformable(self):
        return 'ORE' in self.input.keys()
