import os
import json
import sqlite3
#from games.minecraft.minecraft_ui import minecraft_Blueprint
from flask import Flask, render_template, request, jsonify, send_file, Blueprint
from pathlib import Path
from server_manager.server_manager import Minecraft_Server_Manager

#An ALL in one video game server manager that can take config files and change how it acts depending on the game



#TODO RIGHT NOT Website UI for Servers
#EACH server needs a coroponding webpage where you can start stop and delete servers
#Home page lets you create servers


#TODO
#later
 #EDIT CONFIG FILES
#LIVE SERVER CONSOLE

#DONE
#CREATE AND START SERVER
#START STOP RESTART SERVERS
#CUSTOM SERVER NAME

#load servers saved


# Breakdown 
# server_Manager object easily lets you refrence all created servers
# Main.py is the root where each section builds off 
# each game will have its own blueprint meaning that it will have its own webpage 
#each servers bluepint will handle selecting the specific server for that game and running its commands

app = Flask(__name__)
minecraft_Blueprint = Blueprint("minecraft", __name__)

app.register_blueprint(minecraft_Blueprint, url_prefix="/minecraft")

#TODO create a user database along server_database to store users


#before anything create data base

server_man = Minecraft_Server_Manager()

"""
server_man.create_server({
    "name" : "kingston",
    "uuid" : "", #this will generate a uuid 
    "game" : "minecraft",
    "jar_path" : "",
    "jvm_arguments" : "",
    "server_properties" : ""})
"""

server_man.list_active_servers()





#load flask add minecraft blueprint

@app.route("/")
def index():
    #return render_template("index.html")
    return render_template("home.html")

@app.route("/<user>", methods=["POST"])
def user():
    return render_template()

@app.route("/saved_servers.json")
def serve_json():
    return send_file("saved_servers.json")


"""
#Blueprint minecraft

serv_Man = server_Manager("minecraft")

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

"""


""""
def main():
    print("Minecraft Server Manager")
    print("Type 'help' for a list of commands.")


    while True:
        cmd = input(">>> ").strip().lower()

        if cmd == "help":
            print("Commands: create, download-jar, set-jar, start, stop, exit")
        
        elif cmd == "create":
            name = input("Server name: ").strip()
            current_server = Minecraft_server(name)
        
        elif cmd == "set-jar":
            if current_server:
                filename = input("Jar filename (must be in server folder): ").strip()
                print(filename)
                try:
                    current_server.set_jar(filename)
                except FileNotFoundError as e:
                    print(e)
            else:
                print("You need to create a server first.")
        elif cmd == "download-jar":
            if current_server:
                filename = input("Jar URL: ").strip()
                filename1 = input("Jar name: ").strip()
                current_server.download_server_jar(filename, filename1)
                print(f"downloaded jar from {filename} and named {filename1}")

            else:
                print("You need to create a server first.")


        elif cmd == "start":
            if current_server:
                current_server.start()
            else:
                print("You need to create a server first.")
        
        elif cmd == "stop":
            if current_server:
                current_server.stop()
            else:
                print("You need to create a server first.")
        elif cmd == "send-command":
            if current_server:
                current_server.send_command(input("Input command (dont use /):").strip())
            else:
                print("you need to create a server first.")
        elif cmd == "restart":
            if current_server:
                current_server.restart()
            else:
                print("You need to create a server first.")
        
        elif cmd == "exit":
            print("Exiting.")
            break
            
        else:
            print("Unknown command.")

main()

"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
