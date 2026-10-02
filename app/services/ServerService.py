from collections.abc import Mapping
from dataclasses import asdict
from uuid import uuid4

from app.adapters.base import BaseAdapter
from app.adapters.registry import UnsupportedGameError, get_adapter
from app.server_models.ServerInstance import ServerInstance


class ServerService:
    def __init__(self, repository, adapter_registry: Mapping[str, BaseAdapter]):
        self.repository = repository
        self.adapter_registry = adapter_registry
        self.servers : list[ServerInstance] = []
        # Load servers from the repository on initialization
        self.load_servers()

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


        try:
            get_adapter(game_id, self.adapter_registry)
        except UnsupportedGameError as exc:
            return {"error": str(exc)}

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

    def get_adapter_for_server(self, server: ServerInstance) -> BaseAdapter:
        """Select the registered game adapter for a saved server."""
        return get_adapter(server.game_id, self.adapter_registry)

    def get_update_schema(self) -> dict:
            return {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "game_id": {"type": "string"},
                    "port": {"type": "integer"}
                },
                "additionalProperties": False
            }

    def update_server(self, uuid, data: dict) -> dict:
        editable_fields = {"name", "game_id", "port"}

        server = self.get_server_instance_by_uuid(uuid)
        if not server:
            return {"error": "Server not found"}

        invalid_fields = set(data) - editable_fields
        if invalid_fields:
            return {"error": f"Field '{sorted(invalid_fields)[0]}' is not editable."}

        if "name" in data:
            for existing_server in self.servers:
                if existing_server.uuid != uuid and existing_server.name == data["name"]:
                    return {"error": f"Server with name '{data['name']}' already exists."}

        if "game_id" in data:
            try:
                get_adapter(data["game_id"], self.adapter_registry)
            except UnsupportedGameError as exc:
                return {"error": str(exc)}
            if server.container_id and data["game_id"] != server.game_id:
                return {"error": "Cannot change game_id after a container is created."}

        #TODO validate all data types      

        for key, value in data.items():
            setattr(server, key, value)

        self.repository.update(server)
        return asdict(server)

        

    def delete_server(self, uuid) -> dict:
        server = self.get_server_instance_by_uuid(uuid)
        if server:
            self.servers.remove(server)
            self.repository.delete(uuid)
            return {"message": "Server deleted successfully"}
        else:
            return {"error": "Server not found"}

    

        
        
