import os
import json
from games.minecraft.minecraft_ui import minecraft_Blueprint
from flask import Flask, render_template, request, jsonify, send_file
from Server_manager import server_Manager


#An ALL in one video game server manager that can take config files and change how it acts depending on the game

#TODO
#EDIT CONFIG FILES
#LIVE SERVER CONSOLE
#Website UI for Servers



 

#DONE
#CREATE AND START SERVER
#START STOP RESTART SERVERS
#CUSTOM SERVER NAME

#load servers saved
server_Man = server_Manager()
print(server_Man.servers)


#load flask add minecraft blueprint
app = Flask(__name__)
app.register_blueprint(minecraft_Blueprint, url_prefix="/minecraft")

@app.route("/")
def index():
    #return render_template("index.html")
    return render_template("home.html")

@app.route("/<user>", methods=["POST"])
def user():
    return render_template()

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    if "command" in data:
        current_server.send_command(data["command"])
        return jsonify({"status": f"Command sent: {data['command']}"})
    return jsonify({"error": "No command provided"}), 400

@app.route("/saved_servers.json")
def serve_json():
    return send_file("saved_servers.json")






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
    app.run(debug=True)