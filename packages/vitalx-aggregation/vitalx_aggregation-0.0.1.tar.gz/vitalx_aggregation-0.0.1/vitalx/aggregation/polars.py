import polars
import polars._typing

from vitalx.aggregation.types import ActivityColumnT, SleepColumnT

DF_GROUP_KEY = "group_key"

SLEEP_DATAFRAME_SCHEMA: dict[SleepColumnT, polars._typing.PolarsDataType] = {
    # expectation: RFC 3339 timestamp string input
    "session_start": polars.String,
    # expectation: RFC 3339 timestamp string input
    "session_end": polars.String,
    "state": polars.Utf8,
    "duration_second": polars.Int64,
    "stage_asleep_second": polars.Int64,
    "stage_awake_second": polars.Int64,
    "stage_light_second": polars.Int64,
    "stage_rem_second": polars.Int64,
    "stage_deep_second": polars.Int64,
    "stage_unknown_second": polars.Int64,
    "latency_second": polars.Int64,
    "heart_rate_minimum": polars.Int64,
    "heart_rate_mean": polars.Int64,
    "heart_rate_maximum": polars.Int64,
    "heart_rate_dip": polars.Float64,
    "efficiency": polars.Float64,
    "hrv_mean_rmssd": polars.Float64,
    "hrv_mean_sdnn": polars.Float64,
    "skin_temperature_delta": polars.Float64,
    "respiratory_rate": polars.Float64,
    "score": polars.Int64,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}

ACTIVITY_DATAFRAME_SCHEMA: dict[ActivityColumnT, polars._typing.PolarsDataType] = {
    # expectation: RFC 3339 timestamp string input
    "date": polars.String,
    "calories_total": polars.Float64,
    "calories_active": polars.Float64,
    "steps": polars.Int64,
    "distance_meter": polars.Float64,
    "floors_climbed": polars.Int64,
    "duration_active_second": polars.Int64,
    "intensity_sedentary_second": polars.Int64,
    "intensity_low_second": polars.Int64,
    "intensity_medium_second": polars.Int64,
    "intensity_high_second": polars.Int64,
    "heart_rate_mean": polars.Float64,
    "heart_rate_min": polars.Float64,
    "heart_rate_max": polars.Float64,
    "heart_rate_resting": polars.Float64,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}
