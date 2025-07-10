from flask import Blueprint, render_template, request, jsonify
from Server_manager import server_Manager

minecraft_Blueprint = Blueprint("minecraft", __name__)

serv_Man = server_Manager()
server = None

@minecraft_Blueprint.route("/")
def index():
    return render_template("index.html")

@minecraft_Blueprint.route("/start", methods=["POST"])
def start():
    server.start()
    return jsonify({"status": "started"})

@minecraft_Blueprint.route("/stop", methods=["POST"])
def stop():
    server.stop()
    return jsonify({"status": "stopped"})

@minecraft_Blueprint.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    if "command" in data:
        server.send_command(data["command"])
        return jsonify({"status": f"Command sent: {data['command']}"})
    return jsonify({"error": "No command provided"}), 400

@minecraft_Blueprint.route("/set_server", methods=["POST"])
def set_server():
    data = request.get_json()
    global server
    if "name" in data:
        server = serv_Man.get_server(data["name"])