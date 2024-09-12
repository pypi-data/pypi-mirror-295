from __future__ import annotations

from asyncio import TaskGroup, get_running_loop, run_coroutine_threadsafe
from collections.abc import Iterable, MutableMapping
from contextvars import copy_context
from dataclasses import dataclass, field
from functools import partial
from heapq import heappop, heappush
from inspect import iscoroutine, iscoroutinefunction
from threading import Thread
from typing import TYPE_CHECKING, Generic, ParamSpec, TypeVar, overload

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop, Task
    from collections.abc import Callable, Coroutine, Generator, Iterator
    from contextvars import Context
    from typing import Any, Self

__all__: tuple[str, ...] = (
    "CancellableGather",
    "ensure_async",
    "make_hashable",
    "PrioritizedItem",
    "run_in_background",
)

T = TypeVar("T")
S = TypeVar("S")
P = ParamSpec("P")


@dataclass(order=True, slots=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T = field(compare=False)


@dataclass(slots=True)
class CancellableGather(Generic[T]):
    coroutines: Iterable[Coroutine[Any, Any, T]]
    results: list[PrioritizedItem[T]] = field(default_factory=list, init=False)

    @classmethod
    def map(cls, function: Callable[[S], Coroutine[Any, Any, T]], iterable: Iterable[S], /) -> Self:
        return cls(map(function, iterable))

    def __await__(self) -> Generator[Any, None, tuple[T, ...]]:
        #: ---
        #: Create a suitable iterator by calling __await__ on a coroutine.
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> tuple[T, ...]:
        context: Context = copy_context()
        try:
            async with TaskGroup() as group:
                for priority, coroutine in enumerate(self.coroutines):
                    task: Task[T] = group.create_task(coroutine, context=context)
                    callback: partial[None] = partial(self.populate_results, priority=priority)
                    task.add_done_callback(callback, context=context)
        except BaseExceptionGroup as exc_group:
            #: ---
            #: Propagate the first raised exception from exception group:
            for exc in self.exception_from_group(exc_group):
                raise exc from None

        return tuple(self.iter_results())

    def populate_results(self, task: Task[T], *, priority: int) -> None:
        if not task.cancelled() and task.exception() is None:
            result: PrioritizedItem[T] = PrioritizedItem(priority, task.result())
            heappush(self.results, result)

    def exception_from_group(self, exc: BaseException) -> Iterator[BaseException]:
        if isinstance(exc, BaseExceptionGroup):
            for nested in exc.exceptions:
                yield from self.exception_from_group(nested)
        else:
            yield exc

    def iter_results(self) -> Iterator[T]:
        while True:
            try:
                result: PrioritizedItem[T] = heappop(self.results)
                yield result.item
            except IndexError:
                break


@overload
async def ensure_async(function: Callable[P, Coroutine[Any, Any, T]], /, *args: P.args, **kwargs: P.kwargs) -> T: ...


@overload
async def ensure_async(function: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T: ...


async def ensure_async(function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> Any:
    loop: AbstractEventLoop = get_running_loop()
    context: Context = copy_context()

    if iscoroutinefunction(callback := partial(function, *args, **kwargs)):
        return await loop.create_task(callback(), context=context)
    else:
        return await loop.run_in_executor(None, context.run, callback)


def make_hashable(obj: Any, /) -> Any:
    if isinstance(obj, MutableMapping):
        return tuple((key, make_hashable(value)) for key, value in sorted(obj.items()))
    #: ---
    #: Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    #: to a tuple:
    try:
        hash(obj)
    except TypeError:
        if isinstance(obj, Iterable):
            return tuple(map(make_hashable, obj))
        #: ---
        #: Non-hashable, non-iterable:
        raise

    return obj


def run_in_background(coroutine: Coroutine[Any, Any, Any], /) -> None:
    if not iscoroutine(coroutine):
        raise TypeError(f"a coroutine was expected, got {type(coroutine).__name__!r}")

    def spawn_thread(function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> None:
        thread: Thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.start()

    loop: AbstractEventLoop = get_running_loop()
    spawn_thread(run_coroutine_threadsafe, coroutine, loop)
