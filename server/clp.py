from typing import TypedDict
from enum import Enum

CLP_BASE_URL = "https://personal.math.ubc.ca"


class ClpTextbook(int, Enum):
    CLP_1 = 1
    CLP_2 = 2
    CLP_3 = 3
    CLP_4 = 4


class ClpExerciseDifficulty(int, Enum):
    """
    Enumeration of CLP question difficulties.
    """

    STAGE_1 = 1
    STAGE_2 = 2
    STAGE_3 = 3


class ClpAnswerLevel(int, Enum):
    HINTS = 1
    ANSWERS = 2
    SOLUTIONS = 3


class Clp1Sections(str, Enum):
    """
    A enumeration of valid CLP textbook sections.
    """

    # Chapter 0: The basics
    NUMBERS = "0.1"
    SETS = "0.2"
    OTHER_IMPORTANT_SETS = "0.3"
    FUNCTIONS = "0.4"
    PARSING_FORMULAS = "0.5"
    INVERSE_FUNCTIONS = "0.6"
    # Chapter 1: Limits
    DRAWING_TANGENTS = "1.1"
    COMPUTING_VELOCITY = "1.2"
    LIMITS = "1.3"
    LIMIT_LAWS = "1.4"
    LIMITS_AT_INFINITY = "1.5"
    CONTINUITY = "1.6"
    FORMAL_LIMITS = "1.7"
    FORMAL_INFINITE_LIMITS = "1.8"
    PROVING_LIMIT_LAWS = "1.9"
    # Chapter 2: Derivatives
    REVISITING_TANGENT_LINES = "2.1"
    DEFINITION_OF_DERIVATIVE = "2.2"
    INTERPRETATIONS_OF_DERIVATIVE = "2.3"
    ARITHMETIC_OF_DERIVATIVES = "2.4"
    PROOFS_OF_ARITHMETIC_OF_DERIVATIVES = "2.5"
    USING_ARITHMETIC_OF_DERIVATIVES = "2.6"
    DERIVATIVES_OF_EXPONENTIALS = "2.7"
    DERIVATIVES_OF_TRIGONOMETRIC_FUNCTIONS = "2.8"
    CHAIN_RULE = "2.9"
    NATURAL_LOGARITHM = "2.10"
    IMPLICIT_DIFFERENTIATION = "2.11"
    INVERSE_TRIGONOMETRIC_FUNCTIONS = "2.12"
    MEAN_VALUE_THEOREM = "2.13"
    HIGHER_ORDER_DERIVATIVES = "2.14"
    LIMIT_OF_DIFFERENTIAL = "2.15"
    # Chapter 3: Applications of derivatives
    VELOCITY_AND_ACCELERATION = "3.1"
    RELATED_RATES = "3.2"
    EXPONENTIAL_GROWTH_AND_DECAY = "3.3"
    TAYLOR_POLYNOMIALS = "3.4"
    OPTIMIZATION = "3.5"
    SKETCHING_GRAPHS = "3.6"
    LHOPITAL = "3.7"
    # Chapter 4: Towards integral calculus
    ANTIDERIVATIVES = "4.1"


class Clp2Sections(str, Enum):
    TODO = "0"


class Clp3Sections(str, Enum):
    TODO = "0"


class Clp4Sections(str, Enum):
    TODO = "0"


class ClpSectionInformation(TypedDict):
    topic: str
    exercise_id: int


# TODO(michaelfromyeg): see if this actually works
class ClpReferenece(TypedDict):
    Clp1Sections: ClpSectionInformation


