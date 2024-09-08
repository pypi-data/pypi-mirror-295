from __future__ import annotations

import builtins
import datetime as dt
from collections.abc import (
    AsyncIterator,
    Callable,
    Collection,
    Hashable,
    Iterable,
    Iterator,
)
from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
    asynccontextmanager,
    contextmanager,
    suppress,
)
from dataclasses import dataclass
from datetime import timezone
from enum import Enum, auto
from math import ceil, floor, inf, isfinite, nan
from os import environ
from pathlib import Path
from re import search
from string import ascii_letters, printable
from subprocess import run
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeVar,
    assert_never,
    cast,
    overload,
)
from zoneinfo import ZoneInfo

import redis
import redis.asyncio
from hypothesis import HealthCheck, Phase, Verbosity, assume, settings
from hypothesis.errors import InvalidArgument
from hypothesis.strategies import (
    DataObject,
    DrawFn,
    SearchStrategy,
    booleans,
    characters,
    composite,
    dates,
    datetimes,
    floats,
    integers,
    just,
    lists,
    none,
    sampled_from,
    text,
    timedeltas,
    uuids,
)
from hypothesis.utils.conventions import not_set
from redis.exceptions import ResponseError
from redis.typing import KeyT

from utilities.datetime import MAX_MONTH, MIN_MONTH, Month, date_to_month, get_now
from utilities.math import MAX_INT32, MAX_INT64, MAX_UINT32, MIN_INT32, MIN_INT64
from utilities.pathlib import temp_cwd
from utilities.platform import IS_WINDOWS
from utilities.tempfile import TEMP_DIR, TemporaryDirectory
from utilities.text import ensure_str
from utilities.whenever import CheckValidZonedDateimeError, check_valid_zoned_datetime
from utilities.zoneinfo import UTC

if TYPE_CHECKING:
    from uuid import UUID

    from hypothesis.database import ExampleDatabase
    from numpy.random import RandomState
    from redis.commands.timeseries import TimeSeries
    from sqlalchemy import Engine, MetaData
    from sqlalchemy.ext.asyncio import AsyncEngine

    from utilities.numpy import NDArrayB, NDArrayF, NDArrayI, NDArrayO
    from utilities.types import Duration, Number


_T = TypeVar("_T")
MaybeSearchStrategy = _T | SearchStrategy[_T]
Shape = int | tuple[int, ...]


async def aiosqlite_engines(
    data: DataObject, /, *, metadata: MetaData | None = None, base: Any = None
) -> AsyncEngine:
    from utilities.sqlalchemy import create_engine

    temp_path = data.draw(temp_paths())
    path = Path(temp_path, "db.sqlite")
    engine = create_engine("sqlite+aiosqlite", database=str(path), async_=True)
    if metadata is not None:
        async with engine.begin() as conn:  # pragma: no cover
            await conn.run_sync(metadata.create_all)
    if base is not None:
        async with engine.begin() as conn:  # pragma: no cover
            await conn.run_sync(base.metadata.create_all)

    class EngineWithPath(type(engine)): ...

    engine_with_path = EngineWithPath(engine.sync_engine)
    cast(Any, engine_with_path).temp_path = temp_path  # keep `temp_path` alive
    return engine_with_path


@contextmanager
def assume_does_not_raise(
    *exceptions: type[Exception], match: str | None = None
) -> Iterator[None]:
    """Assume a set of exceptions are not raised.

    Optionally filter on the string representation of the exception.
    """
    try:
        yield
    except exceptions as caught:
        if match is None:
            _ = assume(condition=False)
        else:
            (msg,) = caught.args
            if search(match, ensure_str(msg)):
                _ = assume(condition=False)
            else:
                raise


