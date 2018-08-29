from flask import Flask, Blueprint
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, MethodResource


class Pet:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class PetSchema(Schema):
    class Meta:
        fields = ('name', 'category', 'size')

app = Flask(__name__)
blueprint_demo = Blueprint("api", __name__)

# @blueprint_demo.route('/pets/<name>')
# @use_kwargs({'name': fields.Str()})
# @marshal_with(PetSchema)
# def get_pets(**kwargs):
#     return {'name': 'ABS', 'size': 25, 'category': 'pending'}

class PetResource(MethodResource):

    @use_kwargs({'name': fields.Str()})
    @marshal_with(PetSchema)
    def get(self, name):
        return {'name': 'ABS', 'size': 25, 'category': 'pending'}


blueprint_demo.add_url_rule('/pet/<name>', view_func=PetResource.as_view('pet'))
app.register_blueprint(blueprint_demo, url_prefix="/api")

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='pets',
        version='v1',
        # openapi_version='3.0.1',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
docs = FlaskApiSpec(app)
# print(app.url_map._rules_by_endpoint)
docs.register(PetResource, blueprint="api", endpoint="pet")
# docs.register(get_pets, blueprint="api")

if __name__ == '__main__':
    app.run(debug=True)