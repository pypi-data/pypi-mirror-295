from __future__ import annotations

import datetime as dt
from datetime import timezone
from re import escape
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from hypothesis import assume, given
from hypothesis.strategies import (
    DataObject,
    data,
    dates,
    datetimes,
    integers,
    sampled_from,
    timedeltas,
    times,
)
from pytest import mark, param, raises
from whenever import DateTimeDelta

from tests.conftest import SKIPIF_CI_AND_WINDOWS
from utilities.datetime import (
    _MICROSECONDS_PER_DAY,
    _MICROSECONDS_PER_SECOND,
    drop_milli_and_microseconds,
    maybe_sub_pct_y,
)
from utilities.hypothesis import (
    assume_does_not_raise,
    durations,
    timedeltas_2w,
    zoned_datetimes,
)
from utilities.whenever import (
    MAX_SERIALIZABLE_TIMEDELTA,
    MAX_TWO_WAY_TIMEDELTA,
    MIN_SERIALIZABLE_TIMEDELTA,
    MIN_TWO_WAY_TIMEDELTA,
    CheckValidZonedDateimeError,
    EnsureDateError,
    EnsureDurationError,
    EnsureLocalDateTimeError,
    EnsureTimedeltaError,
    EnsureTimeError,
    EnsureZonedDateTimeError,
    ParseDateError,
    ParseDurationError,
    ParseLocalDateTimeError,
    ParseTimedeltaError,
    ParseTimeError,
    ParseZonedDateTimeError,
    SerializeDurationError,
    SerializeLocalDateTimeError,
    SerializeTimeDeltaError,
    SerializeZonedDateTimeError,
    _to_datetime_delta,
    _ToDateTimeDeltaError,
    check_valid_zoned_datetime,
    ensure_date,
    ensure_duration,
    ensure_local_datetime,
    ensure_time,
    ensure_timedelta,
    ensure_zoned_datetime,
    parse_date,
    parse_duration,
    parse_local_datetime,
    parse_time,
    parse_timedelta,
    parse_zoned_datetime,
    serialize_date,
    serialize_duration,
    serialize_local_datetime,
    serialize_time,
    serialize_timedelta,
    serialize_zoned_datetime,
)
from utilities.zoneinfo import HONG_KONG, UTC, get_time_zone_name

if TYPE_CHECKING:
    from utilities.types import Duration

_TIMEDELTA_MICROSECONDS = dt.timedelta(microseconds=1e18)
_TIMEDELTA_OVERFLOW = dt.timedelta(days=106751991, seconds=14454, microseconds=775808)


@SKIPIF_CI_AND_WINDOWS
class TestCheckValidZonedDatetime:
    @mark.parametrize(
        "datetime",
        [
            param(dt.datetime(1951, 4, 1, 3, tzinfo=HONG_KONG)),
            param(dt.datetime(1951, 4, 1, 5, tzinfo=HONG_KONG)),
        ],
    )
    def test_main(self, *, datetime: dt.datetime) -> None:
        check_valid_zoned_datetime(datetime)

    def test_error(self) -> None:
        datetime = dt.datetime(1951, 4, 1, 4, tzinfo=HONG_KONG)
        with raises(
            CheckValidZonedDateimeError,
            match=escape(
                "Zoned datetime must be valid; got 1951-04-01 04:00:00+08:00 != 1951-04-01 05:00:00+09:00"
            ),
        ):
            check_valid_zoned_datetime(datetime)


class TestParseAndSerializeDate:
    @given(date=dates())
    def test_main(self, *, date: dt.date) -> None:
        serialized = serialize_date(date)
        result = parse_date(serialized)
        assert result == date

    @given(date=dates())
    def test_yyyymmdd(self, *, date: dt.date) -> None:
        serialized = date.strftime(maybe_sub_pct_y("%Y%m%d"))
        result = parse_date(serialized)
        assert result == date

    def test_error_parse(self) -> None:
        with raises(ParseDateError, match="Unable to parse date; got 'invalid'"):
            _ = parse_date("invalid")

    @given(data=data(), date=dates())
    def test_ensure(self, *, data: DataObject, date: dt.date) -> None:
        str_or_value = data.draw(sampled_from([date, serialize_date(date)]))
        result = ensure_date(str_or_value)
        assert result == date

    def test_error_ensure(self) -> None:
        with raises(EnsureDateError, match="Unable to ensure date; got 'invalid'"):
            _ = ensure_date("invalid")


