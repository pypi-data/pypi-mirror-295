"""
    Numeric Between
"""

from marshmallow import post_load

from .base_list import NumericListCondition, NumericListConditionSchema


class ListBetween(NumericListCondition):
    """
        Condition for Between
    """

    def _is_satisfied(self) -> bool:
        if not self.what or not self.values or len(self.values) != 2:
            return False
        for i in self.what:
            if self.values[0] <= i <= self.values[1]:
                return True
        return False


class ListBetweenSchema(NumericListConditionSchema):
    """
        JSON schema for greater than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return ListBetween(**data)
