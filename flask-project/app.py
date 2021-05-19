import io, requests, os, base64, valorant, json
from PIL import Image
from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from flask_basicauth import BasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from blueprints.api_key import api_key_name
from blueprints.home import home
from blueprints.agent import agent
from blueprints.weapon import weapon
from blueprints.map import map
from model import TFModel
from urllib.request import urlopen

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.register_blueprint(api_key_name)
app.register_blueprint(home)
app.register_blueprint(agent)
app.register_blueprint(weapon)
app.register_blueprint(map)

model = TFModel(model_dir='./ml-model/')
model.load()

api = Api(app, version='1.0', title='Valorant API',
          description='Valorant API',
          )
basic_auth = BasicAuth(app)

ns_search_agent = api.namespace('searchAgent', description='SEARCH AGENT operations')
ns_search_weapon = api.namespace('searchWeapon', description='SEARCH WEAPON operations')
ns_search_agent_video = api.namespace('video/agent/<int:id>', description='SEARCH AGENT VIDEO operations')
ns_search_weapon_video = api.namespace('video/weapon/<int:id>', description='SEARCH WEAPON VIDEO operations')
ns_search_map = api.namespace('searchMap', description='SEARCH MAP operations')
ns_ml_image = api.namespace('ml/agent', description='ML operations')

# Admin (POST, PUT, DELETE)
ns_edit_agent = api.namespace('agent', description='EDIT AGENT operations')
ns_edit_weapon = api.namespace('weapon', description='EDIT WEAPON operations')
ns_edit_map = api.namespace('map', description='EDIT MAP operations')

skill_detail_model = api.model('Skill detail', {
    "press": fields.String(required=True, example="Q", description="Key press for use skill"),
    "skillName": fields.String(required=True, example="UPDRAFT", description="Skill name"),
    "description": fields.String(required=True, example="พัดพา Jett ให้ลอยขึ้นไปบนอากาศทันที", description="Skill description"),
    "price": fields.Integer(required=False, example=100, description="Skill price"),
    "orbTotal": fields.Integer(required=False, example=6, description="Ultimate skill"),
    "volume": fields.Integer(required=False, example=2, description="Volume for use skill")
})

agent_skill_model = api.model('Agent skill', {
    "skill1": fields.Nested(skill_detail_model, required=True),
    "skill2": fields.Nested(skill_detail_model, required=True),
    "skill3": fields.Nested(skill_detail_model, required=True),
    "ultimateSkill": fields.Nested(skill_detail_model, required=True)
})

weapon_property_model = api.model('Weapon property', {
    "fireRate": fields.String(required=True, example="9.75 rds/sec", description="Weapon fire rate (rds/sec)"),
    "runSpeed": fields.String(required=True, example="5.4 m/sec", description="Agent run speed when hold weapon (m/sec)"),
    "equipSpeed": fields.String(required=True, example="1 sec", description="Weapon equip speed (sec)"),
    "firstShotSpread": fields.String(required=True, example="0.25/0.157 deg", description="1st shot spread (deg)"),
    "reloadSpeed": fields.String(required=True, example="2.5 sec", description="Weapon reload speed (sec)"),
    "magazine": fields.String(required=True, example="25 rds", description="Weapon magazine (rds)")
})
weapon_damage_agent_model = api.model('Weapon damage agent', {
    "head": fields.Integer(required=True, example=160, description="Head damage"),
    "body": fields.Integer(required=True, example=40, description="Body damage"),
    "leg": fields.Integer(required=True, example=34, description="Leg damage")
})
weapon_damage_model = api.model('Weapon damage', {
    "shortRange": fields.Nested(weapon_damage_agent_model, description="Short range damage", required=True),
    "intermediateRange": fields.Nested(weapon_damage_agent_model, description="Intermediate range damage", required=True),
    "longRange": fields.Nested(weapon_damage_agent_model, description="Long range damage", required=True)
})

