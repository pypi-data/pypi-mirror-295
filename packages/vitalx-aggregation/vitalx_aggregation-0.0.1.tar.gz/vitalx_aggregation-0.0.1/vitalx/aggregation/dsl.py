from typing import Any, Literal, NamedTuple, cast, overload

from vitalx.aggregation.types import (
    ActivityColumnExpr,
    ActivityColumnT,
    AggregateExpr,
    ColumnExpr,
    DatePartExpr,
    DatePartT,
    DateTimeUnit,
    DateTruncExpr,
    GroupByExpr,
    GroupKeyColumnExpr,
    IndexColumnExpr,
    Period,
    QueryInstruction,
    SelectExpr,
    SleepColumnExpr,
    SleepColumnT,
)


def period(value: int, unit: DateTimeUnit) -> Period:
    return Period(value=value, unit=unit)


class SupportsAggregate:
    @property
    def _column_expr(self) -> ColumnExpr:
        return cast(ColumnExpr, self)

    def sum(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="sum")

    def mean(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="mean")

    def min(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="min")

    def max(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="max")

    def median(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="median")

    def stddev(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="stddev")

    def newest(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="newest")

    def oldest(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="oldest")

    def count(self) -> AggregateExpr:
        return AggregateExpr(arg=self._column_expr, func="count")


class SleepColumnExprLike(SleepColumnExpr, SupportsAggregate):
    pass


class ActivityColumnExprLike(ActivityColumnExpr, SupportsAggregate):
    pass


class Sleep:
    @staticmethod
    def col(name: SleepColumnT) -> SleepColumnExprLike:
        return SleepColumnExprLike(sleep=name)

    @staticmethod
    def index() -> IndexColumnExpr:
        """
        The Sleep Session End datetime index (YYYY-mm-dd HH:mm:ss).
        """
        return IndexColumnExpr(index="sleep")


class Activity:
    @staticmethod
    def col(name: ActivityColumnT) -> ActivityColumnExprLike:
        return ActivityColumnExprLike(activity=name)

    @staticmethod
    def index() -> IndexColumnExpr:
        """
        The Activity calendar date index (YYYY-mm-dd).
        """
        return IndexColumnExpr(index="activity")


def group_key(offset: int | Literal["*"]) -> GroupKeyColumnExpr:
    """
    The group key columns created by the GroupBy expressions. The offset corresponds
    to the expression declaration order.

    Specify `*` to select all group key columns.
    """
    return GroupKeyColumnExpr(group_key=offset)


@overload
def date_trunc(argument: IndexColumnExpr, period: Period, /) -> DateTruncExpr:
    """
    Truncate the `argument` at the granularity of `period`.

    For example, given these inputs:
    * `argument` is `2024-08-10 12:34:56`
    * `period` is `period(30, "minute")`

    The output is `2024-08-10 12:30:00`.
    """
    ...


@overload
def date_trunc(
    argument: IndexColumnExpr, value: int, unit: DateTimeUnit, /
) -> DateTruncExpr:
    """
    Truncate the `argument` at the granularity of a period length specified by
    `value` and `unit`.

    For example, given these inputs:
    * `argument` is `2024-08-10 12:34:56`
    * Period length is 30 minutes (`value` is 30, and `unit` is `"minute"`)

    The output is `2024-08-10 12:30:00`.
    """
    ...


def date_trunc(argument: IndexColumnExpr, *args: Any) -> DateTruncExpr:
    if len(args) == 1:
        assert isinstance(args[0], Period)
        return DateTruncExpr(arg=argument, date_trunc=args[0])

    if len(args) == 2:
        return DateTruncExpr(
            arg=argument, date_trunc=Period(value=args[0], unit=args[1])
        )

    raise ValueError(f"unsupported input: {args}")


def date_part(argument: IndexColumnExpr, part: DatePartT) -> DatePartExpr:
    """
    Extract a specific date or time component of the datetime `argument`.
    """
    return DatePartExpr(arg=argument, date_part=part)


class QueryInstructionPartial(NamedTuple):
    attributes: dict[str, Any]

    def group_by(self, *exprs: GroupByExpr) -> "QueryInstructionPartial":
        return QueryInstructionPartial({**self.attributes, "group_by": exprs})

    def split_by_source(self, enabled: bool, /) -> "QueryInstructionPartial":
        return QueryInstructionPartial({**self.attributes, "split_by_source": enabled})

    def finalize(self) -> QueryInstruction:
        return QueryInstruction.model_validate(self.attributes)


def select(*exprs: SelectExpr) -> QueryInstructionPartial:
    return QueryInstructionPartial({"select": exprs})
