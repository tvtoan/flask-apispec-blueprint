from flask import Blueprint, request, jsonify
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, doc, MethodResource
from app.schemas import UserSchema, ErrorSchema
from app.database import mongo

api_user = Blueprint('api_user', __name__)

# @api_v1_bp.route('/pet/<name>', methods=['GET'], provide_automatic_options=False)
# @doc(
#     tags=['pets'],
#     params={'name': {'description': 'pet id', 'maxLength': 24}}
# )
# @marshal_with(UserSchema)
# def get_pets():
#     return {'name': 'ABS', 'age': 25, 'status': 'pending'}

sample_get_user = {
    'x-code-samples': 
    [
        {
            "lang": "curl",
            "source": "curl -i http://localhost:5000/api/user"
        }
    ]
    }

@doc(
    tags=['user'],
)
class UserAllResource(MethodResource):
    @doc(
        summary="Get all users", 
        description="Returns list of users", 
        operationId="getAllUser",
        produces=[
            'application/json'
        ],
        **sample_get_user,
    )
    @marshal_with(
        UserSchema(many=True), 
        code=200, 
        examples={
            "application/json": 
            [
                {
                    "_id" : "5b753a9f6040fd7c219c1f92", 
                    "name" : "name1", 
                    "age" : 18, 
                    "status" : "active" 
                },
                {
                    "_id" : "5b753a9f6040fd7c219c1f92", 
                    "name" : "name1", 
                    "age" : 18, 
                    "status" : "pending" 
                }
            ]
        },
    )
    @marshal_with(ErrorSchema(), code=500)
    def get(self):
        collection_users = mongo.db.users
        cursor = collection_users.find({})
        output = []
        for document in cursor:
            output.append({'_id': str(document.get('_id')), 'name': document['name'], 'age': document['age'], 'status': document['status']})
        if cursor is None:
            return {'message': "Something went wrong on Server"}, 400
        return output, 200

    @doc(
        summary="Add new user", 
        description="Returns a new single pet is added", 
        operationId="postUser",
        produces=[
            'application/json'
        ],
    )
    @use_kwargs(
        UserSchema()
    )
    @marshal_with(ErrorSchema(), code=405, description="Invalid input")
    def post(self, **kwargs):
        # print(kwargs)
        result = UserSchema().dump(kwargs)
        collection_users = mongo.db.users
        name = result.data.get('name')
        age = result.data.get('age')
        status = result.data.get('status')
        user_id = collection_users.insert(
            {'name': name, 'age': age, 'status': status})
        new_user = collection_users.find_one({'_id': user_id})
        output = {'name': new_user['name'],
                'age': new_user['age'], 'status': new_user['status']}
        return jsonify({'result': output})

    @doc(
        summary="Update user", 
        description="Update user", 
        operationId="updateUser", 
    )
    def put(self):
        collection_users = mongo.db.users
        name = request.json['name']
        age = request.json['age']
        result = collection_users.update_one(
            {'name': name}, {'$set': {'age': age}})
        print(result.modified_count)
        return str(result.modified_count)
        
    @doc(
        summary="Delete user", 
        description="Delete user", 
        operationId="deleteUser", 
    )
    def delete(self):
        collection_users = mongo.db.users
        name = request.json['name']
        result = collection_users.delete_one({'name': name})
        print(result.deleted_count)
        return str(result.deleted_count) 

api_user.add_url_rule('/user', view_func=UserAllResource.as_view('user'))