agent_model = api.model('Agent', {
    "id": fields.Integer(required=True, example=100, description="Agent id"),
    "name": fields.String(required=True, example="Jett", description="Agent name"),
    "type": fields.String(required=True, example="Duelist", description="Agent type"),
    "biography": fields.String(required=True, example="เข้าร่วมรบในฐานะตัวแทนบ้านเกิดของเธอจากประเทศเกาหลีใต้ สไตล์การต่อสู้ที่แสนคล่องตัวและสง่างามของ Jett ทำให้เธอสามารถเผชิญหน้ากับความเสี่ยงในแบบที่ไม่มีใครทำได้ เธอวิ่งวนไปทั่วความชุลมุน เชือดเฉือนศัตรูก่อนที่พวกเขาจะรู้ว่าสิ่งใดได้โจมตีพวกเขา", description="Agent biography"),
    "image": fields.List(fields.String, required=True, description="Map image"),
    "specialSkills": fields.Nested(agent_skill_model, required=True)
})
weapon_model = api.model('Weapon', {
    "id": fields.Integer(required=True, example="212", description="Weapon id"),
    "name": fields.String(required=True, example="Vandal", description="Weapon name"),
    "type": fields.String(required=True, example="Rifles", description="Weapon type"),
    "price": fields.Integer(required=True, example="2900", description="Weapon price"),
    "image": fields.String(required=True, example="vandal.png", description="Weapon image"),
    "property": fields.Nested(weapon_property_model, description="Weapon property", required=True),
    "damage": fields.Nested(weapon_damage_model, description="Weapon damage", required=True)
})
agent_video_model = api.model('AgentVideo', {
    "id": fields.Integer(required=True, example=101, description="Agent id"),
    "trailer": fields.String(required=True, example="https://youtu.be/-cPLXswVsvc", description="Agent trailer video"),
    "tutorial": fields.String(required=True, example="https://youtu.be/ea-TCnB43iQ", description="Agent tutorial video")
})
weapon_video_model = api.model('WeaponVideo', {
    "id": fields.Integer(required=True, example=101, description="Weapon id"),
    "tutorial": fields.String(required=True, example="https://youtu.be/ea-TCnB43iQ", description="Weapon tutorial video")
})
map_model = api.model('Map', {
    "id": fields.Integer(required=True, example=301, description="Map id"),
    "name": fields.String(required=True, example="ASCENT", description="Map name"),
    "description": fields.String(required=True, example="ลานกว้างสำหรับสงครามยิ้บย้อยเพื่อชิงตำแหน่งและความได้เปรียบ ได้แยกสนามออกเป็นสองส่วนบน Ascent แต่ละจุดสามารถเสริมการป้องกันด้วยประตูระเบิดที่หมุนกลับไม่ได้ เมื่อประตูมันหล่นลงมาแล้ว คุณต้องทำลายมันหรือหาทางอื่น ยอมสละอาณาเขตให้น้อยที่สุดเท่าที่จะเป็นไปได้", description="Map description"),
    "recommendedComps": fields.List(fields.Integer, required=True, description="Agent recommend for map"),
    "image": fields.List(fields.String, required=True, description="Map image")
})

# Full model
search_agent_model = api.model('SearchAgent', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Result message", example="Success"),
    "totalResult" : fields.Integer(required=True, example=1, description="Total result of agent"),
    "result": fields.List(fields.Nested(agent_model), required=True, description="Agent result from search")
})
search_weapon_model = api.model('SearchWeapon', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Result message", example="Success"),
    "totalResult" : fields.Integer(required=False, example=1, description="Total result of weapon"),
    "result": fields.List(fields.Nested(weapon_model), required=False, description="Weapon result from search")
})
search_agent_video_model = api.model('SearchAgentVideo', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Result message", example="Success"),
    "totalResult" : fields.Integer(required=False, example=1, description="Total result of agent video"),
    "result": fields.List(fields.Nested(agent_video_model), required=False, description="Agent video result from search by id")
})
search_weapon_video_model = api.model('SearchWeaponVideo', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Result message", example="Success"),
    "totalResult" : fields.Integer(required=False, example=1, description="Total result of weapon video"),
    "result": fields.List(fields.Nested(weapon_video_model), required=False, description="Weapon video result from search by id")
})
search_map_model = api.model('SearchMap', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Result message", example="Success"),
    "totalResult" : fields.Integer(required=False, example=1, description="Total result of map"),
    "result": fields.List(fields.Nested(map_model), required=False, description="Map result from search")
})
edit_model = api.model('Edit', {
    "status": fields.Integer(required=True, example=200, description="Code status"),
    "message": fields.String(required=True, description="Edit message", example="Success")
})
ml_model = api.model('ML', {
    "prediction": fields.String(required=True, example="Jett", description="Predict result"),
    "confidence": fields.Float(required=True, example=0.99, description="ฉonfidence result")
})