class TestParseAndSerializeDuration:
    @given(duration=durations())
    def test_main(self, *, duration: Duration) -> None:
        with assume_does_not_raise(SerializeDurationError):
            serialized = serialize_duration(duration)
        with assume_does_not_raise(ParseDurationError):
            result = parse_duration(serialized)
        assert result == duration

    def test_error_parse(self) -> None:
        with raises(
            ParseDurationError, match="Unable to parse duration; got 'invalid'"
        ):
            _ = parse_duration("invalid")

    @mark.parametrize(
        "duration", [param(_TIMEDELTA_MICROSECONDS), param(_TIMEDELTA_OVERFLOW)]
    )
    def test_error_serialize(self, *, duration: Duration) -> None:
        with raises(
            SerializeDurationError, match="Unable to serialize duration; got .*"
        ):
            _ = serialize_duration(duration)

    @given(data=data(), duration=durations(two_way=True))
    def test_ensure(self, *, data: DataObject, duration: Duration) -> None:
        str_or_value = data.draw(sampled_from([duration, serialize_duration(duration)]))
        result = ensure_duration(str_or_value)
        assert result == duration

    def test_error_ensure(self) -> None:
        with raises(
            EnsureDurationError, match="Unable to ensure duration; got 'invalid'"
        ):
            _ = ensure_duration("invalid")


class TestParseAndSerializeLocalDateTime:
    @given(datetime=datetimes())
    def test_main(self, *, datetime: dt.datetime) -> None:
        serialized = serialize_local_datetime(datetime)
        result = parse_local_datetime(serialized)
        assert result == datetime

    @given(datetime=datetimes().map(drop_milli_and_microseconds))
    def test_yyyymmdd_hhmmss(self, *, datetime: dt.datetime) -> None:
        serialized = datetime.strftime(maybe_sub_pct_y("%Y%m%dT%H%M%S"))
        result = parse_local_datetime(serialized)
        assert result == datetime

    @given(datetime=datetimes())
    def test_yyyymmdd_hhmmss_ffffff(self, *, datetime: dt.datetime) -> None:
        _ = assume(datetime.microsecond != 0)
        serialized = datetime.strftime(maybe_sub_pct_y("%Y%m%dT%H%M%S.%f"))
        result = parse_local_datetime(serialized)
        assert result == datetime

    def test_error_parse(self) -> None:
        with raises(
            ParseLocalDateTimeError,
            match="Unable to parse local datetime; got 'invalid'",
        ):
            _ = parse_local_datetime("invalid")

    def test_error_serialize(self) -> None:
        datetime = dt.datetime(2000, 1, 1, tzinfo=UTC)
        with raises(
            SerializeLocalDateTimeError,
            match="Unable to serialize local datetime; got .*",
        ):
            _ = serialize_local_datetime(datetime)

    @given(data=data(), datetime=datetimes())
    def test_ensure(self, *, data: DataObject, datetime: dt.datetime) -> None:
        str_or_value = data.draw(
            sampled_from([datetime, serialize_local_datetime(datetime)])
        )
        result = ensure_local_datetime(str_or_value)
        assert result == datetime

    def test_error_ensure(self) -> None:
        with raises(
            EnsureLocalDateTimeError,
            match="Unable to ensure local datetime; got 'invalid'",
        ):
            _ = ensure_local_datetime("invalid")


class TestParseAndSerializeTime:
    @given(time=times())
    def test_main(self, *, time: dt.time) -> None:
        serialized = serialize_time(time)
        result = parse_time(serialized)
        assert result == time

    def test_error_parse(self) -> None:
        with raises(ParseTimeError, match="Unable to parse time; got 'invalid'"):
            _ = parse_time("invalid")

    @given(data=data(), time=times())
    def test_ensure(self, *, data: DataObject, time: dt.time) -> None:
        str_or_value = data.draw(sampled_from([time, serialize_time(time)]))
        result = ensure_time(str_or_value)
        assert result == time

    def test_error_ensure(self) -> None:
        with raises(EnsureTimeError, match="Unable to ensure time; got 'invalid'"):
            _ = ensure_time("invalid")


