from datetime import date
from typing import Annotated, Literal, Sequence

from pydantic import BaseModel, Field, field_validator

from vitalx.types.providers import Labs, Providers

DateTimeUnit = Literal["minute", "hour", "day", "week", "month", "year"]


class Placeholder(BaseModel):
    placeholder: Literal[True]


class Period(BaseModel):
    value: Annotated[int, Field(ge=1)] = 1
    unit: DateTimeUnit


class RelativeTimeframe(BaseModel):
    type: Literal["relative"]
    anchor: date
    past: Period


Timeframe = RelativeTimeframe | Placeholder


# Select Expressions

TableT = Literal["sleep", "activity"]

SleepColumnT = Literal[
    "session_start",
    "session_end",
    "state",
    "duration_second",
    "stage_asleep_second",
    "stage_awake_second",
    "stage_light_second",
    "stage_rem_second",
    "stage_deep_second",
    "stage_unknown_second",
    "latency_second",
    "heart_rate_minimum",
    "heart_rate_mean",
    "heart_rate_maximum",
    "heart_rate_dip",
    "efficiency",
    "hrv_mean_rmssd",
    "hrv_mean_sdnn",
    "skin_temperature_delta",
    "respiratory_rate",
    "score",
    "source_type",
    "source_provider",
    "source_app_id",
]


ActivityColumnT = Literal[
    "date",
    "calories_total",
    "calories_active",
    "steps",
    "distance_meter",
    "floors_climbed",
    "duration_active_second",
    "intensity_sedentary_second",
    "intensity_low_second",
    "intensity_medium_second",
    "intensity_high_second",
    "heart_rate_mean",
    "heart_rate_min",
    "heart_rate_max",
    "heart_rate_resting",
    "source_type",
    "source_provider",
    "source_app_id",
]

AggregateFunctionT = Literal[
    "mean", "min", "max", "sum", "count", "median", "stddev", "oldest", "newest"
]


class SleepColumnExpr(BaseModel):
    sleep: SleepColumnT


class ActivityColumnExpr(BaseModel):
    activity: ActivityColumnT


class IndexColumnExpr(BaseModel):
    index: TableT


class GroupKeyColumnExpr(BaseModel):
    group_key: int | Literal["*"] = Field(default="*")


ColumnExpr = SleepColumnExpr | ActivityColumnExpr | IndexColumnExpr | GroupKeyColumnExpr


class AggregateExpr(BaseModel):
    arg: ColumnExpr
    func: AggregateFunctionT


SelectExpr = AggregateExpr | ColumnExpr

# Partitioning and Swizzling

DatePartT = DateTimeUnit | Literal["weekday", "week_of_year", "day_of_year"]


class DateTruncExpr(BaseModel):
    date_trunc: Period
    arg: IndexColumnExpr | Placeholder


class DatePartExpr(BaseModel):
    arg: IndexColumnExpr | Placeholder
    date_part: DatePartT


GroupByExpr = DateTruncExpr | DatePartExpr

# Query


class QueryInstruction(BaseModel):
    select: Sequence[SelectExpr]
    group_by: list[GroupByExpr]
    split_by_source: bool = Field(default=False)

    @field_validator("group_by", mode="after")
    @classmethod
    def validate_group_by(cls, v: list[GroupByExpr]) -> list[GroupByExpr]:
        date_trunc_count = sum(isinstance(expr, DateTruncExpr) for expr in v)
        if date_trunc_count >= 2:
            raise ValueError(
                f"group_by supports at most 1 DateTruncExpr. found {date_trunc_count}."
            )
        return v


class QueryConfig(BaseModel):
    week_starts_on: Literal["sunday", "monday"] = "monday"
    provider_priority_overrides: list[Providers | Labs] | None = None


class Query(BaseModel):
    timeframe: Timeframe
    instructions: list[QueryInstruction]
    config: QueryConfig = Field(default_factory=lambda: QueryConfig())
