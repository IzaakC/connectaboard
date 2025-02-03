from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import sleep

import chess
import chess.engine

from connectaboard import Context, config, more_chess


class GameState(ABC):
    @abstractmethod
    def execute(self, context: Context) -> "GameState":
        pass


@dataclass
class PlayersTurn(GameState):
    def execute(self, context: Context) -> GameState:
        context.controller.turn_on_leds(context.promoted_pieces, pulse=False)
        move = context.wait_for_move()
        if move is None:
            return Recovery(self, "Too many changes!")

        if not context.board.is_legal(move):
            return Recovery(self, "Not a legal move.")

        print(f"you've played {move}")

        if context.board.is_castling(move):
            print("castling!")
            context.push_move(move)
            rook_move = more_chess.get_rook_move_for_castling(move)
            return WaitForMove(rook_move, OppenentsTurn(), indicate=False, push=False)

        if more_chess.is_en_passant(move, context.board):
            context.push_move(move)
            return Recovery(
                OppenentsTurn(), "Check if enpassant capture piece is removed"
            )

        if more_chess.is_promotable(move, context.board):
            move.promotion = chess.QUEEN

        context.push_move(move)

        return OppenentsTurn()


@dataclass
class WaitForMove(GameState):
    move: chess.Move
    next_state: GameState
    indicate: bool = field(default=True)
    push: bool = field(default=True)

    def execute(self, context: Context) -> GameState:
        expected_move = self.move

        if self.indicate:
            context.controller.show_move(expected_move, pulse=False)

        played_move = context.wait_for_move()

        if played_move is None:
            return Recovery(self, "Too many changes!")

        # compare move, disregarding promotion.
        if not more_chess.have_same_from_and_to_square(played_move, expected_move):
            msg = f"Not the right move! {played_move = }, {expected_move = }"
            return Recovery(self, msg)

        if self.push:
            context.push_move(expected_move)
        else:
            context.parser.accept_pending_state()

        return self.next_state


@dataclass
class Recovery(GameState):
    next_state: GameState
    msg: str

    def execute(self, context: Context) -> GameState:
        print(self.msg)
        print("\nPlease return board to this state:")
        print(context.board)
        while True:
            raw_board = context.controller.receive_board()
            if self.indicate_fixes_and_check(raw_board, context):
                context.controller.clear_leds()
                return self.next_state
            sleep(config.SLEEP_TIME)

    def indicate_fixes_and_check(self, raw_board: bytes, context: Context) -> bool:
        need_to_be_removed = context.parser.detect_pieces_that_should_not_be_there(
            context.board, raw_board
        )
        if need_to_be_removed:
            context.controller.turn_on_leds(need_to_be_removed, pulse=True)
            return False

        missing = context.parser.detect_missing_pieces(context.board, raw_board)
        if missing:
            piece, square = missing[0]
            moves = more_chess.attacking_squares_for_piece_at(piece, square)
            moves.append(square)
            context.controller.turn_on_leds(moves, piece.color == chess.WHITE)
            return False

        return True


@dataclass
class OppenentsTurn(GameState):
    def execute(self, context: Context) -> GameState:
        move = context.opponent.play(context.board)
        print(f"computer playes {move}")
        if context.board.is_castling(move):
            rook_move = more_chess.get_rook_move_for_castling(move)
            return WaitForMove(move, WaitForMove(rook_move, PlayersTurn(), push=False))

        if more_chess.is_en_passant(move, context.board):
            return WaitForMove(
                move,
                Recovery(PlayersTurn(), "Check if en passant capture is removed."),
            )

        return WaitForMove(move, PlayersTurn())
