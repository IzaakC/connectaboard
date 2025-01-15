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


class BoardParser:
    _previous_state: bytes

    @dataclass
    class State:
        board: bytes
        changed: list[SquareChange]
        move: None | chess.Move

    def __init__(self, inital_state: chess.Board) -> None:
        self._previous_state = self.board2raw(inital_state)

    @staticmethod
    def board2raw(board: chess.Board) -> bytes:
        pieces = [board.piece_at(square) for square in chess.SQUARES]
        return bytes(_piece2raw(piece) for piece in pieces)

    def parse(self, new_state: bytes) -> State:
        if new_state == self._previous_state:
            return self.State(new_state, [], None)

        changes = self._detect_changes(new_state)
        move = self._detect_move(changes)
        return self.State(new_state, changes, move)

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

        if a.new == EMPTY and b.new == a.prev:
            return chess.Move(a.square, b.square)

        if b.new == EMPTY and a.new == b.prev:
            return chess.Move(b.square, a.square)

        return None