class TestParseAndSerializeTimedelta:
    @given(timedelta=timedeltas())
    def test_main(self, *, timedelta: dt.timedelta) -> None:
        with assume_does_not_raise(SerializeTimeDeltaError):
            serialized = serialize_timedelta(timedelta)
        with assume_does_not_raise(ParseTimedeltaError):
            result = parse_timedelta(serialized)
        assert result == timedelta

    @given(timedelta=timedeltas(min_value=dt.timedelta(microseconds=1)))
    def test_min_serializable(self, *, timedelta: dt.timedelta) -> None:
        _ = serialize_timedelta(MIN_SERIALIZABLE_TIMEDELTA)
        with assume_does_not_raise(OverflowError):
            offset = MIN_SERIALIZABLE_TIMEDELTA - timedelta
        with raises(SerializeTimeDeltaError):
            _ = serialize_timedelta(offset)

    @given(timedelta=timedeltas(min_value=dt.timedelta(microseconds=1)))
    def test_max_serializable(self, *, timedelta: dt.timedelta) -> None:
        _ = serialize_timedelta(MAX_SERIALIZABLE_TIMEDELTA)
        with assume_does_not_raise(OverflowError):
            offset = MAX_SERIALIZABLE_TIMEDELTA + timedelta
        with raises(SerializeTimeDeltaError):
            _ = serialize_timedelta(offset)

    @given(timedelta=timedeltas(min_value=dt.timedelta(microseconds=1)))
    def test_min_two_way(self, *, timedelta: dt.timedelta) -> None:
        ser = serialize_timedelta(MIN_TWO_WAY_TIMEDELTA)
        _ = parse_timedelta(ser)
        with assume_does_not_raise(OverflowError):
            offset = MIN_TWO_WAY_TIMEDELTA - timedelta
        with assume_does_not_raise(SerializeTimeDeltaError):
            ser2 = serialize_timedelta(offset)
        with raises(ParseTimedeltaError):
            _ = parse_timedelta(ser2)

    @given(timedelta=timedeltas(min_value=dt.timedelta(microseconds=1)))
    def test_max_two_way(self, *, timedelta: dt.timedelta) -> None:
        ser = serialize_timedelta(MAX_TWO_WAY_TIMEDELTA)
        _ = parse_timedelta(ser)
        with assume_does_not_raise(OverflowError):
            offset = MAX_TWO_WAY_TIMEDELTA + timedelta
        with assume_does_not_raise(SerializeTimeDeltaError):
            ser2 = serialize_timedelta(offset)
        with raises(ParseTimedeltaError):
            _ = parse_timedelta(ser2)

    def test_error_parse(self) -> None:
        with raises(
            ParseTimedeltaError, match="Unable to parse timedelta; got 'invalid'"
        ):
            _ = parse_timedelta("invalid")

    def test_error_parse_nano_seconds(self) -> None:
        with raises(
            ParseTimedeltaError, match="Unable to parse timedelta; got 333 nanoseconds"
        ):
            _ = parse_timedelta("PT0.111222333S")

    @mark.parametrize(
        "timedelta", [param(_TIMEDELTA_MICROSECONDS), param(_TIMEDELTA_OVERFLOW)]
    )
    def test_error_serialize(self, *, timedelta: dt.timedelta) -> None:
        with raises(
            SerializeTimeDeltaError, match="Unable to serialize timedelta; got .*"
        ):
            _ = serialize_timedelta(timedelta)

    @given(data=data(), timedelta=timedeltas_2w())
    def test_ensure(self, *, data: DataObject, timedelta: dt.timedelta) -> None:
        str_or_value = data.draw(
            sampled_from([timedelta, serialize_timedelta(timedelta)])
        )
        result = ensure_timedelta(str_or_value)
        assert result == timedelta

    def test_error_ensure(self) -> None:
        with raises(
            EnsureTimedeltaError, match="Unable to ensure timedelta; got 'invalid'"
        ):
            _ = ensure_timedelta("invalid")

    def test_error_ensure_nano_seconds(self) -> None:
        with raises(
            EnsureTimedeltaError,
            match="Unable to ensure timedelta; got 333 nanoseconds",
        ):
            _ = ensure_timedelta("PT0.111222333S")


