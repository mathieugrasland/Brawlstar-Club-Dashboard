from flask import Flask
from pprint import pprint

import json
config = json.load(open("config.json"))
token = config["BS_token"]

from api.BS_helper import BS_helper
app = Flask(__name__)



@app.route('/')
def hello_world():
    BS = BS_helper(token)
    club_tag = "#YPQ9UGU"
    tag = "#L0VRP2G9"
    test = BS.get_tag_to_name(club_tag)
    pprint(test)
    return str(test)

if __name__ == "__main__":
    app.run()