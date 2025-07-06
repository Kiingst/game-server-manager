

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

    #True is running False is Stoped
    def check_status(self) -> bool:

        if self.process.poll() is None and self.process is not None:
            return True
        else:
            return False

    def stop(self):
        self.send_command("stop")

   # def restart(self):
   #     if self.check_status :
   #         self.stop()
   #         while self.check_status:
   #             print("waiting for sever to stop")
   #             pass
   #         self.start()
   #     else:
   #         print("sever is not running")



#TODO
#EDIT CONFIG FILES
#LIVE SERVER CONSOLE 

#DONE
#CREATE AND START SERVER 
#START STOP RESTART SERVERS


