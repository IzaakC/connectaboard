from typing import Protocol

import chess

_READ_BOARD = b"r"
_SHOW_LEDS = b"l"
_PULSE_FLAG = 0b01000000
_ON_FLAG = 0b10000000


class SupportsReadWrite(Protocol):
    def read(self, size: int) -> bytes: ...
    def write(self, b: bytes, /) -> int | None: ...


class BoardController:
    comms: SupportsReadWrite
    _brightness: int = 7

    def set_brightness(self, value: int):
        if 0 <= value <= 7:
            self._brightness = value
            return

        msg = f"Brightness outside of range: {value} not in [0, 7]"
        raise ValueError(msg)

    def __init__(self, comms: SupportsReadWrite) -> None:
        self.comms = comms

    def receive_board(self) -> bytes:
        self.comms.write(_READ_BOARD)
        return self.comms.read(64)

    def show_move(self, move: chess.Move, pulse: bool) -> None:
        self.turn_on_leds([move.from_square, move.to_square], pulse)

    def turn_on_leds(self, squares: list[chess.Square], pulse: bool) -> None:
        config = self._brightness | pulse * _PULSE_FLAG | _ON_FLAG
        msg = [config if s in squares else 0 for s in chess.SQUARES]
        self.comms.write(_SHOW_LEDS)
        self.comms.write(bytes(msg))

    def clear_leds(self) -> None:
        msg = [0 for _ in chess.SQUARES]
        self.comms.write(_SHOW_LEDS)
        self.comms.write(bytes(msg))
