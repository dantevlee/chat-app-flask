import os
import jwt
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from database.db import db
from events.sockets import socketio
from models import UserModel
from database.schemas import UserSchema, UserLoginSchema, UserLogoutSchema

blp = Blueprint("Users", "users", description="Operations on users.")
active_users = []
active_sessions = {}

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
      
      if(not isMatch):
        abort(401, message="Invalid credentials" )
      
      json_payload = {"id": user.id, "username": user.username, "password": user.password}
      
      if(isMatch):
  
        user.lastactiveat = datetime.utcnow()
        db.session.commit()
        
        token =  jwt.encode(json_payload, os.getenv('TOKEN_SECRET'), algorithm='HS256') 

        return {"username": user.username, "access_token": token }, 200
        
    except SQLAlchemyError:
      abort(500, message="An error occurred while logging into the application. Please try agin later.")
  
  @socketio.on('connect')
  def connect():
    print('connected!')
    if request.sid not in active_sessions:
        active_sessions[request.sid] = None
  
  @socketio.on('login')
  def handlelogin(online_users):
    
    twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)
    online_users = UserModel.query.filter(UserModel.lastactiveat > twelve_hours_ago).all()
      
    if online_users not in active_users:
      active_users.append(online_users)
      active_sessions[request.sid] = online_users
      
    socketio.emit('login', active_users, broadcast=True)
    
@blp.route("/logout")
class UserLogout(MethodView):
  
  @blp.arguments(UserLogoutSchema)
  def post(self, user_data):
    
    try:
     user = UserModel.query.filter(
       UserModel.username == user_data['username']
     ).first() 
    
     user.lastactiveat = None
     db.session.commit()
     
     return {"message": "User successfully logged out."}, 200
    
    except SQLAlchemyError:
      abort(500, message="An error occurred while trying to log out. Please try again later.")
    
       

      
      