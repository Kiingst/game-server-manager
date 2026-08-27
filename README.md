# Game Server Manager

Game Server Manager is a solo CS project for managing multiple video game server instances through a simple web interface. The goal is to let a user create, start, stop, restart, inspect, and eventually configure game servers without manually running terminal commands for each one.

The project is being built with Python and Flask. The long-term design is to run each game server inside its own Docker container and have the main web application control those containers through a clean backend service layer.

## About

Many game servers are controlled differently. A Minecraft server, Terraria server, and Project Zomboid server may all need different ports, startup commands, config files, environment variables, and shutdown behavior.

This project is designed around that problem. Instead of putting every game-specific rule directly into the main server manager, the application will use adapters. The generic backend will handle common behavior such as saving server records, starting containers, stopping containers, reading logs, and showing status. Each game adapter will describe how that specific game should run.

The first supported game target is Minecraft Java. After Minecraft works, the project will add a second game to prove that the adapter design works.

## Project Goals

- Build a local web dashboard for managing game servers.
- Save server instances in a SQLite database.
- Run each server instance in its own Docker container.
- Preserve server data across restarts.
- Support server lifecycle actions:
  - create
  - start
  - stop
  - restart
  - delete
  - inspect status
  - view logs
- Keep game-specific logic inside adapters.
- Support Minecraft Java first.
- Add at least one second game after Minecraft works.
- Keep the project understandable and achievable for a solo developer.

## Planned Architecture

The project should be organized around four main layers:

```text
Flask routes and web UI
ServerService
ContainerService
Game adapters
```

The intended request flow looks like this:

```text
User clicks Start
Flask route receives the request
ServerService loads the server from SQLite
ServerService selects the correct game adapter
The adapter builds the Docker container configuration
ContainerService starts or creates the container
ServerRepository saves the updated status
The browser receives the result
```

This keeps the main backend generic while still allowing each game to behave differently.

## Setup Notes

### Requirements

Install these tools before running the finished project:

- Python 3.11 or newer
- pip
- Docker Desktop
- Git

### Local Setup

Clone the repository:

```bash
git clone <repository-url>
cd game-server-manager
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask app:

```bash
python Run.py
```

Then open:

```text
http://localhost:5000
```

## Development Notes

The project should be built in small scrums. See `SCRUM_PLAN.md` for the full project plan.

The main workflow to build toward is:

```text
Create server -> start container -> show status -> view logs -> stop container -> survive app restart
```

That workflow is the heart of the project.

## Safety Notes

This application is intended for local development use first.

A web app that can control Docker containers has powerful access to the host machine. Do not expose this project directly to the public internet without adding strong authentication, input validation, permissions, and deployment hardening.

## Contact

Project owner: Kingston

Contact information can be added here when the project is ready to share publicly.

## License

No license has been selected yet.
