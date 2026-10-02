"""Generic Docker operations for containers owned by this application."""

from collections.abc import Mapping
from typing import Any

import docker
from docker.errors import DockerException, NotFound


class ContainerServiceError(Exception):
    """Base error for container service operations."""


class ContainerNotFoundError(ContainerServiceError):
    """No container exists for the requested server."""


class UnmanagedContainerError(ContainerServiceError):
    """A found container does not belong to the requested server."""


class ContainerOperationError(ContainerServiceError):
    """Docker failed while performing a container operation."""


class ContainerService:
    MANAGED_LABEL = "com.game-server-manager.managed"
    SERVER_UUID_LABEL = "com.game-server-manager.server-uuid"

    def __init__(self, client=None):
        """Use an injected Docker client, or connect to the local Docker daemon."""
        if client is not None:
            self.client = client
            return

        try:
            self.client = docker.from_env()
            if not self.client.ping():
                raise ContainerOperationError("Docker daemon did not respond to ping.")
        except DockerException as exc:
            raise ContainerOperationError(
                "Cannot connect to Docker; make sure the Docker daemon is running."
            ) from exc

    @staticmethod
    def _container_name(server) -> str:
        return f"gsm-{server.uuid}"

    def _required_labels(self, server) -> dict[str, str]:
        return {
            self.MANAGED_LABEL: "true",
            self.SERVER_UUID_LABEL: server.uuid,
        }

    def _verify_managed_container(self, container, server) -> None:
        labels = container.labels or {}
        required = self._required_labels(server)
        if any(labels.get(key) != value for key, value in required.items()):
            raise UnmanagedContainerError(
                f"Container {container.id} is not managed for server {server.uuid}."
            )

    def _get_container(self, server):
        """Find a container by saved ID, then by name if that ID is stale."""
        identifiers = []
        if server.container_id:
            identifiers.append(server.container_id)
        name = self._container_name(server)
        if name not in identifiers:
            identifiers.append(name)

        for identifier in identifiers:
            try:
                container = self.client.containers.get(identifier)
            except NotFound:
                continue
            except DockerException as exc:
                raise ContainerOperationError(
                    f"Could not look up container for server {server.uuid}."
                ) from exc

            # A found ID with wrong labels is rejected, even if the name might match.
            self._verify_managed_container(container, server)
            return container

        raise ContainerNotFoundError(f"No container found for server {server.uuid}.")

    def _reload(self, container, server) -> None:
        try:
            container.reload()
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not inspect container for server {server.uuid}."
            ) from exc

    def create(self, server, container_config: Mapping[str, Any]):
        """Create a stopped container, or return its existing managed container."""
        if not isinstance(container_config, Mapping):
            raise ValueError("container_config must be a mapping.")
        image = container_config.get("image")
        if not isinstance(image, str) or not image.strip():
            raise ValueError("container_config requires a nonempty image.")
        if "name" in container_config or "detach" in container_config:
            raise ValueError("Container name and detach are controlled by ContainerService.")

        labels = container_config.get("labels", {})
        if not isinstance(labels, Mapping):
            raise ValueError("container_config labels must be a mapping.")

        try:
            return self._get_container(server)
        except ContainerNotFoundError:
            pass

        options = dict(container_config)
        options["labels"] = {**labels, **self._required_labels(server)}
        options["name"] = self._container_name(server)
        options["detach"] = True

        try:
            return self.client.containers.create(**options)
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not create container for server {server.uuid}."
            ) from exc

    def start(self, server) -> bool:
        """Start a stopped container; return whether its state was changed."""
        container = self._get_container(server)
        self._reload(container, server)
        if container.status == "running":
            return False
        try:
            container.start()
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not start container for server {server.uuid}."
            ) from exc
        return True

    def stop(self, server) -> bool:
        """Stop a running container; return whether its state was changed."""
        container = self._get_container(server)
        self._reload(container, server)
        if container.status != "running":
            return False
        try:
            container.stop()
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not stop container for server {server.uuid}."
            ) from exc
        return True

    def restart(self, server) -> bool:
        """Restart the managed container; return True on success."""
        container = self._get_container(server)
        try:
            container.restart()
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not restart container for server {server.uuid}."
            ) from exc
        return True

    def inspect(self, server) -> dict:
        """Return the managed container's latest Docker attributes."""
        container = self._get_container(server)
        self._reload(container, server)
        return dict(container.attrs)

    def logs(self, server, tail: int = 100) -> str:
        """Return the latest container logs as UTF-8 text."""
        if isinstance(tail, bool) or not isinstance(tail, int) or tail <= 0:
            raise ValueError("tail must be a positive integer.")
        container = self._get_container(server)
        try:
            output = container.logs(tail=tail)
        except DockerException as exc:
            raise ContainerOperationError(
                f"Could not read logs for server {server.uuid}."
            ) from exc
        if isinstance(output, bytes):
            return output.decode("utf-8", errors="replace")
        return output

    def is_running(self, server) -> bool:
        """Return whether Docker currently reports the container as running."""
        container = self._get_container(server)
        self._reload(container, server)
        return container.status == "running"
