import os
from dotenv import load_dotenv
load_dotenv()
# now you can use value from .env with from `os.environ` or `os.getenv`

from handleGithubEvent.githubEventRouter import githubEventRouter

# ini cuman flask sederhana, buat testing vercel e jalan ato ngga
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>Hello World!</h2> " + os.getenv('LINE_CHANNEL_SECRET')
