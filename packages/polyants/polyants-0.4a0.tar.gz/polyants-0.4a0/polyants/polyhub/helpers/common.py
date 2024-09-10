""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

import logging
import datetime

from traceback import format_tb
from polyants.polyhub.constants import DEFAULT_ID
from polyants.polyhub.enums import GenericState, ObjectType
from polyants.polyhub.helpers.redis import send_event


def get_now(format_=None, utc=False):
    """Возвращает текущую дату и время, с учетом формата, если задан.
    Пример формата: `%Y-%m-%dT%H:%M:%S`
    """
    now = datetime.datetime.now(datetime.UTC) if utc else datetime.datetime.now()
    return now.strftime(format_) if format_ else now


def get_object_class_type(cls) -> ObjectType:
    """Возвращает тип объекта на основе класса."""
    return ObjectType[cls.__name__.upper()]


def get_type_object_class(type_: ObjectType) -> str:
    """Возвращает наименование класса объекта на основании его типа."""
    return ObjectType(type_).name.capitalize()


def get_object_type(object_, type_=None) -> ObjectType:
    """Возвращает тип объекта."""
    return type_ or get_object_class_type(object_.__class__)


def get_object_class(object_) -> str:
    """Возвращает наименование класса объекта."""
    type_ = get_object_type(object_)
    return get_type_object_class(type_)


def get_active_state(state_enum=GenericState):
    return state_enum.ACTIVE & ~state_enum.DELETED


def is_object_active(object_, state_enum=GenericState):
    return object_.state & (state_enum.DELETED | state_enum.ACTIVE) == state_enum.ACTIVE


def log_event(event_type, object_type, object_id=DEFAULT_ID, message='', context=None):
    """Отправляет событие в поток redis."""
    context = context or dict()

    key = f'{event_type.value}::{object_type.value}::{object_id}'
    value = {'message': message, 'context': context}
    send_event(key, value)


def log_traceback(error, logger=None):
    result = error
    logger = logger or logging.getLogger()

    if isinstance(error, Exception) and logger.getEffectiveLevel() == logging.DEBUG:
        tb = ''.join(format_tb(error.__traceback__))

        result = f'{error}\n{tb}'
    elif error:
        result = str(error)

    return result
