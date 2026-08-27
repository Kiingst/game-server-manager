from flask import Blueprint, render_template, jsonify, request, current_app

main_blueprint = Blueprint("main", __name__)
server_service = current_app.serv_Service

@main_blueprint.get("/")
def home():
    return render_template("home.html")


@main_blueprint.get("/api/servers")
def get_servers():
    servers = server_service.list_servers()
    return jsonify([server.__dict__ for server in servers]), 200


@main_blueprint.post("/api/servers")
def create_server():
    # Get the server details from the request
    data = request.get_json()
    name = data.get("name")
    game_id = data.get("game_id")
    path = data.get("path") # TODO change this have path set by the ServerService to the default path for the game_id
    port = data.get("port")

    #use datacalss
    

    #refrence current_app where server_service is made and tell it to create a server
    new_server = server_service.create_server(name, game_id, path, port)

    # Return the created server as JSON
    return jsonify(new_server.__dict__), 201

@main_blueprint.get("/api/servers/<id>")
def get_specific_server(id):
    pass

@main_blueprint.delete("/api/servers/<id>")
def delete_specific_server(id):
    pass