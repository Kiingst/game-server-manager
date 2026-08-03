from flask import Flask, render_template, request, jsonify, send_file, Blueprint

def create_app():
    app = Flask(__name__)
    #minecraft_Blueprint = Blueprint("minecraft", __name__)
    #auth = HTTPBasicAuth()

    app.secret_key = "testing_dev"
   # admin_password = b"testing_remove_this_later" # bcrypt works with bytes
   # hashed_password = bcrypt.hashpw(admin_password, bcrypt.gensalt())
   # print(f"Hashed Password: {hashed_password}")

   #import & register routes from routes.py
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app


