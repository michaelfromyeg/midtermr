import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


def connect_db():
    """
    Return connection to MongoDB instance.

    TODO: return type
    """
    user = os.environ.get("MONGODB_USER")
    password = os.environ.get("MONGODB_PASSWORD")
    name = os.environ.get("MONGODB_DATABASE_NAME")

    client = MongoClient(
        f"mongodb+srv://{user}:{password}@midtermrdb.wionr6r.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi("1"),
    )

    return client[name]


@app.route("/")
def hello():
    db = connect_db()
    print("exams", db.exams)
    print("find_one", db.exams.find_one())

    return "Hello, World!"
