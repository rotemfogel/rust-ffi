import functools
import inspect
import logging
import os
import time
from types import TracebackType
from typing import Callable, ParamSpec, TypeVar, Literal, Awaitable, cast, Any, Type

P = ParamSpec("P")
T = TypeVar("T")


class TimedLogger(logging.Logger):

    def time(self):
        logger: logging.Logger = self

        def decorator(f: Callable[P, T]) -> Callable[P, T]:

            class FuncL:
                def __init__(self, *args: P.args, **kwargs: P.kwargs):
                    self.args = args
                    self.kwargs = kwargs

                def __enter__(self) -> "FuncL":
                    logger.error(
                        msg=f"executing {f.__name__}...",
                    )
                    self.start_time = time.time()
                    return self

                def __exit__(
                        self,
                        exc_type: Type[BaseException] | None,
                        exc_val: BaseException | None,
                        exc_tb: TracebackType | None,
                ) -> Literal[False]:
                    exec_time = time.time() - self.start_time
                    logger.error(
                        msg=f"{f.__name__} executed in {exec_time:.2f} sec",
                    )
                    return False

                def execute_sync(self) -> T:
                    result = f(*self.args, **self.kwargs)
                    return result

                async def execute_async(self) -> Any:
                    async_fn = cast(Callable[P, Awaitable[Any]], f)
                    result = await async_fn(*self.args, **self.kwargs)
                    return result

            def call(*args: P.args, **kwargs: P.kwargs):
                if inspect.iscoroutinefunction(f):

                    @functools.wraps(f)
                    async def async_executor() -> Any:
                        with FuncL(*args, **kwargs) as fl:
                            value = fl.execute_async()
                        return value

                    wrapper = async_executor()
                else:

                    @functools.wraps(f)
                    def sync_executor() -> Any:
                        with FuncL(*args, **kwargs) as fl:
                            value = fl.execute_sync()
                        return value

                    wrapper = sync_executor()
                return cast(Callable[P, T], wrapper)

            return call

        return decorator


def _get_module_name(stack_offset: int = 0) -> str:
    caller_frame = inspect.stack()[1 + stack_offset]
    file_name = caller_frame.filename
    file_path = os.path.relpath(file_name, ".")
    return file_path.split(os.sep)[-1].split(".")[0]


def get_logger(name: str | None = None) -> TimedLogger:
    if not name:
        name = _get_module_name(stack_offset=1)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(name)
    return TimedLogger(logger)
