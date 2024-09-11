"""
    Numeric conditions base class
"""

import logging

from marshmallow import Schema, fields, EXCLUDE, validate

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


class NumericListCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for numeric conditions
    """

    def __init__(self, values, what, qualifier=ConditionBase.Qualifier.ForAnyValue, **kwargs):
        values_format = [self.convert_number(i) for i in values if self.is_number(i)] if isinstance(
            values, list) else []
        what_format = [self.convert_number(i) for i in what if self.is_number(i)] if isinstance(what, list) else []
        self.values = values_format
        self.what = what_format
        self.qualifier = qualifier

    @staticmethod
    def is_number(value) -> bool:
        """
            Check if value is a number
        """
        try:
            if isinstance(value, str):
                float(value)
                return True
            return isinstance(value, (float, int))
        except:
            return False

    @staticmethod
    def convert_number(value):
        """
            Check if value is a number and convert
        """
        try:
            if isinstance(value, str):
                return float(value)
            return value
        except:
            return value


    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is numeric conditions satisfied

            :param what: numeric value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class NumericListConditionSchema(Schema):
    """
        Base JSON schema for numeric conditions
    """
    values = fields.List(fields.Number(required=True, allow_none=False), required=True, allow_none=False)
    what = fields.List(fields.Number(required=True, allow_none=False), required=True, allow_none=True)
    qualifier = fields.String(allow_none=False, load_default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))

    class Meta:
        unknown = EXCLUDE
