from typing import Generic, TypeVar

T = TypeVar("T")


class SeenCounter(Generic[T]):
    _previous: T | None = None
    n: int
    _seen_count: int = 0

    def __init__(self, n: int) -> None:
        self.n = n

    def has_been_seen_n_times(self, new: T) -> bool:
        if self._previous == new:
            self._seen_count += 1
        else:
            self._seen_count = 1
            self._previous = new
            return False

        return self._seen_count == self.n
