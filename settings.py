import shelve
from config import basedir
import os


filename = os.path.join(basedir, 'settings.data')


def get_top_10_points() -> int:
    settings = shelve.open(filename)
    value = settings['top_10_points']
    settings.close()
    return value


def get_first_try_points() -> int:
    settings = shelve.open(filename)
    value = settings['first_try_points']
    settings.close()
    return value


def get_not_first_try_points() -> int:
    settings = shelve.open(filename)
    value = settings['not_first_try_points']
    settings.close()
    return value


def set_top_10_points(points: int):
    settings = shelve.open(filename)
    settings['top_10_points'] = points
    settings.close()


def set_first_try_points(points: int):
    settings = shelve.open(filename)
    settings['first_try_points'] = points
    settings.close()


def set_not_first_try_points(points: int):
    settinsg = shelve.open(filename)
    settinsg['not_first_try_points'] = points
    settinsg.close()
