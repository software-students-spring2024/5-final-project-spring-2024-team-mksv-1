from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from bson.objectid import ObjectId
import os
import datetime
import requests
from markupsafe import escape

app = Flask(__name__)


app.debug = os.getenv("FLASK_ENV", "development") == "development"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        try:
            response = requests.get("http://api_server:1000/games", timeout=5)
            if response.status_code == 200:
                games = response.json()
                return render_template('index.html', games=games)
            else:
                return "Failed to fetch games", 500
        except requests.exceptions.RequestException as e:
            return str(e), 500


@app.route('/add_game', methods=['POST'])
def add_game():
    title = request.form.get('title')
    developer = request.form.get('developer')
    game_data = {
        'title': title,
        'developer': developer
    }
    response = requests.post("http://api_server:1000/add_game", json=game_data)
    if response.ok:
        flash('Game added successfully!')
    else:
        flash('An error occurred while adding the game.')
    return redirect(url_for('home'))

@app.route('/games/<game_id>/add_review', methods=['POST'])
def add_review(game_id):
    text = request.form.get('text')
    user_id = "placeholder_user_id" # to be decided
    review_data = {
        'text': text,
        'user_id': user_id
    }
    response = requests.post(f"http://api_server:1000/games/{game_id}/add_review", json=review_data)
    if response.ok:
        flash('Review added successfully!')
    else:
        flash('An error occurred while adding the review.')
    return redirect(url_for('home'))



@app.route("/aboutus", methods=['GET'])
def aboutus():
    return render_template("aboutus.html")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
