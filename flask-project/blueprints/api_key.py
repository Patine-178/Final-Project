from flask import Blueprint, render_template, request
import secrets, json, valorant

api_key_name = Blueprint('api_key_name', __name__)

@api_key_name.route('/key', methods=['GET','POST'])
def api_key():
    if request.method == 'GET':
        return render_template("api.html")
    if request.method == 'POST':
        key = secrets.token_urlsafe(16)
        valorant.add_api_key("apiKey.json", key)
        return render_template("api.html", key=key)

@api_key_name.route('/allKey')
def all_api_key():
    api_key_data = valorant.all_api_keys("apiKey.json")
    return api_key_data