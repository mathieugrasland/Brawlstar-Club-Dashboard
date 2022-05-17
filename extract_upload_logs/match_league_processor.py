from datetime import datetime, timedelta


def get_brawler(tag, line, battle_details):
    brawler = "BRAWLER ERROR"
    if 'teams' in battle_details:
        teams = battle_details["teams"]
        for team in teams:
            for player in team:
                if tag == player["tag"]:
                    brawler = player["brawler"]["name"]
        line["brawler"] = brawler
    return line


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
    return line
