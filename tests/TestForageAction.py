import unittest

from Actions.ForageAction import ForageAction

from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from Registries.CharacterRegistry import CharacterRegistry

def has_an_item(char: Character):
    return len(char.weapons) > 0 or len(char.food) > 0 or len(char.medicine) > 0

def has_no_item(char: Character):
    return len(char.weapons) == 0 and len(char.food) == 0 and len(char.medicine) == 0

class ForageActionUnitTests(unittest.TestCase):
    def setUp(self):
        self.all_items = [Item("Sword", "Sword", combat_mod=2, hands_needed=1), \
                     Item("BandAid", "BandAid", is_medicine=True), \
                     Item("Bread", "Bread", is_food=True)]
    
    # Checks that a single team member will always be given
    # the reward if the search succeeds
    def test_single_member_team_success(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_success}))
        team = Team(["Bob"])
        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        self.assertTrue(has_an_item(bob))

    # Test that a search can fail
    def test_single_member_team_failure(self):
        CharacterRegistry.Clear()
        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_fail}))
        team = Team(["Bob"])
        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        self.assertTrue(has_no_item(bob))

    # Tests that when searching, the highest modifier is used
    def test_team_total_modifier(self):
        CharacterRegistry.Clear()

        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_success}))
        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Jane", "Jane", {"Survival Skill": guaranteed_fail}))
        team = Team(["Bob", "Jane"])

        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        jane = CharacterRegistry.GetCharacter("Jane")
        self.assertTrue(has_an_item(bob) or has_an_item(jane))

    # Tests that when an item is found, the person with the highest Commanding + Friendly
    # value will get the item
    def test_team_taker_weight(self):
        CharacterRegistry.Clear()

        guaranteed_success = 100
        almost_guaranteed_fail = -99
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_success}, \
                                                 strategies={"Commanding": guaranteed_success, "Friendly": almost_guaranteed_fail}))

        guaranteed_fail = -100
        almost_guaranteed_success = 99
        CharacterRegistry.AddCharacter(Character("Jane", "Jane", strategies={"Commanding": guaranteed_fail, "Friendly": almost_guaranteed_success}))

        neutral = 0
        CharacterRegistry.AddCharacter(Character("Jon", "Jon", strategies={"Commanding": neutral, "Friendly": neutral}))
        team = Team(["Jon", "Bob", "Jane"])

        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        self.assertTrue(has_an_item(bob))

if __name__ == '__main__':
    unittest.main()