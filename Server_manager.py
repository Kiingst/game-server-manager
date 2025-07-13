import json
import os

#this is here to easliy refrence server objects without re initalizing them

#fix this bull shit
#i fucked up the servers json saving and loading fix this when you feel like toi


#fix add load from file func
#add save to file fun

# when creating a server I will send the server manager a server object
# that server object has a name that is how we locate it 


#when trying to acces a server look for Server_Manager.server.get(name of server)






class server_Manager():
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
        except FileNotFoundError:
            self.servers_json = {}
        except json.JSONDecodeError as e:
            self.servers_json = {}
            print("Server file was corrupted or not valid JSON. Error:", e)
        
        self.save_servers_json()

    def save_servers_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, "w") as f:
            json.dump(self.servers_json, f, indent=2)
    

    def get_server(self, name):
        return self.servers.get(name)

    def add_server(self, server_object):
        self.servers[server_object.name] = server_object
        self.server_json[server_object.name] = server_object.to_dict()
        print(self)
        self.save_servers()
    
    def does_server_exist(self, x):
        return self.servers.get("name") == x
    
    def get_all_server_names(self):
        return list(self.servers.keys())


