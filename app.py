from flask import Flask, render_template,session, request, jsonify
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
  return render_template("base.html", board = board)

@app.route("/submitted", methods=["POST"] )
def show_word():
  word_guess = request.form.get('word', "")

  return {"word": word_guess}

