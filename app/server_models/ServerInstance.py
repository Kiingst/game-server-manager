from dataclasses import dataclass

@dataclass
class ServerInstance:
    id: str
    name: str
    game_id: str
    status: str
    data_path: str
    port: int
    container_id: str 