from pprint import pprint
from BS_helper import BS_helper
import json
from google.cloud import bigquery
from google.cloud import secretmanager


config = json.load(open("api/config.json"))
token = config["BS_token"]
club_tag = config["club_tag"]

def main():
    BS = BS_helper(token)
    # GET ALL PLAYERS
    tag_to_name = BS.get_tag_to_name(club_tag)
    # ONLY LEAGUE MATCH
    lines_to_add = []
    for tag in tag_to_name:
        name = tag_to_name[tag]
        battlelog = BS.get_player_battlelog(tag)
        lines = BS.get_club_league_matchs(name, tag, battlelog)
        print(name, len(lines))
        pprint(lines)
        lines_to_add += lines
    # ONLY NEW RECORDS
    lines_to_add = BS.only_new_lines(lines_to_add)
    #UPLOAD
    BS.upload_lines(lines_to_add)


if __name__ == "__main__":
    main()