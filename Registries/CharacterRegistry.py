
from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from Managers.objects.character import Character

# A separate class in order to improve dependency graph
class CharacterRegistry():
    characters: Dict[str, Character] = {}

    @staticmethod
    def AddCharacter(char: Character):
        CharacterRegistry.characters[char.nid] = char

    @staticmethod
    def GetCharacter(char_nid: str):
        return CharacterRegistry.characters[char_nid]

    @staticmethod
    def Clear():
        return CharacterRegistry.characters.clear()