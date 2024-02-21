import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from dotenv import load_dotenv

from database.db import db
from resources.users import blp as UsersBlueprint


def create_app(db_url=None):
  app = Flask(__name__)
  load_dotenv()
  CORS(app, resources={r'/*': {'origins': '*'}})
  
  socketio = SocketIO(app, cors_allowed_origins='*')
  
  app.config["API_TITLE"] = "Chat App REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
  db.init_app(app)
  api = Api(app)
  if __name__ == '__main__':
    app.run()
  
  with app.app_context():
    db.create_all()
  
  api.register_blueprint(UsersBlueprint)
  
  
  return app