@ns_search_agent.route('')
class SearchAgent(Resource):
    @ns_search_agent.doc('list_agent')
    @ns_search_agent.marshal_with(search_agent_model)
    def get(self):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "status": 401,
                "message": "Can't access because there is no API-Key",
                "totalResult": 0,
                "result": []
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "status": 401,
                    "message": "Can't access because there is wrong API-Key",
                    "totalResult": 0,
                    "result": []
                }, 401
        agent_id = request.args.get('id')
        name = request.args.get('name')
        agent_type = request.args.get('type')
        all_agent = valorant.read_agent_json()
        if agent_id:
            try:
                result = valorant.search_agent(id=int(agent_id))
                if result["status"] == 200:
                    return result, 200
                else:
                    return result, 500
            except:
                return {
                    "status": 500,
                    "message": "Not found agent id",
                    "totalResult": 0,
                    "result": []
                }, 500
        if agent_type:
            result = valorant.search_agent(type=agent_type)
            if result["status"] == 200:
                return result, 200
            else:
                return result, 500
        if name:
            result = valorant.search_agent(name=name)
            if result["status"] == 200:
                return result, 200
            else:
                return result, 500
        return {
            "status": 200,
            "message": "Success",
            "totalResult":len(all_agent),
            "result": all_agent
        }, 200

@ns_search_weapon.route('')
class SearchWeapon(Resource):
    @ns_search_weapon.doc('list_weapon')
    @ns_search_weapon.marshal_with(search_weapon_model)
    def get(self):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "status": 401,
                "message": "Can't access because there is no API-Key",
                "totalResult": 0,
                "result": []
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "status": 401,
                    "message": "Can't access because there is wrong API-Key",
                    "totalResult": 0,
                    "result": []
                }, 401
        weapon_id = request.args.get('id')
        name = request.args.get('name')
        type = request.args.get('type')
        sort_by_damage = request.args.get('sortByDamage')
        sort_by_price = request.args.get('sortByPrice')
        all_weapon = valorant.read_weapon_json()
        if sort_by_damage and type:
            result = valorant.search_weapon(sort_by_damage=sort_by_damage, type=type)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        if sort_by_damage:
            result = valorant.search_weapon(sort_by_damage=sort_by_damage)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        if sort_by_price and type:
            result = valorant.search_weapon(sort_by_price=sort_by_price, type=type)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        if sort_by_price:
            result = valorant.search_weapon(sort_by_price=sort_by_price)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        if weapon_id:
            try:
                result = valorant.search_weapon(id=int(weapon_id))
                if result['status'] == 200:
                    return result, 200
                else:
                    return result, 500
            except:
                return {
                    "status": 500,
                    "message": "Not found weapon id",
                    "totalResult": 0,
                    "result": []
                }, 500
        if name:
            result = valorant.search_weapon(name=name)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        if type:
            result = valorant.search_weapon(type=type)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        return {
            "status": 200,
            "message": "Success",
            "totalResult":len(all_weapon),
            "result": all_weapon
        }, 200

@ns_search_agent_video.route('')
class SearchAgentVideo(Resource):
    @ns_search_agent_video.doc('list_agent_video')
    @ns_search_agent_video.marshal_with(search_agent_video_model)
    def get(self, id):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "status": 401,
                "message": "Can't access because there is no API-Key",
                "totalResult": 0,
                "result": []
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "status": 401,
                    "message": "Can't access because there is wrong API-Key",
                    "totalResult": 0,
                    "result": []
                }, 401
        try:
            result = valorant.search_agent_video(int(id))
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
                return {
                    "status": 500,
                    "message": "Not found agent id",
                    "totalResult": 0,
                    "result": []
                }, 500

@ns_search_weapon_video.route('')
class SearchWeaponVideo(Resource):
    @ns_search_weapon_video.doc('list_weapon_video')
    @ns_search_weapon_video.marshal_with(search_weapon_video_model)
    def get(self, id):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "status": 401,
                "message": "Can't access because there is no API-Key",
                "totalResult": 0,
                "result": []
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "status": 401,
                    "message": "Can't access because there is wrong API-Key",
                    "totalResult": 0,
                    "result": []
                }, 401
        try:
            result = valorant.search_weapon_video(int(id))
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
                return {
                    "status": 500,
                    "message": "Not found weapon id",
                    "totalResult": 0,
                    "result": []
                }, 500

@ns_search_map.route('')
class SearchMap(Resource):
    @ns_search_map.doc('list_map')
    @ns_search_map.marshal_with(search_map_model)
    def get(self):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "status": 401,
                "message": "Can't access because there is no API-Key",
                "totalResult": 0,
                "result": []
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "status": 401,
                    "message": "Can't access because there is wrong API-Key",
                    "totalResult": 0,
                    "result": []
                }, 401
        id = request.args.get('id')
        name = request.args.get('name')
        agent_id = request.args.get('recommendAgentId')
        all_map = valorant.read_map_json()
        if agent_id:
            try:
                result = valorant.search_map(agent_id=int(agent_id))
                if result['status'] == 200:
                    return result, 200
                else:
                    return result, 500
            except:
                return {
                    "status": 500,
                    "message": "Not found agent id",
                    "totalResult": 0,
                    "result": []
                }, 500
        if id:
            try:
                result = valorant.search_map(id=int(id))
                if result['status'] == 200:
                    return result, 200
                else:
                    return result, 500
            except:
                return {
                    "status": 500,
                    "message": "Not found map id",
                    "totalResult": 0,
                    "result": []
                }, 500
        if name:
            result = valorant.search_map(name=name)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        return {
            "status": 200,
            "message": "Success",
            "totalResult":len(all_map),
            "result": all_map
        }, 200