@composite
def bool_arrays(
    _draw: DrawFn,
    /,
    *,
    shape: MaybeSearchStrategy[Shape] | None = None,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
) -> NDArrayB:
    """Strategy for generating arrays of booleans."""
    from hypothesis.extra.numpy import array_shapes, arrays

    draw = lift_draw(_draw)
    shape_use = array_shapes() if shape is None else shape
    strategy: SearchStrategy[NDArrayB] = arrays(
        bool, draw(shape_use), elements=booleans(), fill=fill, unique=draw(unique)
    )
    return draw(strategy)


@composite
def durations(
    _draw: DrawFn,
    /,
    *,
    min_number: MaybeSearchStrategy[Number] | None = None,
    max_number: MaybeSearchStrategy[Number] | None = None,
    min_timedelta: MaybeSearchStrategy[dt.timedelta] = dt.timedelta.min,
    max_timedelta: MaybeSearchStrategy[dt.timedelta] = dt.timedelta.max,
    two_way: bool = False,
) -> Duration:
    """Strategy for generating durations."""
    draw = lift_draw(_draw)
    min_number_, max_number_ = draw(min_number), draw(max_number)
    min_timedelta_, max_timedelta_ = draw(min_timedelta), draw(max_timedelta)
    st_integers = integers(
        min_value=min_number_ if isinstance(min_number_, int) else None,
        max_value=max_number_ if isinstance(max_number_, int) else None,
    )
    st_floats = floats(
        min_value=min_number_,
        max_value=max_number_,
        allow_nan=False,
        allow_infinity=False,
    )
    if two_way:
        from utilities.whenever import MAX_TWO_WAY_TIMEDELTA, MIN_TWO_WAY_TIMEDELTA

        min_timedelta_ = max(min_timedelta_, MIN_TWO_WAY_TIMEDELTA)
        max_timedelta_ = min(max_timedelta_, MAX_TWO_WAY_TIMEDELTA)
    st_timedeltas = timedeltas(min_value=min_timedelta_, max_value=max_timedelta_)
    return _draw(st_integers | st_floats | st_timedeltas)


@composite
def float_arrays(
    _draw: DrawFn,
    /,
    *,
    shape: MaybeSearchStrategy[Shape] | None = None,
    min_value: MaybeSearchStrategy[float | None] = None,
    max_value: MaybeSearchStrategy[float | None] = None,
    allow_nan: MaybeSearchStrategy[bool] = False,
    allow_inf: MaybeSearchStrategy[bool] = False,
    allow_pos_inf: MaybeSearchStrategy[bool] = False,
    allow_neg_inf: MaybeSearchStrategy[bool] = False,
    integral: MaybeSearchStrategy[bool] = False,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
) -> NDArrayF:
    """Strategy for generating arrays of floats."""
    from hypothesis.extra.numpy import array_shapes, arrays

    draw = lift_draw(_draw)
    shape_use = array_shapes() if shape is None else shape
    elements = floats_extra(
        min_value=min_value,
        max_value=max_value,
        allow_nan=allow_nan,
        allow_inf=allow_inf,
        allow_pos_inf=allow_pos_inf,
        allow_neg_inf=allow_neg_inf,
        integral=integral,
    )
    strategy: SearchStrategy[NDArrayF] = arrays(
        float, draw(shape_use), elements=elements, fill=fill, unique=draw(unique)
    )
    return draw(strategy)


@composite
def floats_extra(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[float | None] = None,
    max_value: MaybeSearchStrategy[float | None] = None,
    allow_nan: MaybeSearchStrategy[bool] = False,
    allow_inf: MaybeSearchStrategy[bool] = False,
    allow_pos_inf: MaybeSearchStrategy[bool] = False,
    allow_neg_inf: MaybeSearchStrategy[bool] = False,
    integral: MaybeSearchStrategy[bool] = False,
) -> float:
    """Strategy for generating floats, with extra special values."""
    draw = lift_draw(_draw)
    min_value_, max_value_ = draw(min_value), draw(max_value)
    elements = floats(
        min_value=min_value_,
        max_value=max_value_,
        allow_nan=False,
        allow_infinity=False,
    )
    if draw(allow_nan):
        elements |= just(nan)
    if draw(allow_inf):
        elements |= sampled_from([inf, -inf])
    if draw(allow_pos_inf):
        elements |= just(inf)
    if draw(allow_neg_inf):
        elements |= just(-inf)
    element = draw(elements)
    if isfinite(element) and draw(integral):
        candidates = [floor(element), ceil(element)]
        if min_value_ is not None:
            candidates = [c for c in candidates if c >= min_value_]
        if max_value_ is not None:
            candidates = [c for c in candidates if c <= max_value_]
        _ = assume(len(candidates) >= 1)
        element = draw(sampled_from(candidates))
        return float(element)
    return element


