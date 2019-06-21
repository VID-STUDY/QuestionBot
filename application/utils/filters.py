from application import app
import os
from datetime import datetime


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
