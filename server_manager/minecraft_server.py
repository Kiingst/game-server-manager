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
        self.process = None
        


    def set_jar(self, jar_name):
        expected_path = self.base_path / jar_name
        if not expected_path.exists():
            raise FileNotFoundError(f"JAR file not found at {expected_path}")

        self.jar_path = expected_path
        self.save_to_DB()
    

    def start(self):
        if not self.jar_path:
            raise RuntimeError("jar_path not set")

            arguments = ["java"] + self.jvm_arguments.split() + ["-jar", str(self.jar_path)]
        self.process = subprocess.Popen(

            arguments,
            cwd = self.base_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    
    def send_command(self, command: str):
        if not self.process or self.process.poll() is not None or not self.process.stdin:
            raise RuntimeError("server not running")
        try:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"failed to send command: {e}") from e

    def check_status(self) -> bool:

        if self.process.poll() is None and self.process is not None:
            return True
        else:
            return False

    def stop(self, wait: bool = True, timeout: float | None = 60):
    if not self.check_status():
        return
    try:
        self.send_command("stop")
        if wait:
            self.process.wait(timeout=timeout)
    except Exception:
        try:
            self.process.terminate()
            if wait:
                self.process.wait(timeout=timeout)
        finally:
            pass

    
    def save_to_DB(self):
        db.save_server(self.UUID, self.name, self.game,str(self.jar_path), self.jvm_arguments,self.server_properties)
    
    def delete_server():
        self.stop(wait=False)
        self.db.delete_server(self.uuid)
