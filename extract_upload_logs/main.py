from BS_helper import BS_helper
import json
from google.cloud import bigquery
from google.cloud import secretmanager
import base64
import os
import json


PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

secrets = secretmanager.SecretManagerServiceClient()

bs_secrets = secrets.access_secret_version(request={"name": "projects/"+ PROJECT_NUMBER +"/secrets/bs-dashboard-secrets/versions/latest"}).payload.data.decode("utf-8")
bs_secrets = json.loads(bs_secrets)

token = bs_secrets['BS_token']
club_tag = bs_secrets['club_tag']



def main(request, context):
    print("START")
    pubsub_message = json.loads(base64.b64decode(request['data']).decode('utf-8'))
    day = pubsub_message["day"]
    BS = BS_helper(token)
    # GET ALL PLAYERS
    tag_to_name = BS.get_tag_to_name(club_tag)
    # ONLY LEAGUE MATCH
    lines_to_add = []
    for tag in tag_to_name:
        name = tag_to_name[tag]
        battlelog = BS.get_player_battlelog(tag)
        lines = BS.get_club_league_matchs(day, name, tag, battlelog)
        lines_to_add += lines
    print(len(lines_to_add), "lines to add before check")
    # ONLY NEW RECORDS
    lines_to_add = BS.only_new_lines(lines_to_add)
    # UPLOAD
    BS.upload_lines(lines_to_add)
    print("END")