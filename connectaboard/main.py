import chess
import chess.engine
import serial

from connectaboard import BoardController, BoardParser, Context, game_states, opponent
from connectaboard.config import BAUD_RATE, LIMIT, PATH_TO_ENGINE, USB_PORT


def main():
    board = chess.Board()
    ser = serial.Serial(USB_PORT, BAUD_RATE, timeout=0.5)
    controller = BoardController(ser)
    parser = BoardParser(board)
    state = game_states.PlayersTurn()

    with chess.engine.SimpleEngine.popen_uci(PATH_TO_ENGINE) as engine:
        foe = opponent.Engine(engine, LIMIT)
        conntectaboard = Context(controller, parser, board, foe)

        while not board.is_game_over():
            print(state)
            state = state.execute(conntectaboard)


if __name__ == "__main__":
    main()
