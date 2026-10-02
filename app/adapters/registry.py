"""Registration and lookup of supported game adapters."""

from collections.abc import Mapping

from app.adapters.base import BaseAdapter
from app.adapters.Minecraft_Adapter import MinecraftJavaAdapter


class UnsupportedGameError(ValueError):
    """No adapter is registered for the requested game ID."""


ADAPTERS: dict[str, BaseAdapter] = {
    MinecraftJavaAdapter.game_id: MinecraftJavaAdapter(),
}


def get_adapter(
    game_id: str, adapters: Mapping[str, BaseAdapter] = ADAPTERS
) -> BaseAdapter:
    """Return the adapter registered for a game ID or raise a clear error."""
    if isinstance(game_id, str) and game_id in adapters:
        return adapters[game_id]
    supported = ", ".join(sorted(adapters)) or "none"
    raise UnsupportedGameError(
        f"Invalid game_id. Please choose from: {supported}"
    )
