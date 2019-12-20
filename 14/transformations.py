import math
from collections import defaultdict

from tier_list import TierList
from compund import Compound


def read_input(input_file):
    with open(input_file, 'r') as f:
        return f.readlines()


def required_components_are_linear(compounds, required):
    for req_component, req_count in required.items():
        for compound in compounds:
            transformation_product = compound.output.get(req_component, None)
            if transformation_product is None:
                continue
            if not compound.is_linear_transformable():
                return False
    return True


def required_components_are_transformed_to_ore(compounds, required):
    for req_component, req_count in required.items():
        for compound in compounds:
            transformation_product = compound.output.get(req_component, None)
            if transformation_product is None:
                continue
            if not compound.is_ore_transformable():
                return False
    return True


def find_minimal_components(compounds, required):
    processed = defaultdict(int)
    transformed = False
    linear_flag = False
    ore_flag = False
    # print(required)
    if required_components_are_linear(compounds, required):
        linear_flag = True
    if required_components_are_transformed_to_ore(compounds, required):
        ore_flag = True
    for req_component, req_count in required.items():
        for compound in compounds:
            transformation_product = compound.output.get(req_component, None)
            if transformation_product is None:
                continue
            if not linear_flag and compound.is_linear_transformable():
                processed[req_component] += req_count
                continue
            if not ore_flag and compound.is_ore_transformable():
                processed[req_component] += req_count
                continue
            transformed = True
            count_required = math.ceil(req_count/transformation_product)
            # print(req_count, transformation_product, count_required)
            input_components = {x: y*count_required for (x, y) in compound.input.items()}
            # print(req_count, req_component, input_components)
            for component, count in input_components.items():
                # print(component, count)
                processed[component] += count
    if transformed is False:
        return required
    return find_minimal_components(compounds, processed)


def tiered_minimal_compound(tier_list: TierList, compounds, required):
    for tier in range(tier_list.get_component_tier('FUEL'), 0, -1):
        print(tier, required)
        processed = defaultdict(int)
        for req_component, req_count in required.items():
            for compound in compounds:
                transformation_product = compound.output.get(req_component, None)
                if transformation_product is None:
                    continue
                if tier_list.get_component_tier(req_component) != tier:
                    processed[req_component] += req_count
                    continue
                count_required = math.ceil(req_count / transformation_product)
                input_components = {x: y * count_required for (x, y) in compound.input.items()}
                for component, count in input_components.items():
                    processed[component] += count
        if len(processed) != 0:
            required = {**processed}
    return required

# def tiered_minimal_compound(tier_list: TierList, compounds, required):
#     processed = defaultdict(int)
#     transformed = False
#     tiers = tier_list.find_list_of_tiers(required)
#     lowest_tier = min(tiers)
#     equal_tier = len(set(tiers)) == 1
#     print(required, lowest_tier)
#     for req_component, req_count in required.items():
#         if tier_list.get_component_tier(req_component) >= lowest_tier:
#             for compound in compounds:
#                 transformation_product = compound.output.get(req_component, None)
#                 if transformation_product is None:
#                     continue
#                 if lowest_tier == tier_list.get_component_tier(req_component) and not equal_tier:
#                     processed[req_component] += req_count
#                     continue
#                 transformed = True
#                 count_required = math.ceil(req_count / transformation_product)
#                 input_components = {x: y * count_required for (x, y) in compound.input.items()}
#                 print(req_count, req_component, input_components, tier_list.get_component_tier(req_component))
#                 for component, count in input_components.items():
#                     processed[component] += count
#         else:
#             processed[req_component] += req_count
#     if transformed is False:
#         return required
#     return tiered_minimal_compound(tier_list, compounds, processed)


# def tier_compounds(component_tier_list, compound):
#     input_compontents = compound.input.keys()
#     output_components = compound.output.keys()
#     for input
#     if component_tier_list.get_input_tier(input_compontents):
#
#     pass


def create_and_tier_compounds(transformations):
    component_tier_list = TierList()
    possible_compounds = []
    for transformation in transformations:
        compound = Compound(transformation)
        possible_compounds.append(compound)
        component_tier_list.determine_compound_tier(compound)
        # print(component_tier_list.component_tier_list)
    return possible_compounds, component_tier_list


def main():
    input_files = [
        # 'test_input1',
        # 'test_input2',
        # 'test_input3',
        # 'test_input4',
        # 'test_input5',
        'input',
    ]
    for input_file in input_files:
        print('--------------------------------------------------------------')
        transformations = read_input(input_file)
        possible_compounds, tier_list = create_and_tier_compounds(transformations)
        tier_list.construct_compound_tier_list()
        tier_list.bellam_ford_but_inverse()
        print(tier_list.component_tier_list)
        print(tiered_minimal_compound(tier_list, possible_compounds, {'FUEL': 1}))
        # print(find_minimal_components(possible_compounds, {'FUEL': 1}))


if __name__ == '__main__':
    main()
