from dataclasses import asdict
from unittest import result

from flask import Blueprint, render_template, jsonify, request, current_app

from jsonschema import validate, ValidationError # use this to validate json

main_blueprint = Blueprint("main", __name__)


@main_blueprint.get("/")
def home():
    return render_template("home.html")


@main_blueprint.get("/api/servers")
def get_servers():
    server_service = current_app.serv_Service
    servers = server_service.list_servers_as_dict()
    return jsonify(servers), 200


@main_blueprint.post("/api/servers")
def create_server():
    # Get the server details from the request
    data = request.get_json()
    name = data.get("name")
    game_id = data.get("game_id")
    path = data.get("path") # TODO change this have path set by the ServerService to the default path for the game_id
    port = data.get("port")

    #use datacalss
    
    server_service = current_app.serv_Service
    #refrence current_app where server_service is made and tell it to create a server
    # Return the created server as JSON

    new_server_dict = server_service.create_server(name, game_id, path, port)

    return jsonify(new_server_dict), 400 if "error" in new_server_dict else 201


@main_blueprint.get("/api/servers/<uuid>")
def get_specific_server(uuid):
    server_service = current_app.serv_Service
    server = server_service.list_server_as_dict(uuid)
    if server:
        return jsonify(server), 200
    else:
        return jsonify({"error": "Server not found"}), 404
    

@main_blueprint.delete("/api/servers/<uuid>")
def delete_specific_server(uuid):
    server_service = current_app.serv_Service
    result = server_service.delete_server(uuid)

    return jsonify(result), 200 if "message" in result else 500

@main_blueprint.patch("/api/servers/<uuid>")
def update_specific_server(uuid):
    server_service = current_app.serv_Service
    data = request.get_json()
    result = server_service.update_server(uuid, data)

    return jsonify(result), 200 if "message" in result else 400