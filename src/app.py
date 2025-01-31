from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

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
    
@app.errorhandler(404)
def not_found(error=None):

    message = {
        'message': 'resource not found ' + request.url,
        'status': 404
    }

    return message

if __name__ == '__main__':

    app.run(debug=True)