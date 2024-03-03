
from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from Managers.objects.item import Item

# A separate class in order to improve dependency graph
class ItemRegistry():
    items: Dict[str, Item] = {}

    @staticmethod
    def AddItem(i: Item):
        ItemRegistry.items[i.nid] = i

    @staticmethod
    def GetItem(item_nid: str):
        return ItemRegistry.items[item_nid]