class TestParseAndSerializeZonedDateTime:
    @given(
        datetime=zoned_datetimes(
            time_zone=sampled_from([HONG_KONG, UTC, dt.UTC]), valid=True
        )
    )
    @SKIPIF_CI_AND_WINDOWS
    def test_main(self, *, datetime: dt.datetime) -> None:
        serialized = serialize_zoned_datetime(datetime)
        result = parse_zoned_datetime(serialized)
        assert result == datetime

    @given(
        datetime=zoned_datetimes(
            time_zone=sampled_from([HONG_KONG, UTC, dt.UTC]), valid=True
        ).map(drop_milli_and_microseconds)
    )
    @SKIPIF_CI_AND_WINDOWS
    def test_yyyymmdd_hhmmss(self, *, datetime: dt.datetime) -> None:
        part1 = datetime.strftime(maybe_sub_pct_y("%Y%m%dT%H%M%S"))
        assert isinstance(datetime.tzinfo, ZoneInfo | timezone)
        part2 = get_time_zone_name(datetime.tzinfo)
        serialized = f"{part1}[{part2}]"
        result = parse_zoned_datetime(serialized)
        assert result == datetime

    @given(
        datetime=zoned_datetimes(
            time_zone=sampled_from([HONG_KONG, UTC, dt.UTC]), valid=True
        )
    )
    @SKIPIF_CI_AND_WINDOWS
    def test_yyyymmdd_hhmmss_ffffff(self, *, datetime: dt.datetime) -> None:
        _ = assume(datetime.microsecond != 0)
        part1 = datetime.strftime(maybe_sub_pct_y("%Y%m%dT%H%M%S.%f"))
        assert isinstance(datetime.tzinfo, ZoneInfo | timezone)
        part2 = get_time_zone_name(datetime.tzinfo)
        serialized = f"{part1}[{part2}]"
        result = parse_zoned_datetime(serialized)
        assert result == datetime

    def test_error_parse(self) -> None:
        with raises(
            ParseZonedDateTimeError,
            match="Unable to parse zoned datetime; got 'invalid'",
        ):
            _ = parse_zoned_datetime("invalid")

    def test_error_serialize(self) -> None:
        datetime = dt.datetime(2000, 1, 1).astimezone(None)
        with raises(
            SerializeZonedDateTimeError,
            match="Unable to serialize zoned datetime; got 2000-01-01 00:00:00",
        ):
            _ = serialize_zoned_datetime(datetime)

    @given(
        data=data(),
        datetime=zoned_datetimes(
            time_zone=sampled_from([HONG_KONG, UTC, dt.UTC]), valid=True
        ),
    )
    @SKIPIF_CI_AND_WINDOWS
    def test_ensure(self, *, data: DataObject, datetime: dt.datetime) -> None:
        str_or_value = data.draw(
            sampled_from([datetime, serialize_zoned_datetime(datetime)])
        )
        result = ensure_zoned_datetime(str_or_value)
        assert result == datetime

    def test_error_ensure(self) -> None:
        with raises(
            EnsureZonedDateTimeError,
            match="Unable to ensure zoned datetime; got 'invalid'",
        ):
            _ = ensure_zoned_datetime("invalid")


class TestToDatetimeDelta:
    @given(days=integers(), microseconds=integers())
    def test_main(self, *, days: int, microseconds: int) -> None:
        with assume_does_not_raise(OverflowError):
            timedelta = dt.timedelta(days=days, microseconds=microseconds)
        init_total_micro = _MICROSECONDS_PER_DAY * days + microseconds
        with assume_does_not_raise(_ToDateTimeDeltaError):
            result = _to_datetime_delta(timedelta)
        comp_month, comp_day, comp_sec, comp_nano = result.in_months_days_secs_nanos()
        assert comp_month == 0
        comp_micro, remainder = divmod(comp_nano, 1000)
        assert remainder == 0
        result_total_micro = (
            _MICROSECONDS_PER_DAY * comp_day
            + _MICROSECONDS_PER_SECOND * comp_sec
            + comp_micro
        )
        assert init_total_micro == result_total_micro

    def test_mixed_sign(self) -> None:
        timedelta = dt.timedelta(days=-1, seconds=1)
        result = _to_datetime_delta(timedelta)
        expected = DateTimeDelta(seconds=timedelta.total_seconds())
        assert result == expected

    def test_close_to_overflow(self) -> None:
        timedelta = dt.timedelta(days=104250, microseconds=1)
        result = _to_datetime_delta(timedelta)
        expected = DateTimeDelta(days=104250, microseconds=1)
        assert result == expected

    @mark.parametrize(
        "timedelta", [param(_TIMEDELTA_MICROSECONDS), param(_TIMEDELTA_OVERFLOW)]
    )
    def test_error(self, *, timedelta: dt.timedelta) -> None:
        with raises(
            _ToDateTimeDeltaError, match="Unable to create DateTimeDelta; got .*"
        ):
            _ = _to_datetime_delta(timedelta)
