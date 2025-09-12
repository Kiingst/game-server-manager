import os
import sqlite3
import json
from pathlib import Path
import urllib.request
from games.Server import Server
import subprocess
from Server_manager import server_Managers

from .minecraft_db import ServerDB

#Config is a dict with all the data from the server We are going to use the database to generate this file and use that to init servers
"""
UUID
name
game
jar_path
JVM ARGUments
server_properties
"""
#make sure when you change one of these to push it to the DB



class Minecraft_server(Server):


    def __init__(self, config : dict):

        self.db = ServerDB()

        #init parent SERVER to CREATE DIR AND SET UUID IF NONEXISTANT
        super().__init__(config["name"], config["uuid"] )
        self.name = config["name"]
        self.uuid = config["uuid"]
        self.game = config["game"]
        self.jar_path = config["jar_path"]
        self.jvm_arguments = config["jvm_arguments"]
        self.server_properties = config["server_properties"]

        


    def set_jar(self, jar_name):
        expected_path = self.base_path / jar_name
        if not expected_path.exists():
            raise FileNotFoundError(f"JAR file not found at {expected_path}")

        self.jar_path = expected_path
        print(f"JAR path set to: {self.jar_path}")

        self.save_to_DB()
    

    def start(self):
        self.process = subprocess.Popen(

            ['java', "-Xmx2g", '-Xms1g', '-jar', 'server.jar'],
            cwd = self.base_path,
            stdin=subprocess.PIPE,
            text=True
        )
    
    def send_command(self, command):
        print(f"{self.process}")
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            print(f"Sent command: {command}")
        else:
            print("Server is not running or stdin not available.")

    def check_status(self) -> bool:

        if self.process.poll() is None and self.process is not None:
            return True
        else:
            return False

    def stop(self):
        self.send_command("stop")

    
    def save_to_DB(self):
        db.save_server(self.UUID, self.name, self.game,self.jar_path, self.jvm_arguments,self.server_properties)
        
