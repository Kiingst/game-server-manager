import json
import os
from .minecraft_server import Minecraft_Server
from .minecraft_db import ServerDB
import pdb




class Minecraft_Server_Manager():

    def __init__(self) -> None:

        self.db = ServerDB()
        self.active_servers = [] 
        servers_array = self.db.get_all_servers()
        #pdb.breakpoint()
        self.initialize_servers(servers_array)


    def initialize_servers(self, array):
        for server_config in array:
            self.active_servers.append(Minecraft_Server(server_config))
                        
    
    def create_server(self, config1):   
        server = Minecraft_Server(config1)
        self.active_servers.append(server)
    
    def delete_server(self, server_uuid):
        for server in self.active_servers:
            if server_uuid == server.uuid:
                server.delete_server()
                active_servers.remove(server)
    
    def get_server_from_db(uuid):
        conn = sqlite3.connect("server_database.db")
        conn.row_factory = sqlite3.Row  
        cur = conn.cursor()

        cur.execute("SELECT * FROM servers WHERE uuid = ?", (uuid,))
        row = cur.fetchone()

        conn.close()
        if row is None:
            return None
        return dict(row)
    
    def list_active_servers(self):
        x = 1
        for server in self.active_servers:
            print(f"{x}. {server.name} UUID: {server.uuid}")
            x += 1
    

    


