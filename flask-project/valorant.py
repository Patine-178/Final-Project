import json

# Agent function
def read_agent_json():
    open_json_file = open('agent.json', 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    agent_data = json.loads(read_json_file)

    return agent_data

def search_agent(type=None, name=None, id=None):
    all_agent = read_agent_json()
    if id:
        for agent_dict in all_agent:
            if agent_dict['id'] == id:
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult": 1,
                    "result": [agent_dict]
                }
        return {
            "status": 500,
            "message": "Not found agent id",
            "totalResult": 0,
            "result": []
        }
    if name:
        for agent_dict in all_agent:
            if agent_dict['name'].lower() == name.lower():
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult": 1,
                    "result": [agent_dict]
                }
        return {
            "status": 500,
            "message": "Not found agent name",
            "totalResult": 0,
            "result": []
        }
    if type:
        agent_list = []
        for agent_dict in all_agent:
            if agent_dict['type'].lower() == type.lower():
                agent_list.append(agent_dict)
        if len(agent_list) != 0:
            return {
                "status": 200,
                "message": "Success",
                "totalResult": len(agent_list),
                "result": agent_list
            }
        else:
            return {
                "status": 500,
                "message": "Not found agent type",
                "totalResult": 0,
                "result": []
            }

def delete_agent(id):
    agent_list = read_agent_json()
    agent_video_list = read_agent_video_json()
    agent_recommend = read_map_json()
    
    # Delete agent.json
    for agent_dict in agent_list:
        if agent_dict['id'] == id:
            agent_list.remove(agent_dict)
            open_json_file = open('agent.json', 'w', encoding='utf-8')
            json.dump(agent_list, open_json_file, indent=4, ensure_ascii=False)
            
            # Delete agent_video.json
            for agent_video_dict in agent_video_list:
                if agent_video_dict['id'] == id:
                    agent_video_list.remove(agent_video_dict)
                    open_json_file = open('agent_video.json', 'w', encoding='utf-8')
                    json.dump(agent_video_list, open_json_file, indent=4, ensure_ascii=False)
                    break
            
            # Delete agent in map.json
            for index, map_dict in enumerate(agent_recommend):
                if id in map_dict['recommendedComps']:
                    agent_recommend[index]["recommendedComps"].remove(id)
            open_json_file = open('map.json', 'w', encoding='utf-8')
            json.dump(agent_recommend, open_json_file, indent=4, ensure_ascii=False)

            return {
                "status": 200,
                "message": "Agent has been deleted."
            }

    return {
        "status": 500,
        "message": "Delete failed because agent id not found."
    }

def update_agent(data, id):
    agent_list = read_agent_json()
    for index_agent, agent_dict in enumerate(agent_list):
        if agent_dict['id'] == id:
            result =  all(elem in list(agent_dict.keys()) for elem in list(data.keys()))
            if result:
                agent_list[index_agent].update(data)
                open_json_file = open('agent.json', 'w', encoding='utf-8')
                json.dump(agent_list, open_json_file, indent=4, ensure_ascii=False)
                return {
                    "status": 200,
                    "message": "Agent has been updated."
                }
            else:
                special_skills = all(elem in list(agent_dict['specialSkills'].keys()) for elem in list(data.keys()))
                
                agent_video_list = read_agent_video_json()

                if special_skills:
                    agent_list[index_agent]['specialSkills'].update(data)
                    open_json_file = open('agent.json', 'w', encoding='utf-8')
                    json.dump(agent_list, open_json_file, indent=4, ensure_ascii=False)
                    return {
                        "status": 200,
                        "message": "Agent has been updated."
                    }

                video = all(elem in list(agent_video_list[0].keys()) for elem in list(data.keys()))

                if video:
                    for index_video, agent_video_dict in enumerate(agent_video_list):
                        if agent_video_dict['id'] == id:
                            agent_video_list[index_video].update(data)
                            open_json_file = open('agent_video.json', 'w', encoding='utf-8')
                            json.dump(agent_video_list, open_json_file, indent=4, ensure_ascii=False)
                            return {
                                "status": 200,
                                "message": "Agent video has been updated."
                            }

                return {
                    "status": 500,
                    "message": "Update failed because request body have wrong key."
                }
    return {
        "status": 500,
        "message": "Update failed because agent id not found."
    }

