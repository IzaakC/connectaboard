from abc import ABC, abstractmethod
from dataclasses import dataclass

import chess
import chess.engine


class Opponent(ABC):
    @abstractmethod
    def play(self, board: chess.Board) -> chess.Move:
        pass


@dataclass
class Engine(Opponent):
    engine: chess.engine.SimpleEngine
    limit: chess.engine.Limit

    def play(self, board: chess.Board) -> chess.Move:
        result = self.engine.play(board, self.limit)
        move = result.move

        if not move:
            raise RuntimeError("No move..")

        return move


class ChessDotComPlayer(Opponent):
    def play(self, board: chess.Board) -> chess.Move:
        player_move = board.move_stack[-1]
        raise NotImplementedError()
