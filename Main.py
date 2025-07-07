import os
from pathlib import Path
from games.minecraft.Minecraft import Minecraft_server

from flask import Flask, render_template, request, jsonify
#create server
#whate create server is going to do is in the server director we are going to make a folder for a server give it a jar file and eula and run it 

#An ALL in one video game server manager that can take config files and change how it acts depending on the game


#TODO
#CREATE AND START SERVER

#START STOP RESTART SERVERS
#CUSTOM SERVER NAME
#EDIT CONFIG FILES
#LIVE SERVER CONSOLE 



#server = Minecraft_server("test5")
#server.download_server_jar("https://piston-data.mojang.com/v1/objects/05e4b48fbc01f0385adb74bcff9751d34552486c/server.jar", "server")
#server.set_jar("server.jar")
#server.start()
current_server = Minecraft_server("test7")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True)

@app.route("/<user>", methods=["POST"])
def user():
    return render_template()

@app.route("/start", methods=["POST"])
def start():
    current_server.start()
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    current_server.stop()
    return jsonify({"status": "stopped"})

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    if "command" in data:
        current_server.send_command(data["command"])
        return jsonify({"status": f"Command sent: {data['command']}"})
    return jsonify({"error": "No command provided"}), 400

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