def add_agent(data):
    agent_list = read_agent_json()
    new_id = sorted(agent_list, reverse=True, key= lambda agent: agent["id"])[0]['id'] + 1
    key1_list = list(agent_list[0].keys())
    key1_list.remove("id")
    new_dict = dict()

    agent_video_list = read_agent_video_json()
    video_key_list = list(agent_video_list[0].keys())

    # Add weapon
    if key1_list == list(data.keys()):
        key_skills_list = list(agent_list[0]["specialSkills"].keys())
        if key_skills_list == list(data['specialSkills'].keys()):
            key_skill_detail_list = list(agent_list[0]["specialSkills"]['skill1'].keys())
            key_ult_detail_list = list(agent_list[0]["specialSkills"]['ultimateSkill'].keys())
            if key_skill_detail_list == list(data['specialSkills']['skill1'].keys()) and key_skill_detail_list == list(data['specialSkills']['skill2'].keys()) and key_skill_detail_list == list(data['specialSkills']['skill3'].keys()) and key_ult_detail_list == list(data['specialSkills']['ultimateSkill'].keys()):
                new_dict.update({"id": new_id})
                new_dict.update(data)
                agent_list.append(new_dict)
                open_json_file = open('agent.json', 'w', encoding='utf-8')
                json.dump(agent_list, open_json_file, indent=4, ensure_ascii=False)
                return {
                    "status": 200,
                    "message": "Agent has been add."
                }
            else:
                return {
                    "status": 500,
                    "message":"Add agent failed because keys in skill is missing."
                }
        else:
            return {
                "status": 500,
                "message":"Add agent failed because keys in specialSkills is missing."
            }
    # Add weapon video   
    elif video_key_list == list(data.keys()):
        result = search_agent(id=data['id'])
        if result['status'] == 500:
            return {
                "status": 500,
                "message": "Add agent failed because agent id not in agent.json."
            }
        else:
            result = search_agent_video(data['id'])
            if result['status'] == 200:
                return {
                    "status": 500,
                    "message": "Add agent failed because agent id is duplicate."
                }
            agent_video_list.append(data)
            open_json_file = open('agent_video.json', 'w', encoding='utf-8')
            json.dump(agent_video_list, open_json_file, indent=4, ensure_ascii=False)
            return {
                "status": 200,
                "message": "Agent video has been add."
            }

    return {
        "status": 500,
        "message": "Add agent failed because the number of keys is missing."
    }

