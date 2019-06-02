import json
import os
from typing import List, Tuple
from datetime import datetime
from application.utils.date import convert_utc_to_asia_tz

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings = json.loads(open(os.path.join(_basedir, 'strings.json'), 'r').read())


def get_string(key: str) -> str:
    return _strings.get(key, 'no_string')


def from_test(test) -> str:
    test_content = '<b>Вопрос:</b>\n'
    test_content += test.question
    return test_content


def from_user_points_rating(user_points_list: List[Tuple[str, int]], start_date: datetime, end_date: datetime):
    format_date_str = '%d.%m.%Y'
    rating_content = '<b>Еженедельный рейтинг за {} - {}</b>' \
        .format(convert_utc_to_asia_tz(start_date).strftime(format_date_str),
                convert_utc_to_asia_tz(end_date).strftime(format_date_str))
    rating_content += '\n\n'
    for user_points in user_points_list:
        rating_content += '{} - {}'.format(user_points[0], user_points[1])
    return rating_content
