import chess
import chess.engine
import serial
from dotenv import load_dotenv

from connectaboard import BoardController, BoardParser, Context, game_states, opponents
from connectaboard.config import BAUD_RATE, LIMIT, STOCKFISH_ENGINE, USB_PORT


def main():
    load_dotenv()
    board = chess.Board()
    ser = serial.Serial(USB_PORT, BAUD_RATE, timeout=0.5)
    controller = BoardController(ser)
    parser = BoardParser(board)
    state = game_states.PlayersTurn()

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_ENGINE) as engine:
        opponent = opponents.Engine(engine, LIMIT)
        conntectaboard = Context(controller, parser, board, opponent)

        while not board.is_game_over():
            print(state)
            state = state.execute(conntectaboard)


if __name__ == "__main__":
    main()
