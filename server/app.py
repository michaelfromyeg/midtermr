import os, requests, boto3, markdown, random
from markdownify import markdownify

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_file,
)
from flask_cors import CORS
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
from clp import (
    ClpTextbook,
    Clp1Sections,
    ClpExerciseDifficulty,
    CLP_SECTION_REFERENCES,
    clp_images_url,
    clp_exercises_url,
)

# from flask_ngrok import run_with_ngrok

markdown_processor = markdown.Markdown()


LONG_EXAM_TEMPLATE = {
    "1.6": {
        1: 3,
        2: 2,
        3: 1,
    },
    "2.7": {1: 3, 2: 2, 3: 1},
}

SHORT_EXAM_TEMPLATE = {
    "1.6": {
        1: 2,
        2: 1,
    },
    "2.7": {1: 2, 2: 1},
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
    seed: str | None = Field(None)
    length: int = Field(1)
    content: str = Field("")
    date_created: datetime | None = Field(None)

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
CORS(app)  # This will enable CORS for all routes

# run_with_ngrok(app)


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
    section: Clp1Sections, difficulty: ClpExerciseDifficulty, n: int, seed: str
) -> str:
    """
    Pull a question from the CLP.

    TODO: get rid of Markdown intermediate step; go straight to HTML

    :param section: a section of the CLP textbook
    :param difficulty: the level of difficulty of the questions to pull
    :param n: the number of questions to select in the section
    """
    random.seed(seed)

    clp = ClpTextbook.CLP_1
    url = clp_exercises_url(
        clp=clp,
        exercise_id=CLP_SECTION_REFERENCES[clp][section]["exercise_id"],
    )

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    exercise_groups = soup.find_all("div", class_="exercisegroup")

    exercise_group = exercise_groups[difficulty.value - 1]

    exercises_wrapper = exercise_group.find("div", class_="exercisegroup-exercises")
    exercises = exercises_wrapper.find_all("article", class_="exercise-like")

    exercises_sample = random.sample(list(exercises), n)

    full_html = ""

    for i, exercise in enumerate(exercises_sample):

        questions = exercise.find_all("p")
        maths = exercise.find_all("div", class_="displaymath")
        images = exercise.find_all("img")

        html = f"<h4>Exercise {i + 1}</h4>"

        for i, question in enumerate(questions):
            question_md = markdownify(question.text, heading_style="ATX")
            html += f"\n<p>{question_md}</p>\n"

        for i, math in enumerate(maths):
            math_md = str(math.text).replace("\\amp", "\\newline")
            html += f"<p>{math_md}</p>\n"

        for i, image in enumerate(images):
            image_url = clp_images_url(
                clp=ClpTextbook.CLP_1, relative_path=image["src"]
            )
            html += f'<img style="display: block; margin: auto; margin-top: 2rem;" src={image_url} alt="image-{i}" />\n'

        full_html += html

    return full_html

@app.route("/textbooks", methods=["GET"])
def get_textbooks():
    """
    Return textbook information and available sections.
    """

    return jsonify({
        "textbooks": CLP_SECTION_REFERENCES
    })

@app.route("/exam/<filename>", methods=["GET"])
def get_exam_by_filename(filename: str):
    """
    Get an exam's PDF file.

    TODO: replace this with S3
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"tmp/{filename}")

    return send_file(filename)


@app.route("/exams/<name>", methods=["GET"])
def get_exam_by_name(name: str):
    db = db_connect()

    exam = db.exams.find_one({"name": name})

    return jsonify(exam)


@app.route("/exams", methods=["GET"])
def get_exams():
    db = db_connect()

    exams = list(db.exams.find())

    return jsonify({"exams": exams})


@app.route("/exams", methods=["POST"])
def new_exam():
    """
    Create a new exam.
    """

    db = db_connect()

    seed = request.args.get("seed")

    raw_exam = request.get_json()
    raw_exam["date_created"] = datetime.utcnow()

    template = LONG_EXAM_TEMPLATE if raw_exam["length"] == 1 else SHORT_EXAM_TEMPLATE

    full_html = ""
    for section, value in template.items():
        full_html += f"<h2>Section {section}</h2>"
        for difficulty, n in value.items():
            full_html += f"<h3>Difficulty {difficulty}</h3>"
            question_html = get_questions(
                Clp1Sections(section), ClpExerciseDifficulty(difficulty), n, seed
            )
            full_html += question_html

    raw_exam["content"] = full_html

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"tmp/midtermr-{seed}.pdf")

    if not os.path.exists(filename):
        html = render_template("exam.html", exam=question_html)
        # TODO: write pre-processor to convert math sections into images
        HTML(string=html).write_pdf(filename)

    exam = Exam(**raw_exam)
    inserted_exam = db.exams.insert_one(exam.dict())

    created_exam = db.exams.find_one({"_id": inserted_exam.inserted_id})

    return jsonify(created_exam)


@app.route("/")
def hello():
    return jsonify({"message": "Hello, World!"})


port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=port)
