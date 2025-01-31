from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():

    username = request.json['username']
    password = request.json['password']
    email= request.json['email']

    if username and password and email:
        mongo.db.users.insert_one({
            'username': username,
            'password': password,
            'email': email
        })

    
    return {"message": "recieved"}

if __name__ == '__main__':

    app.run(debug=True)