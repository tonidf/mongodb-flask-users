from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util, ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():

    username = request.json['username']
    password = request.json['password']
    email= request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        
        id = mongo.db.users.insert_one(
            {
            'username': username,
            'password': hashed_password,
            'email': email
            }
        )

        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }

        return response
    else:
        return not_found(), 404
    
@app.route('/users/<id>', methods=['GET'])
def get_one_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(user)

    return Response(response, mimetype='application/json')
    
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)

    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    users = mongo.db.users.delete_one({'id': ObjectId(id)})
    response = jsonify({
        'message': 'User' + id + ' Deleted succesfully'
    })
    response.status_code = 200

    return response

@app.route('/users/<id>', methods=['PUT'])
def delete_users(id):
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    update_data = {}
    
    if username:
        update_data['username'] = username
    
    if username:
        update_data['password'] = generate_password_hash(password)    
    if username:
        update_data['email'] = email
    
    if update_data:
        mongo.db.users.update_one({"_id": ObjectId(id)}, {'$set': update_data})
        return jsonify({'message': 'user updated succesfully'})
    else:
        return jsonify({"message": "No data provided"})

    return response
    
@app.errorhandler(404)
def not_found(error=None):

    message = {
        'message': 'resource not found ' + request.url,
        'status': 404
    }

    return message

if __name__ == '__main__':

    app.run(debug=True)