@ns_edit_map.route('/<int:id>')
class EditMap(Resource):
    @basic_auth.required
    @ns_edit_map.doc('edit_map.json')
    @ns_edit_map.marshal_with(edit_model)
    def delete(self, id):
        try:
            result = valorant.delete_map(id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Delete failed because request body don't have map id or map id must be integer."
            }, 500

    @basic_auth.required
    @ns_edit_map.doc('edit_map.json')
    @ns_edit_map.marshal_with(edit_model)
    def put(self, id):
        try:
            map_data = api.payload
            result = valorant.update_map(map_data, id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Update failed because request body don't have map id or map id must be integer."
            }, 500

@ns_edit_weapon.route('/<int:id>')
class EditWeapon(Resource):
    @basic_auth.required
    @ns_edit_weapon.doc('edit_weapon.json')
    @ns_edit_weapon.marshal_with(edit_model)
    def delete(self, id):
        try:
            result = valorant.delete_weapon(id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Delete failed because request body don't have weapon id or weapon id must be integer."
            }, 500

    @basic_auth.required
    @ns_edit_weapon.doc('edit_weapon.json')
    @ns_edit_weapon.marshal_with(edit_model)
    def put(self, id):
        try:
            weapon_data = api.payload
            result = valorant.update_weapon(weapon_data, id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Update failed because request body don't have weapon id or weapon id must be integer."
            }, 500

@ns_edit_agent.route('/<int:id>')
class EditAgent(Resource):
    @basic_auth.required
    @ns_edit_agent.doc('edit_agent.json')
    @ns_edit_agent.marshal_with(edit_model)
    def delete(self, id):
        try:
            result = valorant.delete_agent(id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Delete failed because request body don't have agent id or agent id must be integer."
            }, 500

    @basic_auth.required
    @ns_edit_agent.doc('edit_agent.json')
    @ns_edit_agent.marshal_with(edit_model)
    def put(self, id):
        try:
            agent_data = api.payload
            result = valorant.update_agent(agent_data, id)
            if result['status'] == 200:
                return result, 200
            else:
                return result, 500
        except:
            return {
                "status": 500,
                "message": "Update failed because request body don't have agent id or agent id must be integer."
            }, 500

@ns_edit_agent.route('')
class AddAgent(Resource):
    @basic_auth.required
    @ns_edit_agent.doc('add_agent')
    @ns_edit_agent.marshal_with(edit_model)
    def post(self):
        agent_data = api.payload
        result = valorant.add_agent(agent_data)
        if result['status'] == 200:
            return result, 200
        else:
            return result, 500

@ns_edit_weapon.route('')
class AddWeapon(Resource):
    @basic_auth.required
    @ns_edit_weapon.doc('add_agent')
    @ns_edit_weapon.marshal_with(edit_model)
    def post(self):
        weapon_data = api.payload
        result = valorant.add_weapon(weapon_data)
        if result['status'] == 200:
            return result, 200
        else:
            return result, 500

@ns_edit_map.route('')
class AddMap(Resource):
    @basic_auth.required
    @ns_edit_weapon.doc('add_agent')
    @ns_edit_weapon.marshal_with(edit_model)
    def post(self):
        map_data = api.payload
        result = valorant.add_map(map_data)
        if result['status'] == 200:
            return result, 200
        else:
            return result, 500

@ns_ml_image.route('')
class MLAgent(Resource):
    @ns_ml_image.doc('')
    @ns_ml_image.marshal_with(ml_model)
    def post(self):
        api_key = request.args.get('apiKey')
        if not api_key:
            return {
                "prediction": "We cannot predict your image because there is no API-Key",
                "confidence": 0.0
            }, 401
        else:
            api_key_list = valorant.all_api_keys("apiKey.json")
            if api_key not in api_key_list['apiKey']:
                return {
                    "prediction": "We cannot predict your image because there is wrong API-Key.",
                    "confidence": 0.0
                }, 401
        try:

            image_data = base64.b64decode(api.payload['base64'])

            image_temp = Image.open(io.BytesIO(image_data))

            outputs = model.predict(image_temp)

            return {
                "prediction": outputs['predictions'][0]['label'],
                "confidence": outputs['predictions'][0]['confidence']
            }, 200
        except:
            return {
                "prediction": "Prediction failed because request body base64 missing",
                "confidence": 0.0
            }, 200

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