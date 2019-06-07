from flask import Blueprint


bp = Blueprint('api', __name__)

from . import channels, tests, quizzes, users, ratings
