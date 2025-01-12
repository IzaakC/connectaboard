from time import sleep

import chess
import serial

from connectaboard import BoardController, BoardParser


def main():
    board = chess.Board()
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)
    controller = BoardController(ser)
    parser = BoardParser(board)
    previous_raw = parser._previous_state

    while True:
        raw_board = controller.receive_board()

        if raw_board == previous_raw:
            sleep(0.1)
            continue
        previous_raw = raw_board

        state = parser.parse(raw_board)

        if state.move is not None:
            if board.is_legal(state.move):
                parser.accept_state(state)
                board.push(state.move)
                controller.show_move(state.move, pulse=False)
                print(state.move)
                print(board)

            else:
                print(f"Illegal move!: {state.move.uci()}")
                controller.show_move(state.move, pulse=True)

        sleep(0.2)


if __name__ == "__main__":
    main()
