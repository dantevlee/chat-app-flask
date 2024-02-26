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

class UserNameSchema(Schema):
   id = fields.Int(dump_only=True)
   username = fields.Str(required=True)

class ChannelSchema(Schema):
   id = fields.Int(dump_only=True)
   channel = fields.Str(required=True)
   createdat = fields.DateTime(dump_only=True)

class SendMessageSchema(Schema):
   id = fields.Int(dump_only=True)
   text = fields.Str(required=True)
   createdat = fields.Date(dump_only=True)
   user = fields.Str(required=True)
   channelid = fields.Int(required=True)

class MessageSchema(Schema):
   id = fields.Int(dump_only=True)
   createdat = fields.Date(dump_only=True)
   user = fields.Str(dump_only=True)
   channel = fields.Str(dump_only=True)
   text = fields.Str(required=True)