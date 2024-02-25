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
from events.active_sessions import active_sessions, active_users
from models import UserModel
from database.schemas import UserSchema, UserLoginSchema, UserNameSchema

blp = Blueprint("Users", "users", description="Operations on users.")

@socketio.on('connect')
def connect():
    if request.sid not in active_sessions:
        active_sessions[request.sid] = None

@socketio.on('login')
def handle_login(username):
    if username not in active_users:
        active_users.append(username)
        active_sessions[request.sid] = username

    socketio.emit('active_users', active_users, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    if request.sid in active_sessions:
        disconnected_user = active_sessions[request.sid]
        del active_sessions[request.sid]

        if disconnected_user in active_users:
            active_users.remove(disconnected_user)

    socketio.emit('active_users', active_users, broadcast=True)

@socketio.on('ping')
def ping(username):
    if username not in active_users:
        active_users.append(username)
        active_sessions[request.sid] = username
        socketio.emit('active_users', active_users, broadcast=True)

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
      
      if(isMatch):
        json_payload = {"id": user.id, "username": user.username, "password": user.password}
        user.lastactiveat = datetime.utcnow()
        db.session.commit()
        
        token =  jwt.encode(json_payload, os.getenv('TOKEN_SECRET'), algorithm='HS256') 
        
        return {"username": user.username, "access_token": token}, 200
        
    except SQLAlchemyError:
      abort(500, message="An error occurred while logging into the application. Please try agin later.")
  
@blp.route("/logout")
class UserLogout(MethodView):
  @blp.arguments(UserNameSchema)
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
  

@blp.route("/users/active")
class ActiveUsers(MethodView):
  @blp.response(200, UserNameSchema(many=True))
  def get(self):
    return active_users

@blp.route("/users/all")
class AllUsers(MethodView):
  @blp.response(200, UserNameSchema(many=True))
  def get(self):
    return UserModel.query.all()    