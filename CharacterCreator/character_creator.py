import json
import time
import os

MAX_SKILL_POINTS = 3

def AssignSkillPoints(points_remaining, skill_name):
    skill_val = -1
    if points_remaining > 0:
        while skill_val == -1 or skill_val > points_remaining:
            print_str = "Assign up to " + str(points_remaining) + " points to " + skill_name + ": "
            skill_val = int(input(print_str))
            if skill_val > points_remaining:
                print("Assigned too many points!\n")
                time.sleep(2)
        print("\nYou have " + str(points_remaining - skill_val) + " points remaining.")
    return max(0, skill_val)

def AssignStrategy(strategy_name, strategy_desc):
    strategy_val = 99
    while strategy_val == 99 or (strategy_val < -3 or strategy_val > 3):
        strategy_val = int(input(strategy_name +": " + strategy_desc + "\nAssign any value from -3 to 3: "))
        if strategy_val < -3 or strategy_val > 3:
            print("Assigned value is out of range!\n")
            time.sleep(2)    
    return strategy_val      

def MakeJSONDict(nid, name, skills, strategies, alliances):  
    character_dict = {
        "nid": nid,
        "name": name,
        "skills": skills,
        "strategies": strategies,
        "alliances": alliances
    }
    return json.dumps(character_dict)

def MakeCharacterFolder():
    current_dirname = os.path.dirname(__file__)
    characters_folder = os.path.join(current_dirname, "characters/")
    if not os.path.exists(characters_folder):
        os.makedirs(characters_folder)
    new_character_dir = os.path.join(characters_folder, nid.lower())
    if not os.path.exists(new_character_dir):
        os.makedirs(new_character_dir)
    else:
        print("Folder with Character NID already exists!\n")
        return False
    return True

def WriteCharacterFile(json_to_write, nid):
    current_dirname = os.path.dirname(__file__)
    character_file = os.path.join(current_dirname, "characters/" + nid.lower() + "/" + nid.lower() + "_character_sheet.json")
    with open(character_file, "w") as outfile:
        outfile.write(json_to_write)

build_character_mode = 1

while build_character_mode:
    name = input("Enter your character's displayed name: ")
    nid = input("Enter a unique identifier: ")

    if not MakeCharacterFolder():
        continue

    print("You have three points to allocate between\nCombat Skill\nMedical Skill\nSurvival Skill\nEndurance Skill\n\nEach skill can only have up to two points allocated.")
    points_remaining = MAX_SKILL_POINTS

    time.sleep(1)

    skills = {
        "Combat Skill": 0,
        "Medical Skill": 0,
        "Survival Skill": 0,
        "Endurance Skill": 0
    }

    for skill in skills:
        skill_val = AssignSkillPoints(points_remaining, skill)
        skills[skill] = skill_val
        points_remaining -= skill_val

    print("Next is your character's strategies. Each value can be assigned from -3 to 3.\n\n")
    time.sleep(3)

    strategy_definitions = {
        "Friendly": "Higher means more likely to form alliances",
        "Trustworthy": "Higher means less likely to betray allies",
        "Aggressive": "Higher means more likely to pursue and attack other players",
        "Commanding": "More likely to make decisions within an alliance"
    }

    strategies = {}

    for strat in strategy_definitions:
        strategies[strat] = AssignStrategy(strat, strategy_definitions[strat])

    alliances_str = input("Enter a comma-separated list of nids of characters you wish to begin the game having an alliance with.\nIn order for the alliance to be valid, the other character must have your unique name in their list of allies!\n")
    alliances = alliances_str.split(',')

    i = 0
    while i < len(alliances):
        alliances[i] = alliances[i].strip()
        i += 1

    print("Character creation done! Now saving...\n\n")

    character_json = MakeJSONDict(nid, name, skills, strategies, alliances)
    WriteCharacterFile(character_json, nid)
    
    print("Saving complete! Written to character/" + nid.lower() + "\n\n")

    make_new = input("Create another character? Type Yes to restart character creation: ")
    if make_new.capitalize() != "YES":
        build_character_mode = 0
