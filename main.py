from pprint import pprint
from api import BS_helper
import json


config = json.load(open("config.json"))
token = config["BS_token"]
club_tag = config["club_tag"]

def main():
    BS = BS_helper(token)
    tag_to_name = BS.get_tag_to_name(club_tag)
    tag_to_name["#P0C9Y9LU0"] = "mateug"

    lines_to_add = []

    for tag in tag_to_name:
        if tag == "#L0VRP2G9" :
        # if tag == "#P0C9Y9LU0":
            battlelog = BS.get_player_battlelog(tag)
            for battle in battlelog:
                time = battle["battleTime"]
                print(time)
                battle_details = battle["battle"]
                if 'mode' in battle_details: # !="soloShowdown" !="duoShowdown"
                    mode = battle["mode"]
                    print(mode)
                if "type" in battle: # ==teamRanked
                    type = battle["type"]
                    print(type)
                if 'result' in battle:
                    result = battle["result"]
                    print(result)
                if 'trophyChange' in battle: # != teamRanked != 8 et mode
                    trophychange = battle["trophyChange"]
                    print(trophychange)
                print()


if __name__ == "__main__":
    main()