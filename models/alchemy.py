from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

db = SQLAlchemy()


def as_dict(iterable, extender=None, *args):
    if not extender:
        return [element.as_dict() for element in iterable]
    else:
        return [element.as_dict(extender(element, *args)) for element in iterable]
