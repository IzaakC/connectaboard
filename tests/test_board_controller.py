import chess
import pytest

from connectaboard.board_controller import (
    _ON_FLAG,
    _PULSE_FLAG,
    _READ_BOARD,
    _SHOW_LEDS,
    BoardController,
)


class MockSerial:
    returned_on_read: bytes
    writen_to_on_write: list[bytes]

    def __init__(self):
        self.writen_to_on_write = list()

    def read(self, size: int) -> bytes:
        return self.returned_on_read

    def write(self, b: bytes, /) -> int | None:
        if self.writen_to_on_write:
            self.writen_to_on_write.append(b)
        else:
            self.writen_to_on_write = [b]


@pytest.fixture
def board_and_comms() -> tuple[BoardController, MockSerial]:
    mock_serial = MockSerial()
    return BoardController(mock_serial), mock_serial


def test_read_board(board_and_comms: tuple[BoardController, MockSerial]):
    bc, c = board_and_comms
    c.returned_on_read = b"abc"
    board = bc.receive_board()

    assert c.writen_to_on_write[0] == _READ_BOARD
    assert board == b"abc"


def test_show_move(board_and_comms: tuple[BoardController, MockSerial]):
    bc, c = board_and_comms

    bc.show_move(move=chess.Move(chess.A1, chess.B1), pulse=False)

    assert c.writen_to_on_write[0] == _SHOW_LEDS
    assert c.writen_to_on_write[1][chess.A1] == bc._brightness | _ON_FLAG
    assert c.writen_to_on_write[1][chess.B1] == bc._brightness | _ON_FLAG

    bc.show_move(move=chess.Move(chess.E4, chess.G1), pulse=True)

    assert c.writen_to_on_write[2] == _SHOW_LEDS
    assert c.writen_to_on_write[3][chess.A1] == 0
    assert c.writen_to_on_write[3][chess.B1] == 0
    assert c.writen_to_on_write[3][chess.E4] == bc._brightness | _ON_FLAG | _PULSE_FLAG
    assert c.writen_to_on_write[3][chess.G1] == bc._brightness | _ON_FLAG | _PULSE_FLAG


def test_turn_on_leds(board_and_comms: tuple[BoardController, MockSerial]):
    bc, c = board_and_comms
    squares = [chess.A1, chess.G1, chess.H6]
    bc.turn_on_leds(squares, pulse=True)

    assert c.writen_to_on_write[0] == _SHOW_LEDS
    for square in squares:
        assert (
            c.writen_to_on_write[1][square] == bc._brightness | _ON_FLAG | _PULSE_FLAG
        )


def test_set_brightness(board_and_comms: tuple[BoardController, MockSerial]):
    bc, _ = board_and_comms
    bc.set_brightness(0)
    assert bc._brightness == 0

    with pytest.raises(ValueError):
        bc.set_brightness(-1)

    with pytest.raises(ValueError):
        bc.set_brightness(8)
