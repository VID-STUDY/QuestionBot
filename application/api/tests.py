from application.api import bp
from application.core.models import Channel
from application.utils import api as apiutils
from flask import jsonify, request


@bp.route('/channels/<string:channel_name>/tests', methods=['GET'])
def get_channel_tests(channel_name: str):
    tests = Channel.get_tests_by_name(channel_name)
    if tests is None:
        error = apiutils.error_message(404, 'Такой канал не зарегистрирован')
        return jsonify(error), 404
    return jsonify([test.to_dict() for test in tests]), 200

