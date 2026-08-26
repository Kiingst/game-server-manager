from uuid import uuid4

from app.server_models.ServerInstance import ServerInstance


class ServerService:
    def __init__(self, repository):
        self.repository = repository

        #on init we need to turn all Serverinstance objects in the database into ServerService objects





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
        return self.repository.create(server)

    def list_servers(self):
        return self.repository.list_all()
        #make sure this returns a dict of all the server instances in the database, so that it can be easily converted to json and sent to the front end
