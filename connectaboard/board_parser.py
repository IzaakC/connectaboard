from dataclasses import dataclass

import chess

WHITE = 0
BLACK = 1
EMPTY = 2


SquareState = int


@dataclass
class SquareChange:
    prev: SquareState
    new: SquareState
    square: chess.Square


def _piece2raw(piece: chess.Piece | None) -> SquareState:
    if not piece:
        return EMPTY
    elif piece.color == chess.WHITE:
        return WHITE
    return BLACK


def _board2raw(board: chess.Board) -> bytes:
    pieces = [board.piece_at(square) for square in chess.SQUARES]
    return bytes(_piece2raw(piece) for piece in pieces)


@dataclass
class State:
    board: bytes
    changed: list[SquareChange]
    move: None | chess.Move


class BoardParser:
    _previous_state: bytes

    def __init__(self, inital_state: chess.Board) -> None:
        self._previous_state = _board2raw(inital_state)

    def parse(self, new_state: bytes) -> State:
        if new_state == self._previous_state:
            return State(new_state, [], None)

        changes = self._detect_changes(new_state)
        move = self._detect_move(changes)
        return State(new_state, changes, move)

    def accept_state(self, state: State):
        self._previous_state = state.board

    def _detect_changes(self, new_state: bytes) -> list[SquareChange]:
        return [
            SquareChange(old, new, square)
            for old, new, square in zip(self._previous_state, new_state, chess.SQUARES)
            if old != new
        ]

    def _detect_move(self, changed: list[SquareChange]) -> chess.Move | None:
        if len(changed) != 2:
            return None

        a, b = changed

        if a.new == EMPTY:
            return chess.Move(a.square, b.square)
        return chess.Move(b.square, a.square)
