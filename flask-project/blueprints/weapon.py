from flask import Blueprint, render_template, request
from urllib.request import urlopen
import json

weapon = Blueprint('weapon', __name__)

WEAPON_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA"

SIDEARM_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA&type=sidearm"
SMG_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA&type=smg"
SHOTGUN_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA&type=shotgun"
RIFLES_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA&type=rifles"
SNIPER_URL = "http://127.0.0.1:5000/searchWeapon?apiKey=DMTiZnC5u_fuRXkbgtK_iA&type=sniper"

VIDEO_URL = "http://127.0.0.1:5000/video/weapon/{0}?apiKey=DMTiZnC5u_fuRXkbgtK_iA"

@weapon.route("/client/weapon")
def all_weapon():
    # Request sidearm
    sidearm_data = urlopen(SIDEARM_URL).read()
    parsed_sidearm = json.loads(sidearm_data)

    # Request smg
    smg_data = urlopen(SMG_URL).read()
    parsed_smg = json.loads(smg_data)

    # Request shotgun
    shotgun_data = urlopen(SHOTGUN_URL).read()
    parsed_shotgun = json.loads(shotgun_data)

    # Request rifles
    rifles_data = urlopen(RIFLES_URL).read()
    parsed_rifles = json.loads(rifles_data)

    # Request sniper
    sniper_data = urlopen(SNIPER_URL).read()
    parsed_sniper = json.loads(sniper_data)

    return render_template('weapon.html', all_sidearm=parsed_sidearm, all_smg=parsed_smg, all_shotgun=parsed_shotgun, all_rifles=parsed_rifles, all_sniper=parsed_sniper)

@weapon.route("/client/weapon/<int:id>")
def info_weapon(id):
    weapon_id = urlopen(WEAPON_URL+"&id="+str(id)).read()
    parsed_weapon = json.loads(weapon_id)

    video = urlopen(VIDEO_URL.format(id)).read()
    parsed_video = json.loads(video)

    return render_template('detail_weapon.html', weapon=parsed_weapon, weapon_video=parsed_video)

@weapon.route("/client/weapon/search", methods=["GET", "POST"])
def search_agent():
    if request.method == 'GET':
        return render_template("search_weapon.html")
    if request.method == 'POST':
        weapon_name = request.form.get('weaponName')
        weapon_type = request.form.get('weaponType')
        weapons = None
        print(weapon_type)
        if weapon_name:
            url = urlopen(WEAPON_URL+"&name="+weapon_name).read()
            weapons = json.loads(url)
            if weapons['totalResult'] == 0:
                return render_template("search_weapon.html")
        elif weapon_type:
            try:
                if weapon_type.lower() == "machine guns":
                    weapon_type = "machine%20guns"
                url = urlopen(WEAPON_URL+"&type="+weapon_type).read()
                weapons = json.loads(url)
            except:
                return render_template("search_weapon.html")
        return render_template("search_weapon.html", weapons=weapons)