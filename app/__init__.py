from flask import Flask, render_template, request, jsonify, send_file, Blueprint

def create_app():
    app = Flask(__name__, template_folder="../templates")
    #minecraft_Blueprint = Blueprint("minecraft", __name__)
    #auth = HTTPBasicAuth()

    app.secret_key = "testing_dev"
   # admin_password = b"testing_remove_this_later" # bcrypt works with bytes
   # hashed_password = bcrypt.hashpw(admin_password, bcrypt.gensalt())
   # print(f"Hashed Password: {hashed_password}")

    from app.repos.ServerRepository import ServerRepo
    serv_Repo = ServerRepo

    from app.services.ServerService import ServerService
    serv_Service = ServerService(serv_Repo)

    



   #import & register routes from routes.py
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app


