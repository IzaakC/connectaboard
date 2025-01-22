from dataclasses import dataclass
from time import sleep

import chess
import chess.engine

from connectaboard.board_controller import BoardController
from connectaboard.board_parser import BoardParser
from connectaboard.config import SEEN_EXACTLY_N_TIMES, SLEEP_TIME
from connectaboard.helpers import SeenCounter
from connectaboard.opponent import Opponent


@dataclass
class Context:
    controller: BoardController
    parser: BoardParser
    board: chess.Board
    opponent: Opponent

    def board_state_is_valid(self) -> bool:
        raw_board = self.controller.receive_board()
        return self.parser.is_state_valid(self.board, raw_board)

    def wait_for_changes(self) -> BoardParser.State:
        """Waits for changes in the board.
        Only returns when the state has changed and has been seen at least SEEN_EXACTLY_N_TIMES times in succession."""
        seen_counter = SeenCounter[bytes](SEEN_EXACTLY_N_TIMES)
        while True:
            raw_board = self.controller.receive_board()
            state = self.parser.parse(raw_board)
            trust_state = seen_counter.has_been_seen_n_times(raw_board)

            if trust_state and state.changed:
                return state

            sleep(SLEEP_TIME)

    def wait_for_move(self) -> chess.Move | None:
        while True:
            state = self.wait_for_changes()
            if state.move:
                return state.move
            if len(state.changed) == 3 and state.changed_to_empty_count == 2:
                # could be that we're waiting for a piece te be placed after attacking
                continue
            if len(state.changed) > 2:
                return None
            sleep(SLEEP_TIME)

    def push_move(self, move: chess.Move) -> None:
        self.board.push(move)
        self.parser.accept_pending_state()
