from flask import Flask, render_template, request, session, redirect, url_for
from models import db_session

app = Flask(__name__)
app.secret_key = "super_secret_key_123"


@app.route("/")
@app.route("/index")
def index():
    session.clear()
    return render_template('index.html')


@app.route("/sign_in")
def sign_in():
    session.clear()
    return render_template('sign_in.html')


@app.route("/sign_up")
def sign_up():
    session.clear()
    return render_template('sign_up.html')


if __name__ == "__main__":
    db_session.global_init("database/users.db")
    app.run("127.0.0.1", 8000, debug=True)
