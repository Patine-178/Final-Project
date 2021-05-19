import requests, base64, json
from PIL import Image
from flask import Flask, request, render_template
from blueprints.home import home
from blueprints.agent import agent
from blueprints.weapon import weapon
from blueprints.map import map
from urllib.request import urlopen

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(agent)
app.register_blueprint(weapon)
app.register_blueprint(map)

@app.route('/client/agent/AI',methods=['GET', 'POST'] )
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']

        base64_encoded_data = base64.b64encode(file1.read())
        base64_message = base64_encoded_data.decode('utf-8')

        url = "http://127.0.0.1:5000/ml/agent?apiKey=t7_PoBODfDGpYiDPvBl_aw"
        body = {
            'base64': base64_message
        }

        prediction = requests.post(url, json = body)
        url = urlopen("http://127.0.0.1:5000/searchAgent?apiKey=t7_PoBODfDGpYiDPvBl_aw&name="+prediction.json()['prediction']).read()
        parsed_agent = json.loads(url)

        return render_template('agent_prediction.html', agent=parsed_agent)

    return render_template('agent_prediction.html')