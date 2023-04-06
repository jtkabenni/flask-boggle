from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
boggle_game = Boggle()

app.config['SECRET_KEY'] = "secrets"


@app.route("/")
def display_board():
    """Display board"""
    board = boggle_game.make_board()
    session["board"] = board
    print(session["board"])
    session["highest_score"] = session.get("highest_score", 0)
    session["times_played"] = session.get("times_played", 0)

    return render_template("base.html", board=board, highest_score=session["highest_score"], times_played=session["times_played"])


@app.route("/submitted", methods=['POST'])
def show_word():
    """Check and return status of submitted word"""
    word_guess = request.json['word']
    print(word_guess)
    board = session["board"]
    result = boggle_game.check_valid_word(board, word_guess)

    return jsonify({"result": result})


@app.route("/end", methods=['POST'])
def end_game():
    """Update times played, highest score stats"""
    score = boggle_game.compute_score()

    if score > session["highest_score"]:
        session["highest_score"] = score
    session["times_played"] += 1
    return jsonify({"times_played": session["times_played"], "highest_score": session["highest_score"]})
