from marshmallow import Schema, fields

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  firstname = fields.Str(required=True)
  lastname = fields.Str(required=True)
  username = fields.Str(required=True)
  password = fields.Str(required=True, load_only=True)

class UserLoginSchema(Schema):
   id = fields.Int(dump_only=True)
   username = fields.Str(required=True)
   password = fields.Str(required=True)

class UserLogoutSchema(Schema):
   id = fields.Int(dump_only=True)
   username = fields.Str(required=True)