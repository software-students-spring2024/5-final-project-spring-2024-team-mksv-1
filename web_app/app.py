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
    if request.method == 'POST':
        text = request.form.get('text')
        user_id = "placeholder_user_id"  # Replace with actual user identification logic
        review_data = {
            'text': text,
            'user_id': user_id,
        }
        # Post the new review
        post_response = requests.post(f"http://api_server:1000/reviews", json=review_data)
        if not post_response.ok:
            flash('An error occurred while adding the review.')
        return redirect(url_for('reviews', game_id=game_id))
    
#Added a route to display reviews
@app.route('/games/<game_id>/reviews')
def view_reviews(game_id):
    try:
        get_response = requests.get(f"http://api_server:1000/games/{game_id}/reviews")
        reviews = get_response.json() if get_response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        reviews = []
        flash(str(e))
    return render_template('view_reviews.html', game_id=game_id, reviews=reviews)

@app.route("/aboutus", methods=['GET'])
def aboutus():
    return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
