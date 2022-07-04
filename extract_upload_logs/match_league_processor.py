from datetime import datetime, timedelta
import pytz


def get_brawler(tag, line, battle_details):
    brawler = "BRAWLER ERROR"
    if 'teams' in battle_details:
        teams = battle_details["teams"]
        for team in teams:
            for player in team:
                if tag == player["tag"]:
                    brawler = player["brawler"]["name"]
        brawler = brawler.replace("\n", " ")
        line["brawler"] = brawler
    return line


def current_season():
    tz = pytz.timezone("Europe/Paris")
    now = datetime.now(tz=tz) + timedelta(days=-1)
    # WEEK 18 OF YEAR 2022 TO BE THE SAISON 0 OF THE RECORDS
    current = "Saison " + str(int(now.strftime("%Y%W")) - 202218)
    return current


def get_season(line, time):
    date_parsed = datetime.strptime(time, '%Y%m%dT%H%M%S.%fZ') + timedelta(days=-1)
    # WEEK 18 OF YEAR 2022 TO BE THE SAISON 0 OF THE RECORDS
    line["season"] = "Saison " + str(int(date_parsed.strftime("%Y%W")) - 202218)
    return line


def get_day(line, time):
    day = "DAY ERROR"
    date_parsed = datetime.strptime(time, '%Y%m%dT%H%M%S.%fZ')
    weekday = date_parsed.strftime("%A")
    if weekday in ['Wednesday', 'Thursday']:
        day = "J1"
    if weekday in ['Friday', 'Saturday']:
        day = "J2"
    if weekday in ['Sunday', 'Monday']:
        day = "J3"
    line["day"] = day
    return line


def get_datetime(line, time):
    line["datetime"] = time[0:4] + "-" + time[4:6] + "-" + time[6:11] + ":" + time[11:13] + ":" + time[13:19]
    return line


def get_seasonday(line):
    line["seasonday"] = line["season"] + " " + line["day"]
    return line


def get_player(line, name, tag):
    line["name"] = name
    line["tag"] = tag
    return line


def get_timestamp(line, time):
    line["timestamp"] = time
    return line


def get_match_details(line, battle_details):
    if "trophyChange" in battle_details:
        line["points"] = battle_details['trophyChange']
    line["mode"] = battle_details['mode']
    if "result" in battle_details:
        line["result"] = battle_details["result"]
    if "type" in battle_details:
        line["type"] = battle_details["type"]
    return line


def get_map(line, event):
    line["map_id"] = str(event["id"])
    line["map_name"] = event["map"]
    return line


def get_starplayer(line, tag, battle_details):
    is_sp = False
    if "starPlayer" in battle_details and battle_details["starPlayer"] is not None:
        starplayer = battle_details["starPlayer"]
        tag_starplayer = starplayer["tag"]
        is_sp = tag == tag_starplayer
    line["starplayer"] = is_sp
    return line
