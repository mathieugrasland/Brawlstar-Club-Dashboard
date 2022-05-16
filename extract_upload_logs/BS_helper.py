from datetime import datetime, timedelta

import requests
from google.cloud import bigquery


# from google.cloud import secretmanager


class BS_helper:

    def __init__(self, token, PROJECT_ID, DATASET_ID, TABLE_ID):
        self.url_api = "https://api.brawlstars.com/"
        self.url_v = "v1/"
        self.url = self.url_api + self.url_v
        self.token = token
        self.headers = {'Authorization': self.token}
        self.PROJECT_ID = PROJECT_ID
        self.DATASET_ID = DATASET_ID
        self.TABLE_ID = TABLE_ID

    def get_club(self, club_tag):
        # Define the endpoint to use
        service = "clubs/"
        # Transform the club tag for api requierements
        club_tag = club_tag.replace("#", "%23")
        # URL to request
        url_request = self.url + service + club_tag
        # Make the request
        r = requests.get(
            url=url_request,
            headers=self.headers
        )
        return r.json()

    def get_tag_to_name(self, club_tag):
        club = self.get_club(club_tag)
        tag_to_name = {}
        for member in club['members']:
            tag = member['tag']
            name = member['name']
            tag_to_name[tag] = name
        return tag_to_name

    def get_name_to_tag(self, club_tag):
        club = self.get_club(club_tag)
        name_to_tag = {}
        for member in club['members']:
            tag = member['tag']
            name = member['name']
            name_to_tag[name] = tag
        return name_to_tag

    def get_player_battlelog(self, tag):
        tag = tag.replace("#", "%23")
        service = "players/" + tag + "/battlelog"
        url_request = self.url + service
        # Make the request
        r = requests.get(
            url=url_request,
            headers=self.headers
        )
        return r.json()["items"]

    def get_club_league_matchs(self, day, name, tag, battlelog):
        lines = []
        for battle in battlelog:
            time = battle["battleTime"]
            battle_details = battle["battle"]
            if 'type' in battle_details:
                if battle_details['type'] == "teamRanked" and 'trophyChange' in battle_details:
                    line["used_tickets"] = 2
                    line["with_club_mate"] = line["points"] in [9, 5]

                elif 'mode' in battle_details and battle_details['mode'] not in ("soloShowdown", "duoShowdown") and battle_details['type'] != 'challenge':
                    if 'trophyChange' in battle_details and battle_details['trophyChange'] != 8 and battle_details['trophyChange'] > 0 and battle_details['trophyChange'] < 5:
                        line["used_tickets"] = 1
                        line["with_club_mate"] = line["points"] in [4, 3]
                line = {}
                # START Brawler
                teams = battle_details["teams"]
                for team in teams:
                    for player in team:
                        if tag == player["tag"]:
                            brawler = player["brawler"]["name"]
                line["brawler"] = brawler
                # END Brawler
                # START SEASON
                date_parsed = datetime.strptime(
                    time, '%Y%m%dT%H%M%S.%fZ') + timedelta(days=-1)
                line["season"] = "Saison " + \
                    str(int(date_parsed.strftime("%Y%W")) - 202218)
                # END SEASON
                # START DAY
                date_parsed = datetime.strptime(time, '%Y%m%dT%H%M%S.%fZ')
                weekday = date_parsed.strftime("%A")
                if weekday in ['Wednesday', 'Thursday']:
                    day = "J1"
                if weekday in ['Friday', 'Saturday']:
                    day = "J2"
                if weekday in ['Sunday', 'Monday']:
                    day = "J3"
                # END DAY
                line["day"] = day
                line["name"] = name
                line["tag"] = tag
                line["points"] = battle_details['trophyChange']
                line["mode"] = battle_details['mode']
                line["result"] = battle_details["result"]
                line["timestamp"] = time
                line["datetime"] = time[0:4] + "-" + time[4:6] + "-" + \
                    time[6:11] + ":" + time[11:13] + ":" + time[13:19]
                line["seasonday"] = line["season"] + " " + line["day"]
                lines.append(line)
        return lines

    def get_current_db(self):
        PROJECT_ID = self.PROJECT_ID
        DATASET_ID = self.DATASET_ID
        TABLE_ID = self.TABLE_ID
        bqclient = bigquery.Client()
        # Download query results.
        query_string = f"""
        SELECT *
        FROM {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}
        """
        dataframe = bqclient.query(query_string).result(
        ).to_dataframe(create_bqstorage_client=True)
        return dataframe

    def only_new_lines(self, lines_to_add):
        current_db = self.get_current_db()
        tag_list = list(current_db['tag'])
        timestamp_list = list(current_db['timestamp'])
        keys = []
        for i in range(len(tag_list)):
            keys.append((tag_list[i], timestamp_list[i]))
        new_lines_to_add = []
        for line in lines_to_add:
            if (line['tag'], line['timestamp']) not in keys:
                new_lines_to_add.append(line)
        return new_lines_to_add

    def upload_lines(self, lines_to_add):
        if len(lines_to_add) != 0:
            print(len(lines_to_add), "new lines.")
            PROJECT_ID = self.PROJECT_ID
            DATASET_ID = self.DATASET_ID
            TABLE_ID = self.TABLE_ID
            for line in lines_to_add:
                client = bigquery.Client()
                errors = client.insert_rows_json(
                    f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", [line]
                )
                if errors:
                    print(str(errors))
        else:
            print("No new lines.")
