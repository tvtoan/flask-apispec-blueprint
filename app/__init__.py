import json
from flask import Flask
from app.pet.views import api_v1_bp, PetResource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

# register Blueprint
app.register_blueprint(api_v1_bp, url_prefix='/api')

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

# app.add_url_rule('/pet/<name>', view_func=PetResource.as_view('PetResource'))
print(app.url_map._rules_by_endpoint)
docs.register(PetResource, blueprint="api_v1", endpoint="pet")

# with open('swagger.json', 'w') as f:
#     json.dump(docs.spec.to_dict(), f)