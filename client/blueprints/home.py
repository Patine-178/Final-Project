from flask import Blueprint, render_template
from urllib.request import urlopen
import json

home = Blueprint('home', __name__)

VALORANT_WEAPON_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA"
VALORANT_AGENT_URL = "http://127.0.0.1:5000/searchAgent?apiKey=DMTiZnC5u_fuRXkbgtK_iA"
VALORANT_MAP_URL = "http://127.0.0.1:5000/searchMap?apiKey=DMTiZnC5u_fuRXkbgtK_iA"

@home.route("/client/home")
def index():
    # Request Agent
    agent_data = urlopen(VALORANT_AGENT_URL).read()
    parsed_agent = json.loads(agent_data)

    # Request weapon
    weapon_data = urlopen(VALORANT_WEAPON_URL).read()
    parsed_weapon = json.loads(weapon_data)
    
    # Request Map
    map_data = urlopen(VALORANT_MAP_URL).read()
    parsed_map = json.loads(map_data)

    return render_template('index.html', all_weapon=parsed_weapon, all_agent=parsed_agent, all_map=parsed_map)