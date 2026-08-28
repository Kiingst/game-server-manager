from dataclasses import dataclass

from typing import Optional

@dataclass
class ServerInstance:
    id: Optional[int]
    uuid: str
    name: str
    game_id: str
    status: str
    path: str
    port: int
    container_id: Optional[str] = None
    last_error: Optional[str] = None

    def update_server_id(self, server_id):
        self.id = server_id

    