from dataclasses import asdict
from uuid import uuid4

from app.server_models.ServerInstance import ServerInstance


class ServerService:
    def __init__(self, repository):
        self.repository = repository
        self.servers : list[ServerInstance] = []
        # Load servers from the repository on initialization
        self.load_servers()
        self.game_list = ["Minecraft", "CSGO", "Rust", "ARK", "Valheim"] #temp valid game list, should come from server adapters

        print("Servers loaded:", self.servers)



    def load_servers(self):
        # use the uuid to get all servers Then use get to load each object
        server_uuids = self.repository.list_all_server_uuids()
        for uuid in server_uuids:
            #get server
            server_data = self.repository.get(uuid)
            if server_data:
                #create instance
                server_instance = ServerInstance(server_data[0], server_data[1], server_data[2], server_data[3], server_data[4], server_data[5], server_data[6], server_data[7], server_data[8])
                self.servers.append(server_instance)


    def create_server(self, name, game_id, path, port):

        server = ServerInstance(
            id=None,
            uuid=str(uuid4()),
            name=name,
            game_id=game_id,
            status="stopped",
            path=path,
            port=port,
        )
        #compare all servers in self.servers to see if any have the same name or port
        for existing_server in self.servers:
            if existing_server.name == name:
                return { "error": f"Server with name '{name}' already exists." }


        #check game list
        if game_id not in self.game_list:
            return {"error": f"Invalid game_id. Please choose from: {', '.join(self.game_list)}"}

        self.servers.append(server) #append to severs list
        self.repository.create(server) #create in the repository
        return server.__dict__ #return to routes

    def list_servers_as_dict(self) -> list[dict]:
        # Refresh the list of servers from the repository
        print("self.servers:", self.servers)
        return [asdict(server) for server in self.servers]

    def list_server_as_dict(self, uuid) -> dict | None:
        server = self.get_server_instance_by_uuid(uuid)
        if server:
            return asdict(server)
        else:
            return None

    def get_server_instance_by_uuid(self,uuid) -> ServerInstance | None:
        for server in self.servers:
            if server.uuid == uuid:
                return server
        return None

    def update_server(self, uuid, data: dict) -> dict:
        editable_fields = {"name", "game_id", "port"}

        server = self.get_server_instance_by_uuid(uuid)
        if not server:
            return {"error": "Server not found"}

        #validate name and game_id
        for existing_server in self.servers:
            if existing_server.name == data.get("name"):
                return { "error": f"Server with name '{data.get('name')}' already exists." }
        if data.get("game_id") not in self.game_list:
            return {"error": f"Invalid game_id. Please choose from: {', '.join(self.game_list)}"}

        #TODO validate all data types      

        for key, value in data.items():
            if key in editable_fields:
                setattr(server, key, value)
            else:
                return {"error": f"Field '{key}' is not editable."}

        

        """ Find the existing ServerInstance by UUID.
        Reject unknown or protected fields.
        Validate each supplied value.
        Change only the supplied fields on the existing instance.
        Call repository.update(server).
        Return asdict(server)."""


        pass

    def delete_server(self, uuid) -> dict:
        server = self.get_server_instance_by_uuid(uuid)
        if server:
            self.servers.remove(server)
            self.repository.delete(uuid)
            return {"message": "Server deleted successfully"}
        else:
            return {"error": "Server not found"}

        
        
