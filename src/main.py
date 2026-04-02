from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

@app.route("/")
@app.route("/index")
def index():
    session.clear()
    return render_template('index.html')


if __name__ == "__main__":
    app.run("127.0.0.1", 8000, debug=True)
