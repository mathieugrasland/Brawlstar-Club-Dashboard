import requests


class BS_helper():

    def __init__(self, token):
        self.url_api = "https://api.brawlstars.com/"
        self.url_v = "v1/"
        self.url = self.url_api + self.url_v
        self.token = token
        self.headers = {'Authorization': self.token}

    def get_club(self, club_tag):
        # Define the endpoint to use
        service = "clubs/"
        # Transform the club tag for api requierements
        club_tag = club_tag.replace("#", "%23")
        # URL to request
        url_request = self.url + service + club_tag
        # Make the request
        r = requests.get(
            url = url_request,
            headers = self.headers
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

    def get_club_league_matchs(self, name, tag, battlelog):
        lines = []
        for battle in battlelog:
            time = battle["battleTime"]
            battle_details = battle["battle"]
            #
            if 'type' in battle_details and battle_details['type'] == "teamRanked" and 'trophyChange' in battle_details:
                line = {}
                line["name"] = name
                line["tag"] = tag
                line["points"] = battle_details['trophyChange']
                line["mode"] = battle_details['mode']
                line["result"] = battle_details["result"]
                line["timestamp"] = time
                lines.append(line)
            elif 'mode' in battle_details and battle_details['mode'] != "soloShowdown" and battle_details['mode'] != "duoShowdown" and 'type' in battle_details and battle_details['type'] != 'challenge':
                if 'trophyChange' in battle_details and battle_details['trophyChange'] != 8 and battle_details['trophyChange'] > 0 and battle_details['trophyChange'] < 5:
                    line = {}
                    line["name"] = name
                    line["tag"] = tag
                    line["points"] = battle_details['trophyChange']
                    line["timestamp"] = time
                    line["mode"] = battle_details['mode']
                    line["result"] = battle_details["result"]
                    lines.append(line)
        return lines

    def only_new_lines(self, lines_to_add):
        # TODO OPEN EXISTING TABLE

        # TODO CHECK IF DUPLICATE

        return lines_to_add

    def upload_lines(self, lines_to_add):
        for line in lines_to_add:
            # TODO UPLOAD 1 LINE
            pass