# Weapon function
def read_weapon_json():
    open_json_file = open('weapon.json', 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    weapon_data = json.loads(read_json_file)

    return weapon_data

def search_weapon(id=None, name=None, type=None, sort_by_damage=None, sort_by_price=None):
    all_weapon = read_weapon_json()
    if sort_by_damage and type:
            weapon_list = []
            for weapon_dict in all_weapon:
                if weapon_dict['type'].lower() == type.lower():
                    weapon_list.append(weapon_dict)
            if len(weapon_list) == 0:
                return {
                    "status": 500,
                    "message": "Not found weapon type",
                    "totalResult": 0,
                    "result": []
                }
            if sort_by_damage.lower() == 'desc':
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":len(weapon_list),
                    "result": sorted(weapon_list, reverse=True, key= lambda weapon: weapon["damage"]["shortRange"]["head"])
                }
            if sort_by_damage.lower() == 'asc':
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":len(weapon_list),
                    "result": sorted(weapon_list, reverse=False, key= lambda weapon: weapon["damage"]["shortRange"]["head"])
                }
            else:
                return {
                    "status": 500,
                    "message": "Wrong sort parameter. Please use only DESC or ASC",
                    "totalResult": 0,
                    "result": []
                }
    if sort_by_damage:
        if sort_by_damage.lower() == 'desc':
            return {
                "status": 200,
                "message": "Success",
                "totalResult":len(all_weapon),
                "result": sorted(all_weapon, reverse=True, key= lambda weapon: weapon["damage"]["shortRange"]["head"])
            }
        if sort_by_damage.lower() == 'asc':
            return {
                "status": 200,
                "message": "Success",
                "totalResult":len(all_weapon),
                "result": sorted(all_weapon, reverse=False, key= lambda weapon: weapon["damage"]["shortRange"]["head"])
            }
        else:
            return {
                "status": 500,
                "message": "Wrong sort parameter. Please use only DESC or ASC",
                "totalResult": 0,
                "result": []
            }
    if sort_by_price and type:
            weapon_list = []
            for weapon_dict in all_weapon:
                if weapon_dict['type'].lower() == type.lower():
                    weapon_list.append(weapon_dict)
            if len(weapon_list) == 0:
                return {
                    "status": 500,
                    "message": "Not found weapon type",
                    "totalResult": 0,
                    "result": []
                }
            if sort_by_price.lower() == 'desc':
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":len(weapon_list),
                    "result": sorted(weapon_list, reverse=True, key= lambda weapon: weapon["price"])
                }
            if sort_by_price.lower() == 'asc':
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":len(weapon_list),
                    "result": sorted(weapon_list, reverse=False, key= lambda weapon: weapon["price"])
                }
            else:
                return {
                    "status": 500,
                    "message": "Wrong sort parameter. Please use only DESC or ASC",
                    "totalResult": 0,
                    "result": []
                }
    if sort_by_price:
        if sort_by_price.lower() == 'desc':
            return {
                "status": 200,
                "message": "Success",
                "totalResult":len(all_weapon),
                "result": sorted(all_weapon, reverse=True, key= lambda weapon: weapon["price"])
            }
        if sort_by_price.lower() == 'asc':
            return {
                "status": 200,
                "message": "Success",
                "totalResult":len(all_weapon),
                "result": sorted(all_weapon, reverse=False, key= lambda weapon: weapon["price"])
            }
        else:
            return {
                "status": 500,
                "message": "Wrong sort parameter. Please use only DESC or ASC",
                "totalResult": 0,
                "result": []
            }
    if id:
        for weapon_dict in all_weapon:
            if weapon_dict['id'] == id:
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":1,
                    "result": [weapon_dict]
                }
        return {
            "status": 500,
            "message": "Not found weapon id",
            "totalResult": 0,
            "result": []
        }
    if name:
        for weapon_dict in all_weapon:
            if weapon_dict['name'].lower() == name.lower():
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":1,
                    "result": [weapon_dict]
                }
        return {
            "status": 500,
            "message": "Not found weapon name",
            "totalResult": 0,
            "result": []
        }
    if type:
        weapon_list = []
        for weapon_dict in all_weapon:
            if weapon_dict['type'].lower() == type.lower():
                weapon_list.append(weapon_dict)
        if len(weapon_list) != 0:
            return {
                "status": 200,
                "message": "Success",
                "totalResult": len(weapon_list),
                "result": weapon_list
            }
        else:
            return {
                "status": 500,
                "message": "Not found weapon type",
                "totalResult": 0,
                "result": []
            }

def delete_weapon(id):
    weapon_list = read_weapon_json()
    weapon_video_list = read_weapon_video_json()
    
    # Delete weapon.json
    for weapon_dict in weapon_list:
        if weapon_dict['id'] == id:
            weapon_list.remove(weapon_dict)
            open_json_file = open('weapon.json', 'w', encoding='utf-8')
            json.dump(weapon_list, open_json_file, indent=4, ensure_ascii=False)
            
            # Delete weapon_video.json
            for weapon_video_dict in weapon_video_list:
                if weapon_video_dict['id'] == id:
                    weapon_video_list.remove(weapon_video_dict)
                    open_json_file = open('weapon_video.json', 'w', encoding='utf-8')
                    json.dump(weapon_video_list, open_json_file, indent=4, ensure_ascii=False)
                    return {
                        "status": 200,
                        "message": "Weapon has been deleted."
                    }
            
            return {
                "status": 200,
                "message": "Weapon has been deleted."
            }

    return {
        "status": 500,
        "message": "Delete failed because weapon id not found."
    }

