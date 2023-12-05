from distutils.command import build
import json
import os

def MakeJSONDict(nid, name, is_medicine, is_food, combat_modifier, hands_needed):  
    character_dict = {
        "nid": nid,
        "name": name,
        "is_medicine": is_medicine,
        "is_food": is_food,
        "combat_modifier": combat_modifier,
        "hands_needed": hands_needed
    }
    return json.dumps(character_dict)

def MakeItemFolder():
    current_dirname = os.getcwd()
    characters_folder = os.path.join(current_dirname, "items/")
    if not os.path.exists(characters_folder):
        os.makedirs(characters_folder)
    new_character_dir = os.path.join(characters_folder, nid.lower())
    if not os.path.exists(new_character_dir):
        os.makedirs(new_character_dir)
    else:
        print("Folder with Item NID already exists!\n")
        return False
    return True

def WriteItemFile(json_to_write, nid):
    current_dirname = os.path.dirname(__file__)
    item_file = os.path.join(current_dirname, "items/" + nid.lower() + "/" + nid.lower() + "_item_sheet.json")
    with open(item_file, "w") as outfile:
        outfile.write(json_to_write)

build_item_mode = 1

positive_responses = ["YES", "Y", "1", "TRUE"]
negative_responses = ["NO", "N", "0", "FALSE"]

def FindResponseType(response: str):
    response = str(response).upper()
    if response in positive_responses:
        return True
    return False

while build_item_mode:
    name = str(input("Enter your item's displayed name: "))
    nid = str(input("Enter a unique identifier: "))

    if not MakeItemFolder():
        continue

    is_medicine = FindResponseType(str(input("Is your item medicine?\n")))
    is_food = FindResponseType(str(input("Is your item food?\n")))
    combat_modifier = int(input("When holding it, what integer combat bonus does it give?\n"))
    hands_needed = int(input("How many hands are needed to hold it?\nIf it is not a weapon, enter 0.\n"))

    print("Item creation done! Now saving...\n\n")

    item_json = MakeJSONDict(nid, name, is_medicine, is_food, combat_modifier, hands_needed)
    WriteItemFile(item_json, nid)

    print("Saving complete! Written to items/" + nid.lower() + "\n\n")

    make_new = input("Create another item? Type Yes to restart item creation: ")
    if make_new.upper() not in positive_responses:
        build_item_mode = 0