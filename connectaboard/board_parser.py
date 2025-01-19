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
    _pending_state: bytes

    @dataclass
    class State:
        board: bytes
        changed: list[SquareChange]
        move: None | chess.Move

        @property
        def changed_to_empty_count(self) -> int:
            return sum(c.new == EMPTY for c in self.changed)

        @property
        def changed_to_piece_count(self) -> int:
            return len(self.changed) - self.changed_to_empty_count

    def __init__(self, inital_state: chess.Board) -> None:
        self._previous_state = self.board2raw(inital_state)
        self._pending_state = self.board2raw(inital_state)

    @staticmethod
    def board2raw(board: chess.Board) -> bytes:
        pieces = [board.piece_at(square) for square in chess.SQUARES]
        return bytes(_piece2raw(piece) for piece in pieces)

    def parse(self, new_state: bytes) -> State:
        if new_state == self._previous_state:
            return self.State(new_state, [], None)

        self._pending_state = new_state
        changes = self._detect_changes(new_state)
        move = self._detect_move(changes)
        return self.State(new_state, changes, move)

    def accept_pending_state(self):
        self._previous_state = self._pending_state

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

    def detect_pieces_that_should_not_be_there(
        self, board: chess.Board, raw_board: bytes
    ) -> list[SquareState]:
        expected_raw = self.board2raw(board)

        return [
            square
            for expected, actual, square in zip(expected_raw, raw_board, chess.SQUARES)
            if expected != actual and actual != EMPTY
        ]

    def detect_missing_pieces(
        self, board: chess.Board, raw_board: bytes
    ) -> list[tuple[chess.Piece, chess.Square]]:
        piece_map = board.piece_map()
        return [
            (piece_map[square], square)
            for actual, square in zip(raw_board, chess.SQUARES)
            if square in piece_map and actual == EMPTY
        ]

    def is_state_valid(self, board: chess.Board, state: bytes) -> bool:
        expected = self.board2raw(board)
        return expected == state