@composite
def git_repos(
    _draw: DrawFn, /, *, branch: MaybeSearchStrategy[str | None] = None
) -> Path:
    draw = lift_draw(_draw)
    path = draw(temp_paths())
    with temp_cwd(path):
        _ = run(["git", "init"], check=True)
        _ = run(["git", "config", "user.name", "User"], check=True)
        _ = run(["git", "config", "user.email", "a@z.com"], check=True)
        file = Path(path, "file")
        file.touch()
        file_str = str(file)
        _ = run(["git", "add", file_str], check=True)
        _ = run(["git", "commit", "-m", "add"], check=True)
        _ = run(["git", "rm", file_str], check=True)
        _ = run(["git", "commit", "-m", "rm"], check=True)
        if (branch := draw(branch)) is not None:
            _ = run(["git", "checkout", "-b", branch], check=True)
    return path


def hashables() -> SearchStrategy[Hashable]:
    """Strategy for generating hashable elements."""
    return booleans() | integers() | none() | text_ascii()


@composite
def int_arrays(
    _draw: DrawFn,
    /,
    *,
    shape: MaybeSearchStrategy[Shape] | None = None,
    min_value: MaybeSearchStrategy[int] = MIN_INT64,
    max_value: MaybeSearchStrategy[int] = MAX_INT64,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
) -> NDArrayI:
    """Strategy for generating arrays of ints."""
    from hypothesis.extra.numpy import array_shapes, arrays
    from numpy import int64

    draw = lift_draw(_draw)
    shape_use = array_shapes() if shape is None else shape
    elements = int64s(min_value=min_value, max_value=max_value)
    strategy: SearchStrategy[NDArrayI] = arrays(
        int64, draw(shape_use), elements=elements, fill=fill, unique=draw(unique)
    )
    return draw(strategy)


@composite
def int32s(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[int] = MIN_INT32,
    max_value: MaybeSearchStrategy[int] = MAX_INT32,
) -> int:
    """Strategy for generating int32s."""
    draw = lift_draw(_draw)
    min_value_, max_value_ = draw(min_value), draw(max_value)
    min_value_ = max(min_value_, MIN_INT32)
    max_value_ = min(max_value_, MAX_INT32)
    return draw(integers(min_value_, max_value_))


@composite
def int64s(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[int] = MIN_INT64,
    max_value: MaybeSearchStrategy[int] = MAX_INT64,
) -> int:
    """Strategy for generating int64s."""
    draw = lift_draw(_draw)
    min_value_, max_value_ = draw(min_value), draw(max_value)
    min_value_ = max(min_value_, MIN_INT64)
    max_value_ = min(max_value_, MAX_INT64)
    return draw(integers(min_value_, max_value_))


_MDF = TypeVar("_MDF")


class _MaybeDrawFn(Protocol):
    @overload
    def __call__(self, obj: SearchStrategy[_MDF], /) -> _MDF: ...
    @overload
    def __call__(self, obj: MaybeSearchStrategy[_MDF], /) -> _MDF: ...
    def __call__(self, obj: MaybeSearchStrategy[_MDF], /) -> _MDF:
        raise NotImplementedError(obj)  # pragma: no cover


