from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Any, Callable, Generator, Iterable, Iterator, TypeVar

from jinja2 import Template

T = TypeVar("T")


def item_formatter(template: str) -> Template:
    return Template(
        template,
        variable_start_string="{",
        variable_end_string="}",
        autoescape=False,
        keep_trailing_newline=True,
        finalize=lambda x: x or "",
    )


@contextmanager
def concurrentcontext(
    function: Callable[[T], Any],
    generator: Iterable[T],
    *,
    workers: int | None = None,
) -> Generator[Iterator[Any], Any, None]:
    """With context, run a function on a batch of arguments concurrently."""

    with ThreadPoolExecutor(max_workers=workers) as executor:
        yield executor.map(function, generator)


def concurrent(
    function: Callable[[T], Any],
    generator: Iterable[T],
    *,
    workers: int | None = None,
) -> list:
    """Run a functions on a batch of arguments in concurrently."""

    with concurrentcontext(function, generator, workers=workers) as results:
        return list(results)
