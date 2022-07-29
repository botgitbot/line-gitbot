# ini cuman flask sederhana, buat testing vercel e jalan ato ngga
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>Hello World!</h2>"