def lift_draw(draw: DrawFn, /) -> _MaybeDrawFn:
    """Lift the `draw` function to handle non-`SearchStrategy` types."""

    def func(obj: MaybeSearchStrategy[_MDF], /) -> _MDF:
        return draw(obj) if isinstance(obj, SearchStrategy) else obj

    return cast(Any, func)


@composite
def lists_fixed_length(
    _draw: DrawFn,
    strategy: SearchStrategy[_T],
    size: MaybeSearchStrategy[int],
    /,
    *,
    unique: MaybeSearchStrategy[bool] = False,
    sorted: MaybeSearchStrategy[bool] = False,  # noqa: A002
) -> list[_T]:
    """Strategy for generating lists of a fixed length."""
    draw = lift_draw(_draw)
    size_ = draw(size)
    elements = draw(
        lists(strategy, min_size=size_, max_size=size_, unique=draw(unique))
    )
    if draw(sorted):
        return builtins.sorted(cast(Iterable[Any], elements))
    return elements


@composite
def months(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[Month] = MIN_MONTH,
    max_value: MaybeSearchStrategy[Month] = MAX_MONTH,
) -> Month:
    """Strategy for generating datetimes with the UTC timezone."""
    draw = lift_draw(_draw)
    min_date = draw(min_value).to_date()
    max_date = draw(max_value).to_date()
    date = draw(dates(min_value=min_date, max_value=max_date))
    return date_to_month(date)


@composite
def random_states(
    _draw: DrawFn, /, *, seed: MaybeSearchStrategy[int | None] = None
) -> RandomState:
    """Strategy for generating `numpy` random states."""
    from numpy.random import RandomState

    draw = lift_draw(_draw)
    seed_ = draw(seed)
    seed_use = draw(integers(0, MAX_UINT32)) if seed_ is None else seed_
    return RandomState(seed=seed_use)


_TRedis = TypeVar("_TRedis", redis.Redis, redis.asyncio.Redis)


@dataclass(repr=False, frozen=True, kw_only=True)
class RedisContainer(Generic[_TRedis]):
    """A container for `redis.Client`."""

    client: _TRedis
    timestamp: dt.datetime
    uuid: UUID
    key: str

    @property
    def ts(self) -> TimeSeries:
        return self.client.ts()  # skipif-ci-and-not-linux


YieldRedisContainer = Callable[[], AbstractContextManager[RedisContainer[redis.Redis]]]


@composite
def redis_cms(draw: DrawFn, /) -> YieldRedisContainer:
    """Strategy for generating redis clients (with cleanup)."""
    from redis import Redis  # skipif-ci-and-not-linux
    from redis.exceptions import ResponseError  # skipif-ci-and-not-linux

    now = get_now(time_zone="local")  # skipif-ci-and-not-linux
    uuid = draw(uuids())  # skipif-ci-and-not-linux
    key = f"{now}_{uuid}"  # skipif-ci-and-not-linux

    @contextmanager
    def yield_redis() -> (  # skipif-ci-and-not-linux
        Iterator[RedisContainer[redis.Redis]]
    ):
        with Redis(db=15) as client:  # skipif-ci-and-not-linux
            keys = cast(list[KeyT], client.keys(pattern=f"{key}_*"))
            with suppress(ResponseError):
                _ = client.delete(*keys)
            yield RedisContainer(client=client, timestamp=now, uuid=uuid, key=key)
            keys = cast(list[KeyT], client.keys(pattern=f"{key}_*"))
            with suppress(ResponseError):
                _ = client.delete(*keys)

    return yield_redis  # skipif-ci-and-not-linux


