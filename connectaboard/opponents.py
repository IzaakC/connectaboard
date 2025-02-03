from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint
from time import sleep

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


class RandomDelayEngine(Engine):
    max_delay_seconds = 60

    def play(self, board: chess.Board) -> chess.Move:
        delay = randint(1, self.max_delay_seconds)
        sleep(delay)
        return super().play(board)
