import json


class server_Manager():
    def __init__(self) -> None:
        self.load_servers()

    def load_servers(self):
    
        try:
            with open("static/saved_servers.json", "r") as x:
                print(x)
                self.servers = json.load(x)
        except FileNotFoundError:
            self.servers = {}

    def get_server(self, name):
        return self.servers.get(name)

    def add_server(self, name, server_object):
        self.servers[name] = server_object