def update_weapon(data, id):
    weapon_list = read_weapon_json()
    for index_weapon, weapon_dict in enumerate(weapon_list):
        if weapon_dict['id'] == id:
            result =  all(elem in list(weapon_dict.keys()) for elem in list(data.keys()))
            if result:
                weapon_list[index_weapon].update(data)
                open_json_file = open('weapon.json', 'w', encoding='utf-8')
                json.dump(weapon_list, open_json_file, indent=4, ensure_ascii=False)
                return {
                    "status": 200,
                    "message": "Weapon has been updated."
                }
            else:
                property = all(elem in list(weapon_dict['property'].keys()) for elem in list(data.keys()))
                damage = all(elem in list(weapon_dict['damage'].keys()) for elem in list(data.keys()))
                
                weapon_video_list = read_weapon_video_json()

                if property:
                    weapon_list[index_weapon]['property'].update(data)
                    open_json_file = open('weapon.json', 'w', encoding='utf-8')
                    json.dump(weapon_list, open_json_file, indent=4, ensure_ascii=False)
                    return {
                        "status": 200,
                        "message": "Weapon has been updated."
                    }
                if damage:
                    weapon_list[index_weapon]['damage'].update(data)
                    open_json_file = open('weapon.json', 'w', encoding='utf-8')
                    json.dump(weapon_list, open_json_file, indent=4, ensure_ascii=False)
                    return {
                        "status": 200,
                        "message": "Weapon has been updated."
                    }

                video = all(elem in list(weapon_video_list[0].keys()) for elem in list(data.keys()))

                if video:
                    for index_video, weapon_video_dict in enumerate(weapon_video_list):
                        if weapon_video_dict['id'] == id:
                            weapon_video_list[index_video].update(data)
                            open_json_file = open('weapon_video.json', 'w', encoding='utf-8')
                            json.dump(weapon_video_list, open_json_file, indent=4, ensure_ascii=False)
                            return {
                                "status": 200,
                                "message": "Weapon has been updated."
                            }

                return {
                    "status": 500,
                    "message": "Update failed because request body have wrong key."
                }
    return {
        "status": 500,
        "message": "Update failed because weapon id not found."
    }

def add_weapon(data):
    weapon_list = read_weapon_json()
    new_id = sorted(weapon_list, reverse=True, key= lambda weapon: weapon["id"])[0]['id'] + 1
    key1_list = list(weapon_list[0].keys())
    key1_list.remove("id")
    new_dict = dict()

    weapon_video_list = read_weapon_video_json()
    video_key_list = list(weapon_video_list[0].keys())

    # Add weapon
    if key1_list == list(data.keys()):
        key_property_list = list(weapon_list[0]["property"].keys())
        if key_property_list == list(data['property'].keys()):
            key_damage_list = list(weapon_list[0]["damage"].keys())
            key_damage_agent_list = list(weapon_list[0]["damage"]['shortRange'].keys())
            if key_damage_list == list(data['damage'].keys()) and key_damage_agent_list == list(data['damage']['shortRange'].keys()) and key_damage_agent_list == list(data['damage']['intermediateRange'].keys()) and key_damage_agent_list == list(data['damage']['longRange'].keys()):
                new_dict.update({"id": new_id})
                new_dict.update(data)
                weapon_list.append(new_dict)
                open_json_file = open('weapon.json', 'w', encoding='utf-8')
                json.dump(weapon_list, open_json_file, indent=4, ensure_ascii=False)
                return {
                    "status": 200,
                    "message": "Weapon has been add."
                }
            else:
                return {
                    "status": 500,
                    "message":"Add weapon failed because keys in damage or range is missing."
                }
        else:
            return {
                "status": 500,
                "message":"Add weapon failed because keys in property is missing."
            }
    # Add weapon video   
    elif video_key_list == list(data.keys()):
        result = search_weapon(id=data['id'])
        if result['status'] == 500:
            return {
                "status": 500,
                "message": "Add weapon failed because weapon id not in weapon.json."
            }
        else:
            result = search_weapon_video(data['id'])
            if result['status'] == 200:
                return {
                    "status": 500,
                    "message": "Add weapon failed because weapon id is duplicate."
                }
            weapon_video_list.append(data)
            open_json_file = open('weapon_video.json', 'w', encoding='utf-8')
            json.dump(weapon_video_list, open_json_file, indent=4, ensure_ascii=False)
            return {
                "status": 200,
                "message": "Weapon video has been add."
            }

    return {
        "status": 500,
        "message": "Add weapon failed because the number of keys is missing."
    }

