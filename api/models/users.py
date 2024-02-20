from database.db import db 

class UserModel(db.Model):
  __tablename__= "users"
  
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(225), nullable=False)
  lastname = db.Column(db.String(225), nullable=False)
  username = db.Column(db.String(225), nullable=False, unique=True)
  password = db.Column(db.String(256), nullable=False)