"""
    Numeric greater than conditions
"""

from marshmallow import post_load

from .base import DateCondition, DateConditionSchema


class DateGt(DateCondition):
    """
        Condition for number `what` greater than `value`
    """

    def _is_satisfied(self) -> bool:
        timestamp_what = self.convert_timestamp_from_any(self.what)
        if not timestamp_what or not self.values:
            return False
        if self.qualifier == self.Qualifier.ForAnyValue:
            for timestamp_i in self.values:
                if timestamp_what > timestamp_i:
                    return True
            return False
        else:
            for timestamp_i in self.values:
                if timestamp_what <= timestamp_i:
                    return False
            return True


class DateGtSchema(DateConditionSchema):
    """
        JSON schema for greater than datetime condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return DateGt(**data)
