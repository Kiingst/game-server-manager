import json
import os
from .minecraft_server import Minecraft_Server
from .minecraft_db import ServerDB




class Minecraft_Server_Manager():

    def __init__(self) -> None:

        self.db = ServerDB()
        self.active_servers = [] 
        servers_array = self.db.get_all_servers_from_DB()
        self.initialize_servers(servers_array)


    def initialize_servers(self, array):
        for server_config in array:
            self.active_servers.append(Minecraft_server(server_config))
                        
    
    def add_server(self):   
        pass

    def create_server():
        pass
    
    def delete_server():
        pass
    
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
    
    def list_active_servers():
        pass
    

    


