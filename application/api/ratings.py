from . import bp
from flask import jsonify
from application.utils import api as apiutils
from application.core.models import Channel


def _sort_tests(test):
    answers = test.answers.all()
    return sum((answer.points for answer in answers if answer.is_right))


@bp.route('/channels/<int:channel_name>/rating', methods=['GET'])
def channel_ratings(channel_name: str):
    channel = Channel.get_by_name(channel_name)
    if not channel:
        error = apiutils.error_message(404, 'Такой канал не зарегистрирован')
        return jsonify(error), 404
    tests = channel.get_channel_tests()
    tests.sort(key=_sort_tests)
    return jsonify(tests), 200
