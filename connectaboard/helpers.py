from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class SeenCounter(Generic[T]):
    _previous: T
    n: int
    _seen_count = 0

    def has_been_seen_n_times(self, new: T) -> bool:
        if self._previous == new:
            self._seen_count += 1
        else:
            self._seen_count = 1
            self._previous = new
            return False

        return self._seen_count >= self.n
