from collections import defaultdict


class TierList:

    def __init__(self):
        self.graph = defaultdict(set)
        self.vertex = {}
        self.component_tier_list = {'FUEL': 1}
        self.compound_tier_list = defaultdict(list)
        self.default_tier = 0

    def construct_compound_tier_list(self):
        for component, tier in self.component_tier_list.items():
            self.compound_tier_list[tier].append(component)

    def get_component_tier(self, component):
        return self.component_tier_list.get(component, self.default_tier)

    def set_component_tier(self, component, tier):
        self.component_tier_list[component] = tier

    def _bump_all_tier_by(self, count):
        for component in self.component_tier_list.keys():
            if component == 'FUEL':
                continue
            self.component_tier_list[component] += count

    def find_list_of_tiers(self, components):
        tiers = []
        for component in components:
            tiers.append(self.component_tier_list.get(component, self.default_tier))
        return tiers

    def determine_compound_tier(self, compound):
        input_components = list(compound.input.keys())
        output_component = list(compound.output.keys())[0]
        for input_component in input_components:
            self.graph[input_component].add(output_component)

    def _relax(self, ver1, ver2):
        if self.vertex[ver1] + 1 >= self.vertex[ver2]:
            self.vertex[ver2] = self.vertex[ver1] + 1

    def bellam_ford_but_inverse(self):
        self.vertex = {k: -1 for k in self.graph.keys()}
        self.vertex['ORE'] = 1
        self.vertex['FUEL'] = -1
        for _ in range(0, len(self.vertex)):
            for vertex in self.vertex.keys():
                for adj_vertex in self.graph[vertex]:
                    self._relax(vertex, adj_vertex)
        self.component_tier_list = self.vertex

    # def determine_compound_tier(self, compound):
    #     input_components = list(compound.input.keys())
    #     output_component = list(compound.output.keys())[0]
    #     output_tier = self.get_component_tier(output_component)
    #     if output_tier == 0:
    #         lowest_input_tier = min(self.find_list_of_tiers(input_components))
    #         if lowest_input_tier is 0:
    #             output_tier = 1
    #             self._bump_all_tier_by(1)
    #         else:
    #             output_tier = lowest_input_tier
    #             for input_comp in input_components:
    #                 input_tier = self.get_component_tier(input_comp)
    #                 if input_tier != 0:
    #                     self.set_component_tier(input_comp, input_tier + 1)
    #     for input_component in input_components:
    #         input_tier = self.get_component_tier(input_component)
    #         if input_tier < output_tier:
    #             self.set_component_tier(input_component, output_tier + 1)
    #         elif input_tier == output_tier:
    #             self.set_component_tier(input_component, output_tier + 1)
    #             self._bump_all_tier_by(1)
    #         else:
    #             self.set_component_tier(input_component, input_tier)
    #     self.set_component_tier(output_component, output_tier)
