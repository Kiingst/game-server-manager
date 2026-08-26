# Game Server Manager Scrum Plan

## Project Vision

Build a web-based game server manager that can create, start, stop, restart, inspect, and manage multiple containerized video game server instances from a simple web interface.

The finished project should support Minecraft Java first, then prove the design by adding at least one more game through an adapter system.

## Finished Project Definition

The project is considered finished when:

- The Flask application starts from one clear command.
- The web dashboard lists all saved server instances.
- A user can create a new server from the browser.
- Each server runs in its own Docker container.
- Server data persists after stopping, restarting, or recreating containers.
- The app can start, stop, restart, delete, and inspect servers.
- Recent logs are visible from the web interface.
- Server status remains correct after restarting the Flask app.
- Minecraft Java is fully supported.
- At least one second game is supported through the same adapter system.
- Game-specific logic lives in adapters, not in the generic server service.
- The code is organized, documented, and safe enough for local development use.

## Core Architecture

The application should be divided into four main layers:

1. Flask routes and web interface
2. Server service
3. Container service
4. Game adapters

The generic backend should manage records, containers, status, logs, and lifecycle actions. Game-specific behavior should be handled through adapters.

Example flow:

```text
User clicks Start
Flask route receives request
ServerService loads the server from SQLite
ServerService selects the correct adapter
Adapter builds the Docker container config
ContainerService starts or creates the container
ServerRepository saves the updated status
Flask returns the result to the browser
```

## Scrum Routine

Because this is a solo project, each scrum should be small and demo-focused.

At the start of each scrum:

- Pick a small goal.
- Choose only the tasks needed for that goal.
- Define what "done" means.

During each work session:

- What did I finish?
- What is blocking me?
- What is the next smallest useful step?

At the end of each scrum:

- Run the app.
- Demo the feature to yourself.
- Write down what works.
- Write down what broke.
- Move unfinished work into a later scrum.

## Scrum 0: Project Cleanup DONE

### Goal

Make the project easier to understand before adding more features.

### Tasks

- Decide that `Run.py` and the `app/` folder are the main application. DONE
- Treat `Main.py` as old prototype code. DONE
- Update `README.md` with the project goal and setup notes. DONE
- Make file and class names consistent. DONE
- Add real dependencies to `requirements.txt`. DONE
- Make sure local databases, server folders, virtual environments, and caches are ignored by Git. DONE
- Create a clear project folder structure. DONE

### Done When

- The Flask app starts from one command.
- The active code path is clear.
- Old prototype code is no longer confusing the project direction.

## Scrum 1: Server Database Foundation

### Goal

Create, save, load, list, update, and delete server records.

### Tasks

- Fix server creation so `uuid` is saved to SQLite.
- Implement `list_all()`.
- Convert database rows into `ServerInstance` objects.
- Add a `settings_json` field for game-specific options.
- Add validation for server name, game ID, path, and port.
- Make sure duplicate names are handled cleanly.
- Add basic manual tests or unit tests for the repository.

### Done When

- A server record can be created.
- The app can restart.
- The same server record can still be loaded from SQLite.
- Server records can be listed, updated, and deleted.

## Scrum 2: Basic API

### Goal

Control saved server records through HTTP endpoints.

### Tasks

- Add `GET /api/servers`.
- Add `POST /api/servers`.
- Add `GET /api/servers/<id>`.
- Add `DELETE /api/servers/<id>`.
- Return JSON responses.
- Use correct status codes.
- Return `404` for missing servers.
- Return `400` for invalid create requests.

### Done When

- Servers can be created through an HTTP request.
- Servers can be listed through an HTTP request.
- A single server can be viewed by ID.
- A server can be deleted by ID.

## Scrum 3: Adapter System

### Goal

Separate generic server management from game-specific logic.

### Tasks

- Create `app/adapters/base.py`.
- Define a base adapter interface.
- Create `MinecraftJavaAdapter`.
- Create an adapter registry keyed by `game_id`.
- Move Minecraft-specific container configuration into the Minecraft adapter.
- Make `ServerService` retrieve adapters from the registry.

### Adapter Interface

The base adapter should eventually support:

```python
class BaseAdapter:
    game_id: str

    def build_container_config(self, server):
        raise NotImplementedError

    def get_default_settings(self):
        raise NotImplementedError

    def validate_settings(self, settings):
        raise NotImplementedError

    def send_command(self, server, command):
        raise NotImplementedError

    def get_players(self, server):
        raise NotImplementedError
```

### Done When

- `ServerService` can select an adapter by `game_id`.
- Minecraft-specific logic is not hardcoded in the generic service.
- Adding another game looks possible without rewriting the backend.

## Scrum 4: Docker Container Service

### Goal

Create and manage Docker containers from generic backend code.

### Tasks

- Add `ContainerService`.
- Use the Docker Python SDK.
- Implement `create(server, container_config)`.
- Implement `start(server)`.
- Implement `stop(server)`.
- Implement `restart(server)`.
- Implement `inspect(server)`.
- Implement `logs(server, tail=100)`.
- Implement `is_running(server)`.
- Add labels to every managed container.
- Use deterministic container names such as `gsm-<server.uuid>`.
- Only manage containers that have the app's managed label.

### Done When

- A hardcoded test server can create a Docker container.
- The container can be started.
- The container can be stopped.
- The container can be inspected.
- Logs can be read.

## Scrum 5: First Real Minecraft Server

### Goal

Run one real Minecraft Java server inside Docker.

### Tasks