def redis_cms_async(
    data: DataObject, /
) -> AbstractAsyncContextManager[RedisContainer[redis.asyncio.Redis]]:
    """Strategy for generating asynchronous redis clients."""
    from redis.asyncio import Redis  # skipif-ci-and-not-linux

    now = get_now(time_zone="local")  # skipif-ci-and-not-linux
    uuid = data.draw(uuids())  # skipif-ci-and-not-linux
    key = f"{now}_{uuid}"  # skipif-ci-and-not-linux

    @asynccontextmanager
    async def yield_redis_async() -> (  # skipif-ci-and-not-linux
        AsyncIterator[RedisContainer[redis.asyncio.Redis]]
    ):
        async with Redis(db=15) as client:  # skipif-ci-and-not-linux
            keys = cast(list[KeyT], await client.keys(pattern=f"{key}_*"))
            with suppress(ResponseError):
                _ = await client.delete(*keys)
            yield RedisContainer(client=client, timestamp=now, uuid=uuid, key=key)
            keys = cast(list[KeyT], await client.keys(pattern=f"{key}_*"))
            with suppress(ResponseError):
                _ = await client.delete(*keys)

    return yield_redis_async()  # skipif-ci-and-not-linux


def setup_hypothesis_profiles(
    *, suppress_health_check: Iterable[HealthCheck] = ()
) -> None:
    """Set up the hypothesis profiles."""

    class Profile(Enum):
        dev = auto()
        default = auto()
        ci = auto()
        debug = auto()

        @property
        def max_examples(self) -> int:
            match self:
                case Profile.dev | Profile.debug:
                    return 10
                case Profile.default:
                    return 100
                case Profile.ci:
                    return 1000
                case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
                    assert_never(never)

        @property
        def verbosity(self) -> Verbosity | None:
            match self:
                case Profile.dev | Profile.default | Profile.ci:
                    return Verbosity.normal
                case Profile.debug:
                    return Verbosity.debug
                case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
                    assert_never(never)

    phases = {Phase.explicit, Phase.reuse, Phase.generate, Phase.target}
    if "HYPOTHESIS_NO_SHRINK" not in environ:
        phases.add(Phase.shrink)
    for profile in Profile:
        try:
            max_examples = int(environ["HYPOTHESIS_MAX_EXAMPLES"])
        except KeyError:
            max_examples = profile.max_examples
        settings.register_profile(
            profile.name,
            max_examples=max_examples,
            phases=phases,
            report_multiple_bugs=True,
            deadline=None,
            print_blob=True,
            suppress_health_check=suppress_health_check,
            verbosity=profile.verbosity,
        )
    settings.load_profile(Profile.default.name)


def settings_with_reduced_examples(
    frac: float = 0.1,
    /,
    *,
    derandomize: bool = not_set,  # pyright: ignore[reportArgumentType]
    database: ExampleDatabase | None = not_set,  # pyright: ignore[reportArgumentType]
    verbosity: Verbosity = not_set,  # pyright: ignore[reportArgumentType]
    phases: Collection[Phase] = not_set,  # pyright: ignore[reportArgumentType]
    stateful_step_count: int = not_set,  # pyright: ignore[reportArgumentType]
    report_multiple_bugs: bool = not_set,  # pyright: ignore[reportArgumentType]
    suppress_health_check: Collection[HealthCheck] = not_set,  # pyright: ignore[reportArgumentType]
    deadline: float | dt.timedelta | None = not_set,  # pyright: ignore[reportArgumentType]
    print_blob: bool = not_set,  # pyright: ignore[reportArgumentType]
    backend: str = not_set,  # pyright: ignore[reportArgumentType]
) -> settings:
    """Set a test to fewer max examples."""
    curr = settings()
    max_examples = max(round(frac * curr.max_examples), 1)
    return settings(
        max_examples=max_examples,
        derandomize=derandomize,
        database=database,
        verbosity=verbosity,
        phases=phases,
        stateful_step_count=stateful_step_count,
        report_multiple_bugs=report_multiple_bugs,
        suppress_health_check=suppress_health_check,
        deadline=deadline,
        print_blob=print_blob,
        backend=backend,
    )


