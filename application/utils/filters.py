from application import app
import os
from datetime import datetime
from .date import convert_utc_to_asia_tz


@app.template_filter()
def filename(value: str):
    """
    Extract filename from file path
    :param value: file path
    :return: filename
    """
    return os.path.basename(value)


@app.template_filter()
def datetime(value: datetime, format="%d.%m.%Y %H:%M"):
    return value.strftime(format)


@app.template_filter()
def date(value: datetime, format="%d.%m.%Y"):
    return value.strftime(format)


@app.template_filter()
def convert_utc_asia(value: datetime):
    return convert_utc_to_asia_tz(value)


@app.template_filter()
def user(value):
    if not value:
        return "None"
    user_name = value.first_name
    if value.last_name:
        user_name += " {}".format(value.last_name)
    return user_name
