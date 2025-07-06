

import os
from pathlib import Path
import urllib.request
from games.Server import Server
import subprocess

class Minecraft_server(Server):
    
    def __init__(self, name) -> None:
        self.jar = None
        self.name = name
        super().__init__(name, "minecraft")
        super().create_server_dir()


    def set_jar(self, jar_name):
        expected_path = self.base_path / jar_name
        if not expected_path.exists():
            raise FileNotFoundError(f"JAR file not found at {expected_path}")

        self.jar_path = expected_path
        print(f"JAR path set to: {self.jar_path}")
    

    def download_server_jar(self, mine_url: str, name_of_jar: str):
        name_of_jar = name_of_jar + ".jar"
        os.makedirs(self.base_path, exist_ok= True)
        urllib.request.urlretrieve(mine_url, self.base_path / name_of_jar )

    def start(self):
        self.process = subprocess.Popen(

            ['java', "-Xmx1g", '-Xms1g', '-jar', 'server.jar'],
            cwd = self.base_path
        )
    
    def send_command(self, command):
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            print(f"Sent command: {command}")
        else:
            print("Server is not running or stdin not available.")


    def stop(self):
        self.send_command("stop")
#TODO
#CREATE AND START SERVER DONE

#START STOP RESTART SERVERS
#CUSTOM SERVER NAME
#EDIT CONFIG FILES
#LIVE SERVER CONSOLE 




