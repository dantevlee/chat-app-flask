import os
import jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from models import UserModel
from database.schemas import UserSchema, UserLoginSchema


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
  
@blp.route("/login")
class UserLogin(MethodView):
  @blp.arguments(UserLoginSchema)
  def post(self, user_login_data):
    
    try:
      user = UserModel.query.filter(
        UserModel.username == user_login_data['username']
      ).first()
      if (user is None):
        return {"message": "User does not exist."}
      
      isMatch = user and pbkdf2_sha256.verify(user_login_data['password'], user.password)
      
      if(isMatch == False):
        abort(401, message="Invalid credentials" )
      
      json_payload = {"id": user.id, "username": user.username, "password": user.password}
      
      if(isMatch):
        token =  jwt.encode(json_payload, os.getenv('TOKEN_SECRET'), algorithm='HS256') 
        return {"username": user.username, "access_token": token }, 200
        
    except SQLAlchemyError:
      abort(500, message="An error occurred while logging into the application. Please try agin later.")
      
      

      
      