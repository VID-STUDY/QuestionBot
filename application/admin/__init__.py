from flask import Blueprint


bp = Blueprint(__name__, 'admin')

from . import index
