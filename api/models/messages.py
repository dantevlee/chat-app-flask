from database.db import db 
from sqlalchemy.sql import func 
from datetime import datetime

class MessageModel(db.Model):
  __tablename__= "messages"
  
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(512), nullable=False)
  createdat = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  userid = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
  user = db.relationship("UserModel", back_populates="messages")
  