CLP1_SECTION_REFERENCE: ClpReferenece = {
    Clp1Sections.DRAWING_TANGENTS: {
        "topic": "drawing tangents; a first limit",
        "exercise_id": 1,
    },
    Clp1Sections.COMPUTING_VELOCITY: {
        "topic": "another limit; computing velocity",
        "exercise_id": 2,
    },
    Clp1Sections.LIMITS: {
        "topic": "limits of a function",
        "exercise_id": 3,
    },
    Clp1Sections.LIMIT_LAWS: {"topic": "limit laws", "exercise_id": 4},
    Clp1Sections.LIMITS_AT_INFINITY: {
        "topic": "limits at infinity",
        "exercise_id": 5,
    },
    Clp1Sections.CONTINUITY: {
        "topic": "continuity",
        "exercise_id": 6,
    },
    Clp1Sections.REVISITING_TANGENT_LINES: {
        "topic": "revisiting tangent lines",
        "exercise_id": 7,
    },
    Clp1Sections.DEFINITION_OF_DERIVATIVE: {
        "topic": "definition of the derivative",
        "exercise_id": 8,
    },
    Clp1Sections.INTERPRETATIONS_OF_DERIVATIVE: {
        "topic": "interpretations of the derivative",
        "exercise_id": 9,
    },
    Clp1Sections.ARITHMETIC_OF_DERIVATIVES: {
        "topic": "arithmetic of derivatives",
        "exercise_id": 10,
    },
    Clp1Sections.USING_ARITHMETIC_OF_DERIVATIVES: {
        "topic": "using the arithmetic of derivatives",
        "exercise_id": 11,
    },
    Clp1Sections.DERIVATIVES_OF_EXPONENTIALS: {
        "topic": "derivatives, exponential functions",
        "exercise_id": 12,
    },
    Clp1Sections.DERIVATIVES_OF_TRIGONOMETRIC_FUNCTIONS: {
        "topic": "derivatives, trigonometric functions",
        "exercise_id": 13,
    },
    Clp1Sections.CHAIN_RULE: {"topic": "chain rule", "exercise_id": 14},
    Clp1Sections.NATURAL_LOGARITHM: {
        "topic": "natural logarithm",
        "exercise_id": 15,
    },
    Clp1Sections.IMPLICIT_DIFFERENTIATION: {
        "topic": "implicit differentiation",
        "exercise_id": 16,
    },
    Clp1Sections.INVERSE_TRIGONOMETRIC_FUNCTIONS: {
        "topic": "inverse trigonometric functions",
        "exercise_id": 17,
    },
    Clp1Sections.MEAN_VALUE_THEOREM: {
        "topic": "mean value theorem",
        "exercise_id": 18,
    },
    Clp1Sections.HIGHER_ORDER_DERIVATIVES: {
        "topic": "higher order derivatives",
        "exercise_id": 19,
    },
    Clp1Sections.VELOCITY_AND_ACCELERATION: {
        "topic": "velocity and acceleration",
        "exercise_id": 20,
    },
}

CLP_SECTION_REFERENCES = {ClpTextbook.CLP_1: CLP1_SECTION_REFERENCE}


def clp_path(clp: ClpTextbook) -> str:
    base_path = f"~CLP/CLP{clp.value}"
    match clp:
        case ClpTextbook.CLP_1:
            return f"{base_path}/clp_1_dc"
        case ClpTextbook.CLP_2:
            return f"{base_path}/clp_2_ic"
        case ClpTextbook.CLP_3:
            return f"{base_path}/clp_3_mc"
        case ClpTextbook.CLP_4:
            return f"{base_path}/clp_4_vc"
    raise ValueError("Invalid CLP textbook based to clp_path")


def clp_images_url(clp: ClpTextbook, relative_path: str) -> str:
    """
    Generator for CLP image links.
    """

    return f"{CLP_BASE_URL}/{clp_path(clp)}/{relative_path}"


def clp_exercises_url(clp: ClpTextbook, exercise_id: int) -> str:
    """
    Generator for CLP exercise links.
    """
    return f"{CLP_BASE_URL}/{clp_path(clp)}/exercises-{exercise_id}.html"


def clp_solutions_url(clp: ClpTextbook, level: ClpAnswerLevel) -> str:
    base_url = f"{CLP_BASE_URL}/{clp_path(clp)}"
    match level:
        case ClpAnswerLevel.HINTS:
            return f"{base_url}/app_hint.html"
        case ClpAnswerLevel.ANSWERS:
            return f"{base_url}/app_answ.html"
        case ClpAnswerLevel.SOLUTIONS:
            return f"{base_url}/app_soln.html"
    raise ValueError("Invalid CLP textbook based to clp_path")


def int2clp(x: int) -> ClpTextbook:
    if x not in [t.value for t in ClpTextbook]:
        raise ValueError(f"CLP textbook {x} does not exist")
    return ClpTextbook(x)


def process_clp_sections(clp: ClpTextbook, sections: dict) -> dict:
    def pop_clp(key: str) -> str:
        return key[2:]

    return {pop_clp(key): sections[key] for key in sections}


def build_template(clp: ClpTextbook, sections: dict, length: int) -> dict:
    template = {}

    all_sections = [s.value for s in Clp1Sections]
    for section_name, include in sections.items():
        if not include or section_name not in all_sections:
            continue

        difficulties = [e.value for e in ClpExerciseDifficulty]
        section_object = {}
        for difficulty in difficulties:
            section_object[difficulty] = length

        template[section_name] = section_object
    return template

# TODO(michaelfromyeg): remove old templates
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
