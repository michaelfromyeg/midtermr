from typing import TypedDict
from enum import Enum


class ClpExerciseDifficulty(int, Enum):
    """
    Enumeration of CLP question difficulties.
    """

    STAGE_1 = 1
    STAGE_2 = 2
    STAGE_3 = 3


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


class Clp2Sections(str, Enum):
    TODO = "0"


class Clp3Sections(str, Enum):
    TODO = "0"


class Clp4Sections(str, Enum):
    TODO = "0"


clpSections = [s.value for s in Clp1Sections]


class ClpSectionInformation(TypedDict):
    topic: str
    exercise_id: int


class ClpReferenece(TypedDict):
    clpSections: ClpSectionInformation


CLP_SECTION_REFERENCE: ClpReferenece = {
    "1.6": {
        "topic": "continuity",
        "exercise_id": 6,
    },
    "2.7": {
        "topic": "derivatives, exponential functions",
        "exercise_id": 12,
    },
}


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
