from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from bson import json_util, ObjectId

app = Flask(__name__)

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
    game = db.games.find_one({'_id': ObjectId(id)})
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

# CRUD for reviews
@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data or 'game_id' not in data or 'user_id' not in data or 'rating' not in data:
        return jsonify({"error": "Game ID, User ID, and Rating required"}), 400
    review_id = db.reviews.insert_one(data).inserted_id
    return jsonify({"id": str(review_id)}), 201

@app.route('/reviews/<game_id>', methods=['GET'])
def view_reviews(game_id):
    reviews = db.reviews.find({'game_id': ObjectId(game_id)})
    return Response(json_util.dumps(reviews), mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=1000)
