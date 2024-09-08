from __future__ import annotations

import asyncio
import logging
import sys
import time
from asyncio import AbstractEventLoop
from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass
from enum import StrEnum, unique
from functools import partial, wraps
from inspect import iscoroutinefunction
from logging import Handler, LogRecord
from sys import __excepthook__, _getframe
from typing import (
    TYPE_CHECKING,
    Any,
    ParamSpec,
    TextIO,
    TypedDict,
    TypeVar,
    cast,
    overload,
)

from loguru import logger
from typing_extensions import override

from utilities.datetime import duration_to_timedelta
from utilities.functions import get_func_name
from utilities.iterables import (
    OneEmptyError,
    OneNonUniqueError,
    one,
    resolve_include_and_exclude,
)

if TYPE_CHECKING:
    import datetime as dt
    from multiprocessing.context import BaseContext
    from types import TracebackType

    from loguru import (
        CompressionFunction,
        FilterDict,
        FilterFunction,
        FormatFunction,
        LevelConfig,
        Message,
        Record,
        RetentionFunction,
        RotationFunction,
        Writable,
    )

    from utilities.asyncio import MaybeCoroutine1
    from utilities.iterables import MaybeIterable
    from utilities.types import Duration, PathLike, StrMapping


_P = ParamSpec("_P")
_T = TypeVar("_T")


_RECORD_EXCEPTION_VALUE = "{record[exception].value!r}"
LEVEL_CONFIGS: Sequence[LevelConfig] = [
    {"name": "TRACE", "color": "<white><bold>"},
    {"name": "DEBUG", "color": "<cyan><bold>"},
    {"name": "INFO", "color": "<green><bold>"},
    {"name": "SUCCESS", "color": "<magenta><bold>"},
    {"name": "WARNING", "color": "<yellow><bold>"},
    {"name": "ERROR", "color": "<red><bold>"},
    {"name": "CRITICAL", "color": "<red><bold><blink>"},
]


class HandlerConfiguration(TypedDict, total=False):
    """A handler configuration."""

    sink: (
        TextIO
        | Writable
        | Callable[[Message], MaybeCoroutine1[None]]
        | Handler
        | PathLike
    )
    level: int | str
    format: str | FormatFunction
    filter: str | FilterFunction | FilterDict | None
    colorize: bool | None
    serialize: bool
    backtrace: bool
    diagnose: bool
    enqueue: bool
    context: str | BaseContext | None
    catch: bool
    loop: AbstractEventLoop
    rotation: str | int | dt.time | dt.timedelta | RotationFunction | None
    retention: str | int | dt.timedelta | RetentionFunction | None
    compression: str | CompressionFunction | None
    delay: bool
    watch: bool
    mode: str
    buffering: int
    encoding: str
    kwargs: StrMapping


