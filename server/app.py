import os
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId, json_util
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json_util.default(obj)


class Exam(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId)
    name: str = Field("My Exam")
    date_created: datetime | None = Field(None)
    filename: str | None = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "date_created": "2022-11-06 22:01",
                "filename": "my-file.pdf",
            }
        }


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

load_dotenv()


def db_connect():
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


@app.route("/exams", methods=["POST"])
def new_exam():
    db = db_connect()

    raw_exam = request.get_json()
    raw_exam["date_created"] = datetime.utcnow()

    exam = Exam(**raw_exam)
    inserted_exam = db.exams.insert_one(exam.dict())

    created_student = db.exams.find_one({"_id": inserted_exam.inserted_id})

    return jsonify(created_student)


@app.route("/")
def hello():
    db = db_connect()
    print("exams", db.exams)
    print("find_one", db.exams.find_one())

    return "Hello, World!"
