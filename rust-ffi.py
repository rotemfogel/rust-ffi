import random
import rust_ffi as rs
from logger import get_logger

_LOG = get_logger()
_DATA = "\n".join(
    [
        " ".join(
            ["bob"] * random.randint(1, 101)
            + ["dan"] * random.randint(1, 101)
            + ["jim"] * random.randint(1, 101)
        )
        for _ in range(1_000_000)
    ]
)
_FIND = "dan"


@_LOG.time()
def pure_python(contents: str, needle: str) -> int:
    total = 0
    for line in contents.splitlines():
        for word in line.split(" "):
            if word == needle:
                total += 1
    return total


@_LOG.time()
def c_python(contents: str, needle: str) -> int:
    return contents.count(needle)


@_LOG.time()
def rust(contents: str, needle: str) -> int:
    return rs.search_rs(contents, needle)


@_LOG.time()
def par_rust(contents: str, needle: str) -> int:
    return rs.par_search_rs(contents, needle)


if __name__ == "__main__":
    _LOG.error(pure_python(_DATA, _FIND))
    _LOG.error(c_python(_DATA, _FIND))
    _LOG.error(rust(_DATA, _FIND))
    _LOG.error(par_rust(_DATA, _FIND))
