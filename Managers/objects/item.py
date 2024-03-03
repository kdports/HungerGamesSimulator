class Item():
    def __init__(self, nid="", name="", is_medicine=False, is_food=False, combat_mod=0, hands_needed=0) -> None:
        self.nid = nid
        self.name = name
        self.is_medicine: bool = is_medicine
        self.is_food: bool = is_food
        self.combat_modifier: int = combat_mod
        self.hands_needed: int = hands_needed # 0 is unequippable, 1 is one-handed, 2 is two-handed

    def load_json_object(self, json_obj):
        self.nid = json_obj["nid"]
        self.name = json_obj["name"]
        self.is_medicine = json_obj.get("is_medicine", False)
        self.is_food = json_obj.get("is_food", False)
        self.combat_modifier = json_obj.get("combat_modifier", 0)
        self.hands_needed = json_obj.get("hands_needed", 0)

    def save(self):
        save_dict = {
            "nid": self.nid,
            "name": self.name,
            "is_medicine": self.is_medicine,
            "is_food": self.is_food,
            "combat_modifier": self.combat_modifier,
            "hands_needed": self.hands_needed
        }
        return save_dict
    
    def get_combat_modifier(self) -> int:
        return self.combat_modifier