import os
import jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.schemas import ChannelSchema
from models import ChannelModel


blp = Blueprint("Channels", "channels", description="Operations on channels.")

@blp.route("/channels")
class ChannelOperations(MethodView):
  @blp.arguments(ChannelSchema)
  @blp.response(201, ChannelSchema)
  @blp.doc(desripton="For development use only.",summary="Create a new channel. For development only." )
  def post(self, channel_data):
    channel = ChannelModel(**channel_data)
    
    try:
      db.session.add(channel)
      db.session.commit()
       
    except SQLAlchemyError:
      abort(500, message="An error occurred creating a channel.")
    
    return channel
  
  @blp.response(200, ChannelSchema(many=True))
  def get(self):
    return ChannelModel.query.all()
  