# Map function
def read_map_json():
    open_json_file = open('map.json', 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    map_data = json.loads(read_json_file)

    return map_data

def search_map(id=None, name=None, agent_id=None):
    map_list = read_map_json()
    if id:
        for map_dict in map_list:
            if map_dict['id'] == id:
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":1,
                    "result": [map_dict]
                }
        return {
                "status": 500,
                "message": "Not found map id",
                "totalResult": 0,
                "result": []
            }
    if name:
        for map_dict in map_list:
            if map_dict['name'].lower() == name.lower():
                return {
                    "status": 200,
                    "message": "Success",
                    "totalResult":1,
                    "result": [map_dict]
                }
        return {
                "status": 500,
                "message": "Not found map name",
                "totalResult": 0,
                "result": []
            }
    if agent_id:
        some_map_list = []
        for map_dict in map_list:
            if agent_id in map_dict['recommendedComps']:
                some_map_list.append(map_dict)
        if len(some_map_list) != 0:
            return {
                "status": 200,
                "message": "Success",
                "totalResult": len(some_map_list),
                "result": some_map_list
            }
        else:
            return {
                "status": 500,
                "message": "Not found agent id",
                "totalResult": 0,
                "result": []
            }

def delete_map(id):
    map_list = read_map_json()
    for map_dict in map_list:
        if map_dict['id'] == id:
            map_list.remove(map_dict)
            open_json_file = open('map.json', 'w', encoding='utf-8')
            json.dump(map_list, open_json_file, indent=4, ensure_ascii=False)
            return {
                "status": 200,
                "message": "Map has been deleted."
            }
    return {
        "status": 500,
        "message": "Delete failed because map id not found."
    }

def update_map(data, id):
    map_list = read_map_json()
    for index, map_dict in enumerate(map_list):
        if map_dict['id'] == id:
            result =  all(elem in list(map_dict.keys()) for elem in list(data.keys()))
            if result:
                map_list[index].update(data)
                open_json_file = open('map.json', 'w', encoding='utf-8')
                json.dump(map_list, open_json_file, indent=4, ensure_ascii=False)
                return {
                    "status": 200,
                    "message": "Map has been updated."
                }
            else:
                return {
                    "status": 500,
                    "message": "Update failed because request body have wrong key."
                }
    return {
        "status": 500,
        "message": "Update failed because map id not found."
    }

def add_map(data):
    map_list = read_map_json()
    new_id = sorted(map_list, reverse=True, key= lambda map: map["id"])[0]['id'] + 1
    key_list = list(map_list[0].keys())
    key_list.remove("id")
    new_dict = dict()
    if key_list == list(data.keys()):
        for id in data['recommendedComps']:
            result = search_agent(id=id)
            if result['status'] == 500:
                return {
                    "status": 500,
                    "message": "Add map failed because agent id in recommendedComps not in agent.json."
                }
        new_dict.update({"id": new_id})
        new_dict.update(data)
        map_list.append(new_dict)
        open_json_file = open('map.json', 'w', encoding='utf-8')
        json.dump(map_list, open_json_file, indent=4, ensure_ascii=False)
        return {
            "status": 200,
            "message": "Map has been add."
        }
    return {
        "status": 500,
        "message": "Add map failed because the number of keys is missing."
    }

# API-Key function
def all_api_keys(path):
    open_json_file = open(path, 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    api_key_data = json.loads(read_json_file)

    return api_key_data

def add_api_key(path, new_key):
    api_data = all_api_keys(path)
    api_data["apiKey"].append(new_key)

    open_json_file = open(path, 'w')
    json.dump(api_data, open_json_file, indent=4)

# Agent video function
def read_agent_video_json():
    open_json_file = open('agent_video.json', 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    agent_video_data = json.loads(read_json_file)

    return agent_video_data

def search_agent_video(id):
    video_list = read_agent_video_json()
    for video_dict in video_list:
        if video_dict['id'] == id:
            return {
                "status": 200,
                "message": "Success",
                "totalResult": 1,
                "result": [video_dict]
            } 
    return {
        "status": 500,
        "message": "Not found agent id from path",
        "totalResult": 0,
        "result": []
    }

# Weapon video function
def read_weapon_video_json():
    open_json_file = open('weapon_video.json', 'r', encoding='utf-8')
    read_json_file = open_json_file.read()

    weapon_video_data = json.loads(read_json_file)

    return weapon_video_data

def search_weapon_video(id):
    video_list = read_weapon_video_json()
    for video_dict in video_list:
        if video_dict['id'] == id:
            return {
                "status": 200,
                "message": "Success",
                "totalResult": 1,
                "result": [video_dict]
            } 
    return {
        "status": 500,
        "message": "Not found weapon id from path",
        "totalResult": 0,
        "result": []
    }