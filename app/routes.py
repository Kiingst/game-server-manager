from flask import Blueprint, render_template, jsonify, request, current_app


main_blueprint = Blueprint("main", __name__)


@main_blueprint.get("/")
def home():
    return render_template("home.html")


@main_blueprint.get("/api/servers")
def get_servers():
    pass

@main_blueprint.post("/api/servers")
def create_server():
    # Get the server details from the request
    data = request.get_json()
    name = data.get("name")
    game_id = data.get("game_id")
    path = data.get("path")
    port = data.get("port")

    #refrence current_app where server_service is made and tell it to create a server
    server_service = current_app.serv_Service
    new_server = server_service.create_server(name, game_id, path, port)

    # Return the created server as JSON
    return jsonify(new_server.__dict__), 201

@main_blueprint.get("/api/servers/<id>")
def get_servers():
    pass

@main_blueprint.delete("/api/servers/<id>")
def delete_server():
    pass