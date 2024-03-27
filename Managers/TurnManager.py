from logging.config import valid_ident
from typing import List, Dict
from Actions.ActionEnum import Actions
from Actions.CombatAction import CombatAction
from Actions.ForageAction import ForageAction
from Actions.HideAction import HideAction
from Managers.objects.character import Character
from Managers.objects.item import Item
from Registries.CharacterRegistry import CharacterRegistry
from Registries.ItemRegistry import ItemRegistry
from utilities import static_random
from Managers.helper_functions import CharacterFunctions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Managers.objects.team import Team
    from Managers.objects.combatoutput import CombatOutput
    from Actions.GameAction import GameAction

class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.teams: List[Team] = []
        self.seed = 0
        self.combats: List[CombatOutput] = []
        self.action_list: List[GameAction] = []
        # TODO: Make this actually do something
        self.modifiers = []

    # Step 1 of turn
    def StartTurn(self, data: dict):
        self.LoadJSONData(data)
        static_random.set_seed(self.seed)
        self.BuildAlliances()
        self.MakeSinglePersonTeams()

    # Step 2 of turn
    def RandomizeTeamActionOrder(self):
        self.teams = static_random.shuffle(self.teams)

    # Step 3 of turn
    def ChooseActions(self):
        self.ConsiderOneRemainingTeam()
        for team in self.teams:
            self.DecideBetrayals(team)
            team.decide_action([t for t in self.teams if t != team])
        self.DoTargeting()

    # Find targets for each combat action
    def DoTargeting(self):
        #TODO: Thoughts
        """We need a way to keep track of valid targets who aren't the 
        combat initiator nor already in a combat. If a hiding target is
        chosen, there should be a dice roll to see if they're found.
        All combats should be added to action_list first, then the 
        other actions."""

    # Each character decides if they will betray
    def DecideBetrayals(self, team: Team):
        for char_nid in team.members():
            char = CharacterRegistry.GetCharacter(char_nid)
            betrayal_chance = char.base_betrayal_chance()
            # more likely to betray if there's no greater threat
            if len(team.members()) > CharacterRegistry.Size() // 2:
                betrayal_chance += 15
            char.will_betray = True if static_random.get_randint(0, 99) < betrayal_chance else False

    # Different effects depending on the team action
    def PlanBetrayals(self, char: Character, team: Team):
        action = team.action
        for char_nid in team:
            char = CharacterRegistry.GetCharacter(char_nid)
            if char.will_betray:
                # TODO
                # If Forage Action, betrayer stays part of team 
                # and takes a forage action that only benefits themselves
                if action == Actions.Forage:
                    pass
                # If Hide Action, betrayer will only heal themselves
                if action == Actions.Hide:
                    pass
                # If Combat Action, betrayer splits from party immediately
                # and does not assist
                if action == Actions.Combat:
                    pass
        
    '''
    DOES NOT HANDLE the case where there is
    one team of one person. Assume that's checked
    elsewhere
    '''
    def ConsiderOneRemainingTeam(self):
        if len(self.teams) == 1:
            new_teams = []
            for char_nid in self.teams[0].members():
                char = CharacterRegistry.GetCharacter(char_nid)
                new_teams.append(Team([char]))
            self.teams = new_teams

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.LoadCharacterData(data["characters"])
        self.LoadItemData(data["items"])
        self.teams = data.get("teams", [])
        self.seed = data.get("seed", 0)
        # We don't load combat outputs from last turn because we don't care

    def SaveJSONData(self):
        data = {}
        data["board"] = self.board
        data["characters"] = [CharacterRegistry.GetCharacter(ch).save() for ch in CharacterRegistry.characters]
        data["items"] = [ItemRegistry.GetItem(i).save() for i in ItemRegistry.items]
        data["teams"] = [t.save() for t in self.teams]
        data["seed"] = self.seed
        # we save combat outputs purely for human review
        data["combats"] = [c.save() for c in self.combats]
        return data

    def LoadCharacterData(self, char_data: dict):
        # Loads into the CharacterRegistry holder
        for char_nid in char_data.keys():
            new_character = Character()
            new_character.load_json_object(char_data[char_nid])
            CharacterRegistry.AddCharacter(new_character)

    def LoadItemData(self, item_data: dict):
        for item_nid in item_data.keys():
            new_item = Item()
            new_item.load_json_object(item_data[item_nid])
            ItemRegistry.AddItem(new_item)

    def IsCharacterInTeam(self, char_nid):
        for team in self.teams:
            if char_nid in team:
                return True
        return False

    def GetCharacter(self, char_nid):
        return CharacterRegistry.GetCharacter(char_nid)

    def CalculateTrueAllies(self):
        for char_nid in CharacterRegistry.characters:
            char = self.GetCharacter(char_nid)
            true_allies = []
            for prospective_ally_nid in char.get_alliances():
                if char.nid in CharacterRegistry.characters[prospective_ally_nid].get_alliances():
                    true_allies.append(prospective_ally_nid)
            char.set_alliances(true_allies)

    def BuildAlliances(self):
        self.CalculateTrueAllies()

        for char_nid in CharacterRegistry.characters:
            char = self.GetCharacter(char_nid)
            # You can't be in multiple teams
            if self.IsCharacterInTeam(char_nid):
                continue

            for team in self.teams:
                if CharacterFunctions.ResolveCharacterEnteringTeam(char):
                    team.add_player(char_nid)
                    break
            self.PurgeEmptyTeams()

    def MakeSinglePersonTeams(self):
        for char_nid in CharacterRegistry.characters:
            if not self.IsCharacterInTeam(char_nid):
                self.teams.append(CharacterFunctions.MakeSinglePersonTeam(char_nid))

    def KillCharacter(self, nid):
        for team in self.teams:
            team.remove_player(nid)
        self.PurgeEmptyTeams()

    def PurgeEmptyTeams(self):
        for team in self.teams:
            if len(team) == 0:
                self.teams.remove(team)

    def RemainingPlayers(self):
        return len(CharacterRegistry.characters)

turn = TurnManager()

def make_turn_manager():
    global turn
    return turn