@composite
def slices(
    _draw: DrawFn,
    iter_len: MaybeSearchStrategy[int],
    /,
    *,
    slice_len: MaybeSearchStrategy[int | None] = None,
) -> slice:
    """Strategy for generating continuous slices from an iterable."""
    draw = lift_draw(_draw)
    iter_len_ = draw(iter_len)
    if (slice_len_ := draw(slice_len)) is None:
        slice_len_ = draw(integers(0, iter_len_))
    elif not 0 <= slice_len_ <= iter_len_:
        msg = f"Slice length {slice_len_} exceeds iterable length {iter_len_}"
        raise InvalidArgument(msg)
    start = draw(integers(0, iter_len_ - slice_len_))
    stop = start + slice_len_
    return slice(start, stop)


@composite
def sqlite_engines(
    _draw: DrawFn, /, *, metadata: MetaData | None = None, base: Any = None
) -> Engine:
    """Strategy for generating SQLite engines."""
    from utilities.sqlalchemy import create_engine

    temp_path = _draw(temp_paths())
    path = Path(temp_path, "db.sqlite")
    engine = create_engine("sqlite", database=str(path))
    cast(Any, engine).temp_path = temp_path  # keep `temp_path` alive
    if metadata is not None:
        metadata.create_all(engine)
    if base is not None:
        base.metadata.create_all(engine)
    return engine


@composite
def str_arrays(
    _draw: DrawFn,
    /,
    *,
    shape: MaybeSearchStrategy[Shape] | None = None,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    allow_none: MaybeSearchStrategy[bool] = False,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
) -> NDArrayO:
    """Strategy for generating arrays of strings."""
    from hypothesis.extra.numpy import array_shapes, arrays

    draw = lift_draw(_draw)
    shape_use = array_shapes() if shape is None else shape
    elements = text_ascii(min_size=min_size, max_size=max_size)
    if draw(allow_none):
        elements |= none()
    strategy: SearchStrategy[NDArrayO] = arrays(
        object, draw(shape_use), elements=elements, fill=fill, unique=draw(unique)
    )
    return draw(strategy)


_TEMP_DIR_HYPOTHESIS = Path(TEMP_DIR, "hypothesis")


@composite
def temp_dirs(_draw: DrawFn, /) -> TemporaryDirectory:
    """Search strategy for temporary directories."""
    _TEMP_DIR_HYPOTHESIS.mkdir(exist_ok=True)
    uuid = _draw(uuids())
    return TemporaryDirectory(
        prefix=f"{uuid}__", dir=_TEMP_DIR_HYPOTHESIS, ignore_cleanup_errors=IS_WINDOWS
    )


@composite
def temp_paths(_draw: DrawFn, /) -> Path:
    """Search strategy for paths to temporary directories."""
    temp_dir = _draw(temp_dirs())
    root = temp_dir.path
    cls = type(root)

    class SubPath(cls):
        _temp_dir = temp_dir

    return SubPath(root)


def text_ascii(
    *,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    disallow_na: MaybeSearchStrategy[bool] = False,
) -> SearchStrategy[str]:
    """Strategy for generating ASCII text."""
    return _draw_text(
        characters(whitelist_categories=[], whitelist_characters=ascii_letters),
        min_size=min_size,
        max_size=max_size,
        disallow_na=disallow_na,
    )


def text_clean(
    *,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    disallow_na: MaybeSearchStrategy[bool] = False,
) -> SearchStrategy[str]:
    """Strategy for generating clean text."""
    return _draw_text(
        characters(blacklist_categories=["Z", "C"]),
        min_size=min_size,
        max_size=max_size,
        disallow_na=disallow_na,
    )


def text_printable(
    *,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    disallow_na: MaybeSearchStrategy[bool] = False,
) -> SearchStrategy[str]:
    """Strategy for generating printable text."""
    return _draw_text(
        characters(whitelist_categories=[], whitelist_characters=printable),
        min_size=min_size,
        max_size=max_size,
        disallow_na=disallow_na,
    )