- Use the `itzg/minecraft-server` Docker image.
- Mount server data into `servers/<uuid>/`.
- Set `EULA=TRUE`.
- Expose the Minecraft port.
- Store the container ID in SQLite.
- Update server status after start and stop.
- Preserve world data between restarts.

### Done When

- A Minecraft server record can be created.
- The Minecraft container can be started.
- The server appears as running in Docker.
- The Minecraft container can be stopped.
- The same server can be restarted without losing data.

## Scrum 6: Lifecycle API

### Goal

Control real containers through HTTP endpoints.

### Tasks

- Add `POST /api/servers/<id>/start`.
- Add `POST /api/servers/<id>/stop`.
- Add `POST /api/servers/<id>/restart`.
- Add `GET /api/servers/<id>/status`.
- Add `GET /api/servers/<id>/logs`.
- Prevent starting a server that is already running.
- Prevent stopping a server that is already stopped.
- Return useful errors when Docker fails.
- Set server status to `error` when lifecycle actions fail.

### Done When

- A Minecraft server can be started through the API.
- A Minecraft server can be stopped through the API.
- A Minecraft server can be restarted through the API.
- Logs and status can be fetched through the API.

## Scrum 7: Simple Web Dashboard

### Goal

Create the first usable browser interface.

### Tasks

- Build a homepage that lists all servers.
- Add a create-server form.
- Add a server detail page.
- Add start, stop, restart, and delete buttons.
- Show current server status.
- Show recent logs.
- Add simple JavaScript for button actions.
- Refresh status after actions.

### Done When

- The project can be used from the browser.
- A user can create a server without manually calling the API.
- A user can start, stop, restart, and delete a server from the dashboard.

## Scrum 8: Persistence and Recovery

### Goal

Make the app recover correctly after Flask restarts.

### Tasks

- On app startup, load all servers from SQLite.
- Inspect Docker containers by app labels.
- Match containers to servers by UUID.
- Update server status based on actual Docker state.
- Handle missing containers.
- Handle containers that are running even if the database says stopped.
- Show clear errors for broken or missing containers.

### Done When

- Start a Minecraft server.
- Restart the Flask app.
- The dashboard still lists the server.
- The dashboard shows the correct running or stopped state.
- The app can still control the existing container.

## Scrum 9: Commands and Logs

### Goal

Interact with a running server from the web interface.

### Tasks

- Add `POST /api/servers/<id>/commands`.
- Add command support to the base adapter interface.
- Implement Minecraft command support.
- Prefer RCON for Minecraft commands.
- Add a command input to the server detail page.
- Improve the log viewer.
- Poll logs automatically from the browser.

### Done When

- A command can be sent to a running Minecraft server from the browser.
- Recent logs can be viewed from the browser.
- The user can confirm that commands affect the running server.

## Scrum 10: Second Game Adapter

### Goal

Prove that the adapter architecture works for more than Minecraft.

### Good Candidate Games

- Terraria
- Valheim
- Project Zomboid
- Palworld

### Tasks

- Pick one second game.
- Find a reliable Docker image for that game.
- Create a new adapter.
- Define default settings.
- Define default ports.
- Define required environment variables.
- Reuse the same `ServerService`.
- Reuse the same `ContainerService`.
- Add the game as an option in the create-server form.

### Done When

- The app can create a Minecraft server.
- The app can create one other game server.
- Both server types use the same generic lifecycle API.
- No game-specific conditions were added to `ServerService`.

## Scrum 11: Safety and Polish

### Goal

Make the project safer, cleaner, and easier to present.

### Tasks

- Validate all ports.
- Validate all paths.
- Keep server paths inside the project server-data directory.
- Prevent unsafe container names.
- Improve error messages.
- Add loading states to the UI.
- Add empty states to the dashboard.
- Add basic authentication or local-only warnings.
- Document that the app should not be exposed directly to the internet.
- Add screenshots or usage examples to the README.

### Done When

- The UI feels understandable.
- Invalid input is rejected.
- Common errors produce clear messages.
- The README explains how to run and use the project.

## Scrum 12: Final Project Review

### Goal

Prepare the project as a finished solo CS project.

### Tasks

- Review the folder structure.
- Remove unused prototype code.
- Remove committed local data if any exists.
- Confirm `.gitignore` is correct.
- Run all tests.
- Manually test the main workflow.
- Update README with:
  - project summary
  - features
  - architecture
  - setup steps
  - usage steps
  - known limitations
  - future improvements
- Create a short demo checklist.

### Final Demo Checklist

- Start the Flask app.
- Open the dashboard.
- Create a Minecraft server.
- Start the Minecraft server.
- View its status.
- View its logs.
- Stop the Minecraft server.
- Restart the Flask app.
- Confirm the server still exists.
- Start it again.
- Create a second game server.
- Start and stop the second game server.

### Done When

- The app works from the web dashboard.
- The backend architecture is clean.
- The project demonstrates persistence, Docker, adapters, and a usable UI.
- The README explains the project clearly enough for someone else to run it.

## Backlog Ideas

These are useful ideas, but they should wait until the main project works.

- User accounts
- Server backups
- Scheduled restarts
- Automatic updates
- Mod/plugin management
- Live console using WebSockets
- Player list display
- CPU and memory usage graphs
- File browser for server files
- Config file editor
- Role-based permissions
- Public share page for server status
- Discord bot integration

## Priority Rule

When unsure what to work on next, choose the smallest task that moves the project closer to this workflow:

```text
Create server -> start container -> show status -> view logs -> stop container -> survive app restart
```

That workflow is the heart of the project.
