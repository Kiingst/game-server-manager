import json

#this is here to easliy refrence server objects without re initalizing them

#fix this bull shit
#i fucked up the servers json saving and loading fix this when you feel like toi


class server_Manager():
    def __init__(self, game: str) -> None:
        self.active_server = None
        self.game = game
        self.load_servers()
        self.filepath = f"static/{self.game}saved_servers.json"
        

    def load_servers(self):
    
        try:
            with open(self.filepath, "r") as x:
                print("servers were loaded from file")
                self.servers = json.load(x)
        except FileNotFoundError:
            self.servers = {}
        except json.JSONDecodeError as e:
            self.servers = {}
            print("Server file was corrupted or not valid JSON. Error:", e)

    def get_server(self, name):
        return self.servers.get(name)

    def add_server(self, name, server_object):
        self.servers[name] = server_object
        self.save_servers()

    def save_servers(self):
            with open(self.filepath, "w") as f:
                json.dump(self.servers, f)
    
    def does_server_exist(self, x):
        return self.servers.get("name") == x
    
    def get_all_server_names(self):
        return list(self.servers.keys())


