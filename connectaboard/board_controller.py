import chess
import serial

_READ_BOARD = b"r"
_SHOW_LEDS = b"l"
_PULSE_FLAG = 0b01000000


def _led_config(square: chess.Square, pulse: bool) -> int:
    return square


class BoardController:
    ser: serial.Serial
    _brightness: int = 7

    def set_brightness(self, value: int):
        if 0 <= value <= 7:
            self._brightness = value
            return

        msg = f"Brightness outside of range: {value} not in [0, 7]"
        raise ValueError(msg)

    def __init__(self, port: str) -> None:
        self.ser = serial.Serial(port, 115200, timeout=0.5)

    def receive_board(self) -> tuple[int, ...]:
        self.ser.write(_READ_BOARD)
        return tuple(self.ser.read(64))

    def show_move(self, move: chess.Move, pulse: bool) -> None:
        self.turn_on_leds([move.from_square, move.to_square], pulse)

    def turn_on_leds(self, squares: list[chess.Square], pulse: bool) -> None:
        config = self._brightness | pulse * _PULSE_FLAG
        msg = [config if s in squares else 0 for s in chess.SQUARES]
        self.ser.write(_SHOW_LEDS)
        self.ser.write(bytes(msg))
