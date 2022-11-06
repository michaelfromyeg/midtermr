import os, requests, boto3, markdown, random
from pathlib import Path
from markdownify import markdownify
from enum import Enum
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_file,
)
from flask_caching import Cache
from flask.json import JSONEncoder
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId, json_util
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from weasyprint import HTML

markdown_processor = markdown.Markdown()


def clp_images_url(relative_path: str) -> str:
    """
    Generator for CLP image links.
    """
    return f"https://personal.math.ubc.ca/~CLP/CLP1/clp_1_dc/{relative_path}"


def clp_exercises_url(exercise_id: int) -> str:
    """
    Generator for CLP exercise links.
    """
    return (
        f"https://personal.math.ubc.ca/~CLP/CLP1/clp_1_dc/exercises-{exercise_id}.html"
    )


class TextbookSection(float, Enum):
    """
    A enumeration of valid CLP textbook sections.
    """

    # Chapter 0: The basics
    NUMBERS = 0.1
    SETS = 0.2
    OTHER_IMPORTANT_SETS = 0.3
    FUNCTIONS = 0.4
    PARSING_FORMULAS = 0.5
    INVERSE_FUNCTIONS = 0.6
    # Chapter 1: Limits
    DRAWING_TANGENTS = 1.1
    COMPUTING_VELOCITY = 1.2
    LIMITS = 1.3
    LIMIT_LAWS = 1.4
    LIMITS_AT_INFINITY = 1.5
    CONTINUITY = 1.6
    FORMAL_LIMITS = 1.7
    FORMAL_INFINITE_LIMITS = 1.8
    PROVING_LIMIT_LAWS = 1.9
    # Chapter 2: Derivatives
    REVISITING_TANGENT_LINES = 2.1
    DEFINITION_OF_DERIVATIVE = 2.2
    INTERPRETATIONS_OF_DERIVATIVE = 2.3
    ARITHMETIC_OF_DERIVATIVES = 2.4
    PROOFS_OF_ARITHMETIC_OF_DERIVATIVES = 2.5
    USING_ARITHMETIC_OF_DERIVATIVES = 2.6
    DERIVATIVES_OF_EXPONENTIALS = 2.7
    # ...many more


class ExerciseDifficulty(int, Enum):
    """
    Enumeration of CLP question difficulties.
    """

    STAGE_1 = 1
    STAGE_2 = 2
    STAGE_3 = 3


CLP_SECTION_REFERENCE = {
    1.6: {
        "topic": "continuity",
        "exercise_id": 6,
    },
    2.7: {
        "topic": "derivatives, exponential functions",
        "exercise_id": 12,
    },
}

EXAM_TEMPLATE = {
    1.6: {
        1: 1,
        2: 2,
        3: 3,
    },
    2.7: {1: 1, 2: 2, 3: 3},
}


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

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app.config.from_mapping(config)
cache = Cache(app)

load_dotenv()


def aws_connect():
    """
    Return connection to S3.

    TODO: return type
    """
    region = os.environ.get("AWS_REGION")
    access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.client(
        "s3",
        region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    return s3


def generate_presigned_url(key: str, expires: int = 3600):
    """
    Generate presigned URL for a specific filename (key).
    """
    s3 = aws_connect()

    response = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": os.environ.get("AWS_BUCKET_NAME"), "Key": key},
        ExpiresIn=expires,
    )

    return response


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


def get_questions(
    section: TextbookSection, difficulty: ExerciseDifficulty, n: int, seed: str
) -> str:
    """
    Pull a question from the CLP.

    TODO: get rid of Markdown intermediate step; go straight to HTML

    :param section: a section of the CLP textbook
    :param difficulty: the level of difficulty of the questions to pull
    :param n: the number of questions to select in the section
    """
    random.seed(seed)

    url = clp_exercises_url(
        exercise_id=CLP_SECTION_REFERENCE[section.value]["exercise_id"]
    )

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    exercise_groups = soup.find_all("div", class_="exercisegroup")

    print(difficulty.value - 1, exercise_groups)

    exercise_group = exercise_groups[difficulty.value - 1]

    exercises_wrapper = exercise_group.find("div", class_="exercisegroup-exercises")
    exercises = exercises_wrapper.find_all("article", class_="exercise-like")

    exercises_sample = random.sample(list(exercises), n)

    full_markdown = ""

    for i, exercise in enumerate(exercises_sample):

        questions = exercise.find_all("p")
        maths = exercise.find_all("div", class_="displaymath")
        images = exercise.find_all("img")

        markdown = f"## Exercise {i + 1}\n"

        for i, question in enumerate(questions):
            question_md = markdownify(question.text, heading_style="ATX")
            markdown += f'\n<div class="displaymath">{question_md}</div>'

        for i, math in enumerate(maths):
            math_md = str(math.text).replace("\\amp", "\\newline")
            markdown += f'\n<div class="displaymath">{math_md}</div>\n'

        for i, image in enumerate(images):
            image_url = clp_images_url(relative_path=image["src"])
            markdown += f'\n<img style="display: block; margin: auto; margin-top: 2rem;" src={image_url} alt="image-{i}" />\n'

        full_markdown += f"{markdown}\n\n"

    return full_markdown


@app.route("/exams", methods=["POST"])
def new_exam():
    db = db_connect()

    raw_exam = request.get_json()
    raw_exam["date_created"] = datetime.utcnow()

    exam = Exam(**raw_exam)
    inserted_exam = db.exams.insert_one(exam.dict())

    created_exam = db.exams.find_one({"_id": inserted_exam.inserted_id})

    return jsonify(created_exam)


@app.route("/exam", methods=["GET"])
def test():
    seed = request.args.get("seed")

    question = get_questions(
        TextbookSection.DERIVATIVES_OF_EXPONENTIALS, ExerciseDifficulty.STAGE_1, 2, seed
    )

    question_html = markdown_processor.convert(question)

    html = render_template("exam.html", exam=question_html)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"tmp/midtermr-{seed}.pdf")

    # TODO: write pre-processor to convert math sections into images
    HTML(string=html).write_pdf(filename)

    return send_file(filename)


@app.route("/")
def hello():
    db = db_connect()
    # url = generate_presigned_url("MATH100 1C3.pdf")

    print("exams", db.exams)
    print("find_one", db.exams.find_one())

    return jsonify({"message": "Hello, World!"})
