from database.db import db 
from sqlalchemy.sql import func 
from datetime import datetime

class ChannelModel(db.Model):
  __tablename__= "channels"
  
  id = db.Column(db.Integer, primary_key=True)
  channel = db.Column(db.String(512), nullable=False)
  createdat = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  messages = db.relationship("MessageModel", back_populates="channel")