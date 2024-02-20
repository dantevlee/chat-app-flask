from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from models import UserModel
from database.schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users.")

@blp.route("/register")
class UserRegistartion(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
    if UserModel.query.filter(UserModel.username == user_data['username']).first():
      abort(409, message="A user with that username already exists.")
      
    user = UserModel(
      firstname = user_data['firstname'],
      lastname = user_data['lastname'],
      username = user_data['username'],
      password = pbkdf2_sha256.hash(user_data['password'])
    )
    
    try:
     db.session.add(user)
     db.session.commit()
    except SQLAlchemyError:
      abort(500, message="An error occurred registering a new user.")
    
    return {"message": "User created successfully."}, 201
    