class InterceptHandler(Handler):
    """Handler for intercepting standard logging messages.

    https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    @override
    def emit(self, record: LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:  # pragma: no cover
            level = logger.level(record.levelname).name
        except ValueError:  # pragma: no cover
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = _getframe(6), 6  # pragma: no cover
        while (  # pragma: no cover
            frame and frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(  # pragma: no cover
            level, record.getMessage()
        )


@unique
class LogLevel(StrEnum):
    """An enumeration of the logging levels."""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def get_logging_level_name(level: int, /) -> str:
    """Get the logging level name."""
    core = logger._core  # noqa: SLF001 # pyright: ignore[reportAttributeAccessIssue]
    try:
        return one(k for k, v in core.levels.items() if v.no == level)
    except OneEmptyError:
        raise _GetLoggingLevelNameEmptyError(level=level) from None
    except OneNonUniqueError as error:
        error = cast(OneNonUniqueError[str], error)
        raise _GetLoggingLevelNameNonUniqueError(
            level=level, first=error.first, second=error.second
        ) from None


@dataclass(kw_only=True)
class GetLoggingLevelNameError(Exception):
    level: int


@dataclass(kw_only=True)
class _GetLoggingLevelNameEmptyError(GetLoggingLevelNameError):
    @override
    def __str__(self) -> str:
        return f"There is no level with severity {self.level}"


@dataclass(kw_only=True)
class _GetLoggingLevelNameNonUniqueError(GetLoggingLevelNameError):
    first: str
    second: str

    @override
    def __str__(self) -> str:
        return f"There must be exactly one level with severity {self.level}; got {self.first!r}, {self.second!r} and perhaps more"


def get_logging_level_number(level: str, /) -> int:
    """Get the logging level number."""
    try:
        return logger.level(level).no
    except ValueError:
        raise GetLoggingLevelNumberError(level=level) from None


@dataclass(kw_only=True)
class GetLoggingLevelNumberError(Exception):
    level: str

    @override
    def __str__(self) -> str:
        return f"Invalid logging level: {self.level!r}"


_MATHEMATICAL_ITALIC_SMALL_F = "𝑓"  # noqa: RUF001


@overload
def log(
    func: Callable[_P, _T],
    /,
    *,
    depth: int = 1,
    entry: LogLevel | None = ...,
    entry_bind: StrMapping | None = ...,
    entry_message: str = ...,
    error_expected: type[Exception] | tuple[type[Exception], ...] | None = ...,
    error_bind: StrMapping | None = ...,
    error_message: str = ...,
    exit_: LogLevel | None = ...,
    exit_predicate: Callable[[_T], bool] | None = ...,
    exit_bind: StrMapping | None = ...,
    exit_message: str = ...,
) -> Callable[_P, _T]: ...
@overload
def log(
    func: None = None,
    /,
    *,
    depth: int = 1,
    entry: LogLevel | None = ...,
    entry_bind: StrMapping | None = ...,
    entry_message: str = ...,
    error_bind: StrMapping | None = ...,
    error_expected: type[Exception] | tuple[type[Exception], ...] | None = ...,
    error_message: str = ...,
    exit_: LogLevel | None = ...,
    exit_predicate: Callable[[Any], bool] | None = ...,
    exit_bind: StrMapping | None = ...,
    exit_message: str = ...,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...
def log(
    func: Callable[_P, _T] | None = None,
    /,
    *,
    depth: int = 1,
    entry: LogLevel | None = LogLevel.TRACE,
    entry_bind: StrMapping | None = None,
    entry_message: str = "⋯",
    error_expected: type[Exception] | tuple[type[Exception], ...] | None = None,
    error_bind: StrMapping | None = None,
    error_message: str = _RECORD_EXCEPTION_VALUE,
    exit_: LogLevel | None = None,
    exit_bind: StrMapping | None = None,
    exit_predicate: Callable[[_T], bool] | None = None,
    exit_message: str = "✔",
) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Log the function call."""
    if func is None:
        return partial(
            log,
            depth=depth,
            entry=entry,
            entry_bind=entry_bind,
            entry_message=entry_message,
            error_expected=error_expected,
            error_bind=error_bind,
            error_message=error_message,
            exit_=exit_,
            exit_bind=exit_bind,
            exit_predicate=exit_predicate,
            exit_message=exit_message,
        )

    func_name = get_func_name(func)
    if iscoroutinefunction(func):

        @wraps(func)
        async def wrapped_async(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            if entry is not None:
                logger_use = logger if entry_bind is None else logger.bind(**entry_bind)
                logger_use.opt(depth=depth).log(
                    entry, entry_message, **{_MATHEMATICAL_ITALIC_SMALL_F: func_name}
                )
            try:
                result = await func(*args, **kwargs)
            except Exception as error:
                if (error_expected is None) or not isinstance(error, error_expected):
                    logger_use = (
                        logger if error_bind is None else logger.bind(**error_bind)
                    )
                    logger_use.opt(exception=True, record=True, depth=depth).error(
                        error_message
                    )
                raise
            if ((exit_predicate is None) or (exit_predicate(result))) and (
                exit_ is not None
            ):
                logger_use = logger if exit_bind is None else logger.bind(**exit_bind)
                logger_use.opt(depth=depth).log(exit_, exit_message)
            return result

        return cast(Callable[_P, _T], wrapped_async)

    @wraps(func)
    def wrapped_sync(*args: Any, **kwargs: Any) -> Any:
        if entry is not None:
            logger_use = logger if entry_bind is None else logger.bind(**entry_bind)
            logger_use.opt(depth=depth).log(
                entry, entry_message, **{_MATHEMATICAL_ITALIC_SMALL_F: func_name}
            )
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            if (error_expected is None) or not isinstance(error, error_expected):
                logger_use = logger if error_bind is None else logger.bind(**error_bind)
                logger_use.opt(exception=True, record=True, depth=depth).error(
                    error_message
                )
            raise
        if ((exit_predicate is None) or (exit_predicate(result))) and (
            exit_ is not None
        ):
            logger_use = logger if exit_bind is None else logger.bind(**exit_bind)
            logger_use.opt(depth=depth).log(exit_, exit_message)
        return result

    return cast(Callable[_P, _T], wrapped_sync)


def logged_sleep_sync(
    duration: Duration, /, *, level: LogLevel = LogLevel.INFO, depth: int = 1
) -> None:
    """Log a sleep operation, synchronously."""
    timedelta = duration_to_timedelta(duration)
    logger.opt(depth=depth).log(
        level, "Sleeping for {timedelta}...", timedelta=timedelta
    )
    time.sleep(timedelta.total_seconds())


async def logged_sleep_async(
    duration: Duration, /, *, level: LogLevel = LogLevel.INFO, depth: int = 1
) -> None:
    """Log a sleep operation, asynchronously."""
    timedelta = duration_to_timedelta(duration)
    logger.opt(depth=depth).log(
        level, "Sleeping for {timedelta}...", timedelta=timedelta
    )
    await asyncio.sleep(timedelta.total_seconds())


def make_except_hook(
    **kwargs: Any,
) -> Callable[[type[BaseException], BaseException, TracebackType | None], None]:
    """Make an `excepthook` which uses `loguru`."""

    def except_hook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
        /,
    ) -> None:
        """Exception hook which uses `loguru`."""
        if issubclass(exc_type, KeyboardInterrupt):  # pragma: no cover
            __excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.bind(**kwargs).opt(  # pragma: no cover
            exception=exc_value, record=True
        ).error(_RECORD_EXCEPTION_VALUE)
        sys.exit(1)  # pragma: no cover

    return except_hook


