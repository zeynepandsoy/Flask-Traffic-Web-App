#from flask import Flask
from flask import render_template, current_app as app

# Delete line, left to show what was here before the Factory Application pattern was applied
#app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/")
def index():
    """Generates the home page."""
    # Remove, left in to show what was here before render_template was used
    # return "Hello, World!"
    return render_template("index.html")