from database.db import db 
from sqlalchemy.sql import func 

class MessageModel(db.Model):
  __tablename__= "messages"
  
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(512), nullable=False)
  createdat = db.Column(db.Date, server_default=func.now(), nullable=False)
  userid = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
  channelid = db.Column(db.Integer(), db.ForeignKey("channels.id"), nullable=False)
  user = db.relationship("UserModel", back_populates="messages")
  channel = db.relationship("ChannelModel", back_populates="messages")
  
