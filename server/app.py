import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


@app.route("/")
def hello():
    print(os.environ.get("MONGODB_USER"))
    return "Hello, World!"
