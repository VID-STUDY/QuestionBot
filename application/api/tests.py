from application.api import bp
from application.core.models import Channel, Test
from application.utils import api as apiutils
from flask import jsonify, request


@bp.route('/channels/<string:channel_name>/tests', methods=['GET'])
def get_channel_tests(channel_name: str):
    tests = Channel.get_tests_by_name(channel_name)
    if tests is None:
        error = apiutils.error_message(404, 'Такой канал не зарегистрирован')
        return jsonify(error), 404
    return jsonify([test.to_dict() for test in tests]), 200


@bp.route('/channels/<string:channel_name>/tests', methods=['POST'])
def create_test(channel_name: str):
    data = request.get_json()
    channel = Channel.get_by_name(channel_name)
    new_test = Test.create(data, channel)
    return jsonify(new_test.to_dict()), 200
