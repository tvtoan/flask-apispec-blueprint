from marshmallow import fields, Schema

class UserSchema(Schema):
    _id = fields.Str(dump_only=True, description="Id of User")
    name = fields.Str(required=True, description="Name of User", example="vantoan")
    age = fields.Int(description="Age of User", example="18", default=23)
    status = fields.Str(description="Status of User", default="pending")

    class Meta:
        fields = ('_id', 'name', 'age', 'status')
        # ordered = True
    

class ErrorSchema(Schema):
    message = fields.Str(required=True, description="The error message.",example="Something went wrong.")