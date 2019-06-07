from flask import Blueprint


bp = Blueprint(__name__, 'auth')

from . import login