def make_filter(
    *,
    level: LogLevel | None = None,
    min_level: LogLevel | None = None,
    max_level: LogLevel | None = None,
    name_include: MaybeIterable[str] | None = None,
    name_exclude: MaybeIterable[str] | None = None,
    extra_include_all: MaybeIterable[Hashable] | None = None,
    extra_include_any: MaybeIterable[Hashable] | None = None,
    extra_exclude_all: MaybeIterable[Hashable] | None = None,
    extra_exclude_any: MaybeIterable[Hashable] | None = None,
    final_filter: bool | Callable[[], bool] | None = None,
) -> FilterFunction:
    """Make a filter."""

    def filter_func(record: Record, /) -> bool:
        rec_level_no = record["level"].no
        if (level is not None) and (rec_level_no != get_logging_level_number(level)):
            return False
        if (min_level is not None) and (
            rec_level_no < get_logging_level_number(min_level)
        ):
            return False
        if (max_level is not None) and (
            rec_level_no > get_logging_level_number(max_level)
        ):
            return False
        name = record["name"]
        if name is not None:
            name_inc, name_exc = resolve_include_and_exclude(
                include=name_include, exclude=name_exclude
            )
            if (name_inc is not None) and not any(name.startswith(n) for n in name_inc):
                return False
            if (name_exc is not None) and any(name.startswith(n) for n in name_exc):
                return False
        rec_extra_keys = set(record["extra"])
        extra_inc_all, extra_exc_any = resolve_include_and_exclude(
            include=extra_include_all, exclude=extra_exclude_any
        )
        if (extra_inc_all is not None) and not extra_inc_all.issubset(rec_extra_keys):
            return False
        if (extra_exc_any is not None) and (len(rec_extra_keys & extra_exc_any) >= 1):
            return False
        extra_inc_any, extra_exc_all = resolve_include_and_exclude(
            include=extra_include_any, exclude=extra_exclude_all
        )
        if (extra_inc_any is not None) and (len(rec_extra_keys & extra_inc_any) == 0):
            return False
        if (extra_exc_all is not None) and extra_exc_all.issubset(rec_extra_keys):
            return False
        return (final_filter is None) or (
            (isinstance(final_filter, bool) and final_filter)
            or (isinstance(final_filter, Callable) and final_filter())
        )

    return filter_func


__all__ = [
    "LEVEL_CONFIGS",
    "GetLoggingLevelNameError",
    "GetLoggingLevelNumberError",
    "HandlerConfiguration",
    "InterceptHandler",
    "LogLevel",
    "get_logging_level_name",
    "get_logging_level_number",
    "log",
    "logged_sleep_async",
    "logged_sleep_sync",
    "make_except_hook",
    "make_filter",
]
