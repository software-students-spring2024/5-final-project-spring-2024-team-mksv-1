from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from bson.objectid import ObjectId
import os
import datetime
import requests
from markupsafe import escape

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")
app.debug = os.getenv("FLASK_ENV", "development") == "development"

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("login.html")

@app.route("/show", methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        try:
            response = requests.get("http://api_server:1000/games", timeout=5)
            if response.status_code == 200:
                games = response.json()
                return render_template('index.html', docs=games)
            else:
                return "Failed to fetch games", 500
        except requests.exceptions.RequestException as e:
            return str(e), 500

@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        game_title = request.form['game_title']
        developer = request.form['developer']
        response = requests.post("http://api_server:1000/add_game", json={"game_title": game_title, "developer": developer})
        if response.status_code == 200:
            flash('Game added successfully!', 'success') 
        else:
            flash('An error occurred while adding the game.', 'error') 
        return redirect(url_for('show'))
    return render_template('add_game.html')

@app.route('/games/<game_id>/add_review', methods=['GET', 'POST'])
def add_review(game_id):
    if request.method == 'POST':
        review_text = request.form['review']
        user_id = session.get('user_id')
        

        if not user_id:
            flash('You must be logged in to add a review.', 'error')
            return redirect(url_for('login'))

        review_data = {
            'user_id': user_id,
            'game_id': game_id,
            'review': review_text
        }

        response = requests.post(f"http://api_server:1000/reviews", json=review_data)

        if response.status_code == 200:
            flash('Review added successfully!', 'success')
        else:
            flash('Failed to add review. Please try again.', 'error')

        return redirect(url_for('view_reviews', game_id=game_id))

    return render_template('add_review.html', game_id=game_id)

@app.route('/games/<game_id>/reviews', methods=['GET'])
def view_reviews(game_id):
    try:
        game_title = request.args.get('game_title')
        response = requests.get(f"http://api_server:1000/reviews/{game_id}")
        
        
        if response.status_code == 200:
            reviews = response.json()
        else:
            flash('Failed to fetch reviews.', 'error')
            return redirect(url_for('show'))

    except requests.exceptions.RequestException as e:
        flash(str(e), 'error')
        return redirect(url_for('show'))

    return render_template('view_reviews.html', reviews=reviews, game_id=game_id,game_title=game_title)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post("http://api_server:1000/register", json={"username": username, "password": password})
        if response.status_code == 201:
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post("http://api_server:1000/login", json={"username": username, "password": password})
        if response.status_code == 200:
            session['user_id'] = response.json().get('user_id')
            flash('Login successful!')
            return redirect(url_for('show'))
        else:
            flash('Login failed. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')
    

@app.route("/aboutus", methods=['GET'])
def aboutus():
    return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
