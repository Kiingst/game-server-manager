import json
import os
from games.minecraft.Minecraft import Minecraft_server

#this is here to easliy refrence server objects without re initalizing them

#fix this bull shit
#i fucked up the servers json saving and loading fix this when you feel like toi


#fix add load from file func
#add save to file fun

# when creating a server I will send the server manager a server object
# that server object has a name that is how we locate it 


#when trying to acces a server look for Server_Manager.server.get(name of server)




class server_Managers():
    def __init__(self, game: str) -> None:
        self.active_servers = [] #server objects loaded form sersers_json still have to edit rest of code
        self.game = game
        self.servers_json = {}
        self.filepath = f"static/{self.game}saved_servers.json"
        self.load_servers_json()
        
        
        

    def load_servers_json(self):
    
        try:
            with open(self.filepath, "r") as x:
                print("servers were loaded from file")
                self.servers_json = json.load(x)
                self.load_from_file()
        except FileNotFoundError:
            self.servers_json = {}
        except json.JSONDecodeError as e:
            self.servers_json = {}
            print("Server file was corrupted or not valid JSON. Error:", e)
        self.save_servers_json()


   # def load_from_file(self):
       # self.active_servers = []  # Clear current active list
   #     for server_name, data in self.servers_json.items():
     #       server_object = Minecraft_server(server_name, self)
   #         self.active_servers.update({
   #             server_name : server_object
   #         })

    def save_servers_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, "w") as f:
            json.dump(self.servers_json, f, indent=2)
    
    
    def add_server(self, server : Minecraft_server):
        
        self.active_servers.append(server)
        #self.active_servers.update({
        #        server_name : server_object
        #    })
        
        #self.servers_json[server_object.name] = server_object.to_dict()
        #self.save_servers_json()
    
    def does_server_exist(self, x):
        return any(s.name == x for s in self.active_servers)
    


