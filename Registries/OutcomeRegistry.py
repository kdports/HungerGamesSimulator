from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Managers.objects.combatoutput import CombatOutput

class OutcomeRegistry():
    outcomes: List[CombatOutput] = []

    @staticmethod
    def AddOutcome(result: CombatOutput):
        OutcomeRegistry.outcomes.append(result)

    @staticmethod
    def Clear():
        OutcomeRegistry.outcomes = []