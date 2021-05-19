from flask import Blueprint, render_template, request
from urllib.request import urlopen
import json

agent = Blueprint('agent', __name__)

VALORANT_AGENT_URL = "http://127.0.0.1:5000/searchAgent?apiKey=DMTiZnC5u_fuRXkbgtK_iA"
VIDEO_URL = "http://127.0.0.1:5000/video/agent/{0}?apiKey=DMTiZnC5u_fuRXkbgtK_iA"

@agent.route("/client/agent")
def agent_all():
    # Request Agent
    agent_data = urlopen(VALORANT_AGENT_URL).read()
    parsed_agent = json.loads(agent_data)
    return render_template('agent.html', all_agent=parsed_agent)

@agent.route("/client/agent/<int:id>")
def info_agent(id):
    agent_id = urlopen(VALORANT_AGENT_URL+"&id="+str(id)).read()
    parsed_agent = json.loads(agent_id)

    video = urlopen(VIDEO_URL.format(id)).read()
    parsed_video = json.loads(video)

    return render_template('detail_agent.html', agent=parsed_agent, agent_video=parsed_video)

@agent.route("/client/agent/search", methods=["GET", "POST"])
def search_agent():
    if request.method == 'GET':
        return render_template("search_agent.html")
    if request.method == 'POST':
        agent_name = request.form.get('agentName')
        agent_type = request.form.get('agentType')
        agents = None
        if agent_name:
            url = urlopen(VALORANT_AGENT_URL+"&name="+agent_name).read()
            agents = json.loads(url)
            if agents['totalResult'] == 0:
                return render_template("search_agent.html")
        elif agent_type:
            try:
                url = urlopen(VALORANT_AGENT_URL+"&type="+agent_type).read()
                agents = json.loads(url)
            except:
                return render_template("search_agent.html")
        return render_template("search_agent.html", agents=agents)