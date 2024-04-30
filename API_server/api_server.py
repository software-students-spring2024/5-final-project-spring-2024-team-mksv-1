import os
from flask import Flask, jsonify, request, Response, session
from pymongo import MongoClient
from bson import json_util, ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

client = MongoClient("mongodb://db:27017/")
db = client.game

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Game Review Platform API"})

@app.route('/games', methods=['GET'])
def get_games():
    
    games = db.games.find()
    return Response(json_util.dumps(games), mimetype='application/json')


@app.route('/games/<id>', methods=['GET'])
def get_game(id):
    game = db.games.find_one({'_id': id})
    return Response(json_util.dumps(game), mimetype='application/json') if game else ('', 404)

@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.get_json()
    if not data or 'game_title' not in data or 'developer' not in data:
        return jsonify({"error": "Title and developer required"}), 400
    game_id = db.games.insert_one(data).inserted_id
    return jsonify({"id": str(game_id)}), 200

@app.route('/delete_games/<id>', methods=['DELETE'])
def delete_game(id):
    result = db.games.delete_one({'_id': ObjectId(id)})
    return ('', 204) if result.deleted_count > 0 else ('', 404)

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data or 'user_id' not in data or 'game_id' not in data or 'review' not in data:
        return jsonify({"error": "Review, user_id, and game_id required"}), 400

    review_id = db.reviews.insert_one(data).inserted_id
    return jsonify({"review_id": str(review_id)}), 200

@app.route('/reviews/<game_id>', methods=['GET'])
def view_reviews(game_id):
    try:
        reviews = db.reviews.find({'game_id': game_id})
        reviews_list = list(reviews)
        
        return Response(json_util.dumps(reviews_list), mimetype='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    user = db.users.find_one({'username': data['username']})
    if user:
        return jsonify({"error": "Username already exists"}), 400
    user_id = db.users.insert_one(data).inserted_id
    return jsonify({"user_id": str(user_id)}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    user = db.users.find_one({'username': data['username'], 'password': data['password']})
    if user:
        session['user_id'] = str(user['_id'])
        return jsonify({"user_id": str(user['_id'])}), 200
    return jsonify({"error": "Invalid username or password"}), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=1000)
