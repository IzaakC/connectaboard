from abc import ABC, abstractmethod
from dataclasses import dataclass

import chess
import chess.engine


class Foe(ABC):
    @abstractmethod
    def play(self, board: chess.Board) -> chess.Move:
        pass


@dataclass
class Engine(Foe):
    engine: chess.engine.SimpleEngine
    time_limit: float

    def play(self, board: chess.Board) -> chess.Move:
        result = self.engine.play(board, chess.engine.Limit(self.time_limit))
        move = result.move

        if not move:
            raise RuntimeError("No move..")

        return move


class ChessDotComPlayer(Foe):
    def play(self, board: chess.Board) -> chess.Move:
        player_move = board.move_stack[-1]
        raise NotImplementedError()
