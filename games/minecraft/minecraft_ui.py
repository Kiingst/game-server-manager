from flask import Blueprint, render_template, request, jsonify
from Server_manager import server_Managers
from games.minecraft.Minecraft import Minecraft_server


#TODO 
# add creating a server
# each server is a different ID

minecraft_Blueprint = Blueprint("minecraft", __name__)

serv_Man = server_Managers("minecraft")

@minecraft_Blueprint.route("/")
def index():
    return render_template("index.html")

@minecraft_Blueprint.route("/start", methods=["POST"])
def start():
    serv_Man.active_server.start()
    return jsonify({"status": "started"})

@minecraft_Blueprint.route("/stop", methods=["POST"])
def stop():
    serv_Man.active_server.stop()
    return jsonify({"status": "stopped"})

@minecraft_Blueprint.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    if "command" in data:
        serv_Man.active_server.send_command(data["command"])
        return jsonify({"status": f"Command sent: {data['command']}"})
    return jsonify({"error": "No command provided"}), 400

@minecraft_Blueprint.route("/get_servers")
def get_servers():

    return {
        "message" : ", ".join(serv_Man.servers.keys()),

    }, 200

@minecraft_Blueprint.route("/set_server", methods=["POST"])
def set_server():
    data = request.get_json()

    global server
    print(data["name"])
    print(serv_Man.servers)
    if "name" in data and serv_Man.does_server_exist(data["name"]):
        serv_Man.active_server = serv_Man.get_server(data["name"])
        return {"message": f"Server '{data['name']}' set successfully"}, 200
    else:
        return {"error": "Server does not exist or name not provided"}, 400
    

@minecraft_Blueprint.route("/create-server", methods=["POST"])
def create_server():
    data = request.get_json()
    x = {}

    x["name"] = data["name"]
    x["config"] = data["config"]

    Minecraft_server(x["name"], serv_Man, x["config"])

    return {
        "message" : f"added server {x}"
    }, 200




#FLOW
# create the server in mincraft ui
# u give it to server manager
# that server manager then saves all server locations and data to its own json file
#