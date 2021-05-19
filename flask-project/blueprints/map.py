from flask import Blueprint, render_template, request
from urllib.request import urlopen
import json

map = Blueprint('map', __name__)

VALORANT_MAP_URL = "http://127.0.0.1:5000/searchMap?apiKey=DMTiZnC5u_fuRXkbgtK_iA"
VALORANT_AGENT_URL = "http://127.0.0.1:5000/searchAgent?apiKey=DMTiZnC5u_fuRXkbgtK_iA&id={0}"

@map.route("/client/map")
def all_map():
    # Request Map
    map_data = urlopen(VALORANT_MAP_URL).read()
    parsed_map = json.loads(map_data)

    return render_template('map.html', all_map=parsed_map)

@map.route("/client/map/<int:id>")
def info_map(id):
    # Request Map
    map_data = urlopen(VALORANT_MAP_URL+"&id="+str(id)).read()
    parsed_map = json.loads(map_data)

    agent_list = []
    for agent_id in parsed_map['result'][0]['recommendedComps']:
        agent_data = urlopen(VALORANT_AGENT_URL.format(agent_id)).read()
        parsed_agent = json.loads(agent_data)
        agent_list.append(parsed_agent['result'][0])

    return render_template('detail_map.html', map=parsed_map, agents=agent_list, agent_total=len(agent_list))