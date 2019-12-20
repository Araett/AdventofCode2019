import pytest
from hamcrest import assert_that, is_

from tier_list import TierList
from compund import Compound
from transformations import read_input, create_and_tier_compounds

@pytest.fixture
def tier_list():
    return TierList()


def describe_TierList():

    def describe_create_and_tier():

        def describe_input1():
            input_file = 'test_input1'

            def test_it_makes_a_good_tier_list():
                _, tier_list = create_and_tier_compounds(read_input(input_file))
                tier_list.bellam_ford_but_inverse()
                assert_that(
                    tier_list.component_tier_list,
                    is_(
                        {'FUEL': 6, 'ORE': 1, 'A': 2, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
                    ),
                )

        def describe_input2():
            input_file = 'test_input2'

            def test_it_makes_a_good_tier_list():
                _, tier_list = create_and_tier_compounds(read_input(input_file))
                tier_list.bellam_ford_but_inverse()
                assert_that(
                    tier_list.component_tier_list,
                    is_(
                        {'FUEL': 4, 'ORE': 1, 'A': 2, 'B': 2, 'C': 2, 'AB': 3, 'BC': 3, 'CA': 3}
                    ),
                )

        def describe_input3():
            input_file = 'test_input3'

            def test_it_makes_a_good_tier_list():
                _, tier_list = create_and_tier_compounds(read_input(input_file))
                tier_list.bellam_ford_but_inverse()
                assert_that(
                    tier_list.component_tier_list,
                    is_(
                        {'VPVL': 0, 'FWMGM': 0, 'CXFTF': 0, 'MNCFX': 2, 'NVRVD': 2, 'JNWZP': 2, 'STKFG': 0, 'VJHF': 2, 'HVMC': 1, 'GNMV': 0, 'ORE': 1, 'RFSQX': 0, 'FUEL': 1}
                    ),
                )

        def describe_input():
            input_file = 'test_input4'

            def test_it_makes_a_good_tier_list():
                _, tier_list = create_and_tier_compounds(read_input(input_file))
                tier_list.bellam_ford_but_inverse()
                assert_that(
                    tier_list.component_tier_list,
                    is_(
                        {'ORE': 1, 'ZLQW': 4, 'BMBT': 3, 'XCVML': 3, 'XMNCP': 4, 'WPTQ': 0, 'MZWV': 3, 'RJRHP': 0, 'VRPVC': 2, 'BHXH': 2, 'KTJDG': 2, 'PLWSL': 1, 'FHTLT': 3, 'ZDVW': 4, 'XDBXC': 3, 'LTCX': 3, 'CNZTR': 2, 'FUEL': 4}
                    ),
                )

#
#     def describe_get_component_tier():
#
#         def describe_given_that_there_is_no_component_in_tier_list():
#
#             def test_it_returns_default_tier(tier_list):
#                 component = 'TEST'
#                 tier = tier_list.get_component_tier(component)
#                 assert_that(tier, is_(0))
#
#         def describe_given_that_tier_list_has_a_component():
#
#             def test_it_returns_component_tier(tier_list):
#                 exp = 5
#                 tier_list.component_tier_list['TEST'] = exp
#                 component = 'TEST'
#                 tier = tier_list.get_component_tier(component)
#                 assert_that(tier, is_(exp))
#
#     def describe_set_component_tier():
#
#         def describe_given_component_and_tier():
#
#             component = 'TEST'
#             tier = 4
#
#             def test_it_sets_component_tier_in_the_tier_list(tier_list):
#                 tier_list.component_tier_list = {}
#                 tier_list.set_component_tier(component, tier)
#                 assert_that(tier_list.component_tier_list, is_({component: tier}))
#
#     def describe_determine_input_and_output_tiers():
#
#         def describe_given_linear_compound():
#
#             test_compound = Compound('1 INPUT => 1 OUTPUT')
#
#             def describe_given_no_components_in_tier_list():
#
#                 component_tier_list = {}
#
#                 def test_it_adds_both_components_to_tier_list_starting_from_0(tier_list):
#                     # Output is higher than input in tier
#                     tier_list.component_tier_list = component_tier_list
#                     tier_list.determine_compound_tier(test_compound)
#                     assert_that(tier_list.get_component_tier('INPUT'), is_(2))
#                     assert_that(tier_list.get_component_tier('OUTPUT'), is_(1))
#
#             def describe_given_output_tier():
#
#                 component_tier_list = {'OUTPUT': 5}
#
#                 def test_it_adds_components_to_tier_list_starting_output_tier(tier_list):
#                     tier_list.component_tier_list = component_tier_list
#                     tier_list.determine_compound_tier(test_compound)
#                     assert_that(tier_list.get_component_tier('INPUT'), is_(6))
#                     assert_that(tier_list.get_component_tier('OUTPUT'), is_(5))
#
#             def describe_given_input_tier():
#
#                 component_tier_list = {'INPUT': 5}
#
#                 def test_it_adds_components_to_tier_list_output_being_lower_than_input(tier_list):
#                     tier_list.component_tier_list = component_tier_list
#                     tier_list.determine_compound_tier(test_compound)
#                     assert_that(tier_list.get_component_tier('INPUT'), is_(5))
#                     assert_that(tier_list.get_component_tier('OUTPUT'), is_(1))
#
#             def describe_given_input_tier_is_higher_than_output():
#
#                 component_tier_list = {'INPUT': 5, 'OUTPUT': 6}
#
#                 def test_it_adds_components_to_tier_list_output_being_lower_than_input(tier_list):
#                     tier_list.component_tier_list = component_tier_list
#                     tier_list.determine_compound_tier(test_compound)
#                     assert_that(tier_list.get_component_tier('INPUT'), is_(7))
#                     assert_that(tier_list.get_component_tier('OUTPUT'), is_(6))
#
#         def describe_given_multi_compound():
#
#             test_compound = Compound('1 INPUT_1, 1 INPUT_2 => 1 OUTPUT')
#
#             def describe_given_no_components_in_tier_list():
#
#                 component_tier_list = {}
#
#                 def test_it_adds_all_components_to_tier_list(tier_list):
#                     tier_list.component_tier_list = component_tier_list
#                     tier_list.determine_compound_tier(test_compound)
#                     assert_that(tier_list.get_component_tier('INPUT_1'), is_(2))
#                     assert_that(tier_list.get_component_tier('INPUT_2'), is_(2))
#                     assert_that(tier_list.get_component_tier('OUTPUT'), is_(1))

