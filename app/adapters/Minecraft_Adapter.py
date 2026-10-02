"""Minecraft Java container configuration."""

from pathlib import Path
from typing import Any

from app.adapters.base import BaseAdapter
from app.server_models.ServerInstance import ServerInstance


class MinecraftJavaAdapter(BaseAdapter):
    game_id = "Minecraft"

    def build_container_config(self, server: ServerInstance) -> dict[str, Any]:
        """Return Docker options for one persistent Minecraft Java server."""
        if not isinstance(server.path, str) or not server.path.strip():
            raise ValueError("Minecraft server path must be a nonempty string.")
        if isinstance(server.port, bool) or not isinstance(server.port, int):
            raise ValueError("Minecraft server port must be an integer from 1 to 65535.")
        if not 1 <= server.port <= 65535:
            raise ValueError("Minecraft server port must be an integer from 1 to 65535.")

        data_path = str(Path(server.path).expanduser().resolve())
        return {
            "image": "itzg/minecraft-server",
            "environment": {"EULA": "TRUE"},
            "ports": {"25565/tcp": server.port},
            "volumes": {data_path: {"bind": "/data", "mode": "rw"}},
        }
