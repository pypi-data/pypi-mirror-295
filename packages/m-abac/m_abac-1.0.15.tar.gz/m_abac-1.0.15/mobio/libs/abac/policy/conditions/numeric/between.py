"""
    Numeric Between
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Between(NumericCondition):
    """
        Condition for Between
    """

    def _is_satisfied(self) -> bool:
        if not self.is_number(self.what) or not self.values or len(self.values) != 2:
            return False
        if self.values[0] <= self.what <= self.values[1]:
            return True
        return False


class BetweenSchema(NumericConditionSchema):
    """
        JSON schema for greater than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Between(**data)
