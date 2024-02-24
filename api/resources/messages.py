import os
import jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from models.messages import MessageModel
from database.schemas import MessageSchema

blp = Blueprint("Messages", "messages", description="Operations on messages.")

@blp.route("/message")
class SendMessage(MethodView):
  
  @blp.arguments(MessageSchema)
  @blp.response(201, MessageSchema)
  def post(self, message_data):
    message = MessageModel(**message_data)
  
    try:
      db.session.add(message)
      db.session.commit()
       
    except SQLAlchemyError:
      abort(500, message="An error occurred sending a message.")

    return message