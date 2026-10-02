"""Interface for game-specific container configuration."""

from abc import ABC, abstractmethod
from typing import Any

from app.server_models.ServerInstance import ServerInstance


class BaseAdapter(ABC):
    game_id: str

    @abstractmethod
    def build_container_config(self, server: ServerInstance) -> dict[str, Any]:
        """Describe how Docker should create this game's server container."""

    def get_default_settings(self) -> dict[str, Any]:
        """Return game defaults when settings are added in a later scrum."""
        raise NotImplementedError

    def validate_settings(self, settings: dict[str, Any]) -> None:
        """Validate game settings when settings are added in a later scrum."""
        raise NotImplementedError

    def send_command(self, server: ServerInstance, command: str) -> None:
        """Send a game command when command support is added."""
        raise NotImplementedError

    def get_players(self, server: ServerInstance) -> list[str]:
        """List players when player inspection is added."""
        raise NotImplementedError
