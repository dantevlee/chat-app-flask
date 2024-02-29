import os
import jwt
from flask import jsonify, Flask
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_socketio import emit, SocketIO
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.db import db
from models import UserModel
from database.schemas import UserSchema, UserLoginSchema, UserNameSchema

blp = Blueprint("Users", "users", description="Operations on users.")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


            
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
  
  @socketio.on('login')
  def handle_login(self):
    print('login connected')
     
  
  @blp.arguments(UserLoginSchema)
  def post(self, user_login_data):
    try:
      input_username = user_login_data['username'].casefold()
      user = UserModel.query.filter(
        UserModel.username == input_username
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
        
        self.handle_login()
        return {"username": user.username, "access_token": token}, 200
        
    except SQLAlchemyError:
      abort(500, message="An error occurred while logging into the application. Please try agin later.")
    
  
@blp.route("/logout")
class UserLogout(MethodView):
  
  @socketio.on('logout')
  def handle_logout(self, user):
    print('logout connected')
    socketio.emit('logout', user)  
  
  @blp.arguments(UserNameSchema)
  def post(self, user_data):
    try:
     user = UserModel.query.filter(
       UserModel.username == user_data['username']
     ).first()
    
     if user:
        user.lastactiveat = None
        db.session.commit()
     
        query = text('''
       SELECT id, username, lastactiveat FROM users WHERE lastactiveat > now() - interval '12 hours';
        ''')
        engine = create_engine(os.getenv('DATABASE_URL'))
        Session = sessionmaker(bind=engine)
        session = Session()
     
        result = []
        for row in session.execute(query):
          updated_row = {
            'id': row[0],
            'username': row[1],
            'lastactiveat': row[2]
        }
        
          result.append(updated_row)
        
        self.handle_logout(user.username)
        return {"message": "User successfully logged out."}, 200
    
    except SQLAlchemyError as e:
      print(f"Error: {e}")
      abort(500, message="An error occurred while trying to log out. Please try again later.")
      
    
  

@blp.route("/users/active")
class ActiveUsers(MethodView):
  @blp.response(200, UserNameSchema(many=True))
  def get(self):
    query = text('''
       SELECT id, username, lastactiveat FROM users WHERE lastactiveat > now() - interval '12 hours';
    ''')
    engine = create_engine(os.getenv('DATABASE_URL'))
    Session = sessionmaker(bind=engine)
    session = Session()
    
    result = []
    for row in session.execute(query):
        updated_row = {
            'id': row[0],
            'username': row[1],
            'lastactiveat': row[2]
        }
    
        result.append(updated_row)

    session.close()
    return jsonify(result)
    
    
@blp.route("/users/all")
class AllUsers(MethodView):
  @blp.response(200, UserNameSchema(many=True))
  def get(self):
    return UserModel.query.all()    