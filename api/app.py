import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
from database.db import db
from resources.users import blp as UsersBlueprint
from resources.messages import blp as MessagesBlueprint
from resources.channels import blp as ChannelsBlueprint

app = Flask(__name__, static_folder='./build', static_url_path='/')
socketio = SocketIO(app, cors_allowed_origins='*')

def create_app(db_url=None):
  load_dotenv()
  
  CORS(app, resources={r"/*": {"origins": "*"}})
  
  
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")
  app.config['TOKEN_SECRET'] = os.getenv("TOKEN_SECRET")
  app.config["API_TITLE"] = "Chat App REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config["PROPAGATE_EXCEPTIONS"] = True

  db.init_app(app)
  api = Api(app)
  
  with app.app_context():
    db.create_all()
  
  api.register_blueprint(UsersBlueprint)
  api.register_blueprint(MessagesBlueprint)
  api.register_blueprint(ChannelsBlueprint)
  
  return app
  
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
  
if __name__ == '__main__':
    socketio.run(app, debug=True)
  