@composite
def timedeltas_2w(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[dt.timedelta] = dt.timedelta.min,
    max_value: MaybeSearchStrategy[dt.timedelta] = dt.timedelta.max,
) -> dt.timedelta:
    """Strategy for generating timedeltas which can be se/deserialized."""
    from utilities.whenever import MAX_TWO_WAY_TIMEDELTA, MIN_TWO_WAY_TIMEDELTA

    draw = lift_draw(_draw)
    min_value_ = max(draw(min_value), MIN_TWO_WAY_TIMEDELTA)
    max_value_ = min(draw(max_value), MAX_TWO_WAY_TIMEDELTA)
    return draw(timedeltas(min_value=min_value_, max_value=max_value_))


_ZONED_DATETIMES_LEFT_MOST = ZoneInfo("Asia/Manila")
_ZONED_DATETIMES_RIGHT_MOST = ZoneInfo("Pacific/Kiritimati")


@composite
def zoned_datetimes(
    _draw: DrawFn,
    /,
    *,
    min_value: MaybeSearchStrategy[dt.datetime] = dt.datetime.min,
    max_value: MaybeSearchStrategy[dt.datetime] = dt.datetime.max,
    time_zone: MaybeSearchStrategy[ZoneInfo | timezone] = UTC,
    valid: bool = False,
) -> dt.datetime:
    """Strategy for generating zoned datetimes."""
    draw = lift_draw(_draw)
    min_value_, max_value_, time_zone_ = (
        draw(min_value),
        draw(max_value),
        draw(time_zone),
    )
    if min_value_.tzinfo is not None:
        with assume_does_not_raise(OverflowError, match="date value out of range"):
            min_value_ = min_value_.astimezone(time_zone_)
        min_value_ = min_value_.replace(tzinfo=None)
    if max_value_.tzinfo is not None:
        with assume_does_not_raise(OverflowError, match="date value out of range"):
            max_value_ = max_value_.astimezone(time_zone_)
        max_value_ = max_value_.replace(tzinfo=None)
    strategy = datetimes(
        min_value=min_value_, max_value=max_value_, timezones=just(time_zone_)
    )
    datetime = draw(strategy)
    with assume_does_not_raise(OverflowError, match="date value out of range"):
        _ = datetime.astimezone(_ZONED_DATETIMES_LEFT_MOST)  # for dt.datetime.min
    with assume_does_not_raise(OverflowError, match="date value out of range"):
        _ = datetime.astimezone(  # for dt.datetime.max
            _ZONED_DATETIMES_RIGHT_MOST
        )
    result = datetime.astimezone(time_zone_)
    if valid:
        with assume_does_not_raise(  # skipif-ci-and-windows
            CheckValidZonedDateimeError
        ):
            check_valid_zoned_datetime(result)
    return result


@composite
def _draw_text(
    _draw: DrawFn,
    alphabet: MaybeSearchStrategy[str],
    /,
    *,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    disallow_na: MaybeSearchStrategy[bool] = False,
) -> str:
    """Draw from a text-generating strategy."""
    draw = lift_draw(_draw)
    drawn = draw(text(alphabet, min_size=draw(min_size), max_size=draw(max_size)))
    if draw(disallow_na):
        _ = assume(drawn != "NA")
    return drawn


__all__ = [
    "MaybeSearchStrategy",
    "RedisContainer",
    "Shape",
    "aiosqlite_engines",
    "assume_does_not_raise",
    "bool_arrays",
    "durations",
    "float_arrays",
    "floats_extra",
    "git_repos",
    "hashables",
    "int32s",
    "int64s",
    "int_arrays",
    "lift_draw",
    "lists_fixed_length",
    "months",
    "random_states",
    "redis_cms",
    "redis_cms_async",
    "setup_hypothesis_profiles",
    "slices",
    "sqlite_engines",
    "str_arrays",
    "temp_dirs",
    "temp_paths",
    "text_ascii",
    "text_clean",
    "text_printable",
    "timedeltas_2w",
    "zoned_datetimes",
]
