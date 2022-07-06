from BS_helper import BS_helper
from google.cloud import secretmanager
import base64
import os
import json


PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

secrets = secretmanager.SecretManagerServiceClient()

bs_secrets = secrets.access_secret_version(request={"name": "projects/" + PROJECT_NUMBER + "/secrets/bs-dashboard-secrets/versions/latest"}).payload.data.decode("utf-8")
bs_secrets = json.loads(bs_secrets)

token = bs_secrets['BS_token']
club_tag = bs_secrets['club_tag']
PROJECT_ID = bs_secrets['PROJECT_ID']
DATASET_ID = bs_secrets['DATASET_ID']
TABLE_ID = bs_secrets['TABLE_ID']


def main(request, context):
    print("START")
    BS = BS_helper(token, PROJECT_ID, DATASET_ID, TABLE_ID)
    # GET ALL PLAYERS
    tag_to_name = BS.get_tag_to_name(club_tag)
    # ONLY LEAGUE MATCH
    lines_to_add = []
    for tag in tag_to_name:
        name = tag_to_name[tag]
        player = BS.get_player_info(tag)
        battlelog = BS.get_player_battlelog(tag)
        lines = BS.get_club_league_matchs(name, tag, player, battlelog)
        lines_to_add += lines
    print(len(lines_to_add), "lines to add before check")
    # ONLY NEW RECORDS
    lines_to_add = BS.only_new_lines(lines_to_add)
    if lines_to_add:
        print("Lines that will be added :")
    for i,line in enumerate(lines_to_add):
        print(i+1, ":", line)
    # UPLOAD
    BS.upload_lines(lines_to_add)
    print("END")
