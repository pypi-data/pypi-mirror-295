from marshmallow import post_load
from .base import MonthDayCondition, MonthDayConditionSchema


class MonthDayGte(MonthDayCondition):

    def _is_satisfied(self) -> bool:
        day_what = self.convert_day_format_from_any(self.what)
        if not day_what or not self.values:
            return False
        if self.qualifier == self.Qualifier.ForAnyValue:
            for day_i in self.values:
                if day_what >= day_i:
                    return True
            return False
        else:
            for day_i in self.values:
                if day_what < day_i:
                    return False
            return True


class MonthDayGteSchema(MonthDayConditionSchema):
    """
        JSON schema for greater than datetime condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return MonthDayGte(**data)
