"""
    String conditions base class
"""

import datetime
import logging

from dateutil.parser import parse
from marshmallow import Schema, fields, EXCLUDE, validate

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


class DateCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for string conditions
    """

    class DateFormat:
        ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, values, what, date_format=DateFormat.ISO_FORMAT, qualifier=ConditionBase.Qualifier.ForAnyValue,
                 **kwargs):
        self.date_format = date_format
        self.values = []
        if values and isinstance(values, list):
            for i in values:
                i_convert = self.convert_timestamp_from_any(i)
                if i_convert:
                    self.values.append(i_convert)
        self.what = what
        self.qualifier = qualifier

    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is string conditions satisfied

            :param what: string value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()

    def convert_string_to_timestamp(self, date_str):
        try:
            return round(
                datetime.datetime.strptime(date_str, self.date_format).replace(
                    tzinfo=datetime.timezone.utc).timestamp())
        except:
            return None

    @staticmethod
    def convert_date_to_timestamp(d):
        return round(d.replace(tzinfo=datetime.timezone.utc).timestamp())

    @staticmethod
    def convert_timestamp_to_date(timestamp):
        # try:
        return datetime.datetime.fromtimestamp(timestamp)
        # except:
        #     return None

    @staticmethod
    def convert_string_to_timestamp_from_parse(date_str):
        try:
            return round(parse(date_str).replace(tzinfo=datetime.timezone.utc).timestamp())
        except:
            return None

    def convert_timestamp_from_any(self, i):
        try:
            if isinstance(i, (int, float)):
                timestamp_i = round(i)
            elif isinstance(i, str):
                timestamp_i = self.convert_string_to_timestamp(i)
                if timestamp_i is None:
                    timestamp_i = self.convert_string_to_timestamp_from_parse(i)
            elif isinstance(i, datetime.datetime):
                timestamp_i = self.convert_date_to_timestamp(i)
            else:
                return False
            return self.convert_timestamp_to_round_minute(timestamp_i) if timestamp_i else False
        except:
            return False

    @staticmethod
    def convert_timestamp_to_round_minute(value_timestamp):
        round_timestamp = round(value_timestamp)
        return round_timestamp - (round_timestamp % 60)


class DateConditionSchema(Schema):
    """
        Base JSON schema for string conditions
    """
    values = fields.List(fields.Raw(required=True, allow_none=True), required=True, allow_none=False)
    what = fields.Raw(required=True, allow_none=True)
    qualifier = fields.String(allow_none=False, load_default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))
    date_format = fields.String(allow_none=False, load_default=DateCondition.DateFormat.ISO_FORMAT, )

    class Meta:
        unknown = EXCLUDE
