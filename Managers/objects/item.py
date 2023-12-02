class Item():
    def __init__(self) -> None:
        self.is_medicine: bool = False
        self.is_food: bool = False
        self.combat_modifier: int = 0

    def load_json_object(self, json_obj):
        self.is_medicine = json_obj.get("is_medicine", False)
        self.is_food = json_obj.get("is_food", False)
        self.combat_modifier = json_obj.get("combat_modifier", 0)