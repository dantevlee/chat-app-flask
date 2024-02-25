import os
import jwt
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from database.db import db
from models.messages import MessageModel
from database.schemas import SendMessageSchema, MessageSchema

blp = Blueprint("Messages", "messages", description="Operations on messages.")

@blp.route("/message")
class SendMessage(MethodView):
  
  @blp.arguments(SendMessageSchema)
  @blp.response(201, SendMessageSchema)
  def post(self, message_data):
    if 'Authorization' not in request.headers:
        abort(401, message="Token is required.")
 
    try:
      token = request.headers['Authorization']
      decoded_token = jwt.decode(token, os.getenv('TOKEN_SECRET'), algorithms=['HS256'])
      if (decoded_token is None):
        abort(401, message="Invalid token.")   
         
      message = MessageModel(**message_data)
      db.session.add(message)
      db.session.commit()
       
    except SQLAlchemyError:
      abort(500, message="An error occurred sending a message.")

    return message
  
  @blp.response(200, MessageSchema(many=True))
  def get(self):
    query = text('''
        SELECT 
            messages.id,
            messages.createdat,
            users.username AS user,
            channels.channel,
            messages.text
        FROM messages
        INNER JOIN channels ON messages.channelid = channels.id
        INNER JOIN users ON messages.userid = users.id
        ORDER BY messages.createdat;
    ''')
    engine = create_engine(os.getenv('DATABASE_URL'))
    Session = sessionmaker(bind=engine)
    session = Session()
    
    result = []
    for row in session.execute(query):
        updated_row = {
            'id': row[0],
            'createdat': row[1],
            'user': row[2],
            'channel': row[3],
            'text': row[4]
        }
        message = MessageSchema().dump(updated_row)
        result.append(message)

    session.close()
    return jsonify(result)
    