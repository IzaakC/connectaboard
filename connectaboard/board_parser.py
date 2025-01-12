import enum
from dataclasses import dataclass

import chess


class SquareState(enum.Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2


@dataclass
class SeenCounter:
    _previous: tuple[int, ...]
    n: int
    _seen_count = 0

    def has_been_seen_n_times(self, new: tuple[int, ...]) -> bool:
        if self._previous == new:
            self._seen_count += 1
        else:
            self._seen_count = 1
            self._previous = new
            return False

        return self._seen_count >= self.n


@dataclass
class Square:
    state: SquareState
    square: chess.Square

    @classmethod
    def from_piece(cls, piece: chess.Piece | None, square: chess.Square) -> "Square":
        if not piece:
            state = SquareState.EMPTY
        elif piece.color == chess.WHITE:
            state = SquareState.WHITE
        else:
            state = SquareState.BLACK
        return cls(state, square)

    @classmethod
    def from_raw(cls, raw: int, square: chess.Square) -> "Square":
        return cls(SquareState(raw), square)


class SquareChange:
    prev: SquareState
    new: SquareState
    square: chess.Square

    def __init__(self, prev: Square, new: Square):
        self.prev = prev.state
        self.new = new.state
        self.square = prev.square


def _board2squares(board: chess.Board) -> tuple[Square, ...]:
    pieces = [(board.piece_at(square), square) for square in chess.SQUARES]
    return tuple(Square.from_piece(piece, square) for piece, square in pieces)


def _parse_square_states(board: tuple[int, ...]) -> tuple[Square, ...]:
    return tuple(Square.from_raw(raw, square) for square, raw in enumerate(board))


@dataclass
class State:
    board: tuple[Square, ...]
    changed: tuple[SquareChange, ...]
    move: None | chess.Move


class BoardParser:
    _previous_state: tuple[Square, ...]

    def __init__(self, inital_state: chess.Board) -> None:
        self._previous_state = _board2squares(inital_state)

    def parse(self, raw_board: tuple[int, ...]) -> State:
        pending_state = _parse_square_states(raw_board)
        if pending_state == self._previous_state:
            return State(pending_state, (), None)

        changes = self._detect_changes(pending_state)
        move = self._detect_move(changes)
        return State(pending_state, changes, move)

    def accept_state(self, state: State):
        self._previous_state = state.board

    def _detect_changes(
        self, pending_state: tuple[Square, ...]
    ) -> tuple[SquareChange, ...]:
        return tuple(
            SquareChange(prev, pend)
            for prev, pend in zip(self._previous_state, pending_state)
            if prev.state != pend.state
        )

    def _detect_move(self, changed: tuple[SquareChange, ...]) -> chess.Move | None:
        if len(changed) != 2:
            return None

        a, b = changed

        if a.new == SquareState.EMPTY:
            return chess.Move(a.square, b.square)
        return chess.Move(b.square, a.square)
