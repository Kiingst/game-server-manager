from uuid import uuid4

from app.server_models.ServerInstance import ServerInstance


class ServerService:
    def __init__(self, repository):
        self.repository = repository

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

