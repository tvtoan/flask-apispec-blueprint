from flask import Blueprint
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, MethodResource


class Pet:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class PetSchema(Schema):
    class Meta:
        fields = ('name', 'category', 'size')

api_v1_bp = Blueprint('api_v1', __name__)

# @api_v1_bp.route('/pets/<name>')
# @use_kwargs({'name': fields.Str()})
# @marshal_with(PetSchema)
# def get_pets(**kwargs):
#     return {'name': 'ABS', 'size': 25, 'category': 'pending'}

class PetResource(MethodResource):

    @use_kwargs({'name': fields.Str()})
    @marshal_with(PetSchema)
    def get(self, name):
        return {'name': 'ABS', 'size': 25, 'category': 'pending'}

api_v1_bp.add_url_rule('/pet/<name>', view_func=PetResource.as_view('pet'))

