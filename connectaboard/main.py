from time import sleep

import chess

from connectaboard import BoardController, BoardParser


def main():
    board = chess.Board()
    controller = BoardController("/dev/ttyUSB0")
    parser = BoardParser(board)

    while True:
        raw_board = controller.receive_board()
        state = parser.parse(raw_board)

        if state.changed:
            controller.turn_on_leds(
                [change.square for change in state.changed], pulse=False
            )

        if state.move is not None:
            if board.is_legal(state.move):
                parser.accept_state(state)
                board.push(state.move)
                controller.show_move(state.move, pulse=False)
                print(state.move)
                print(board)

            else:
                print("Illegal move!")
                controller.show_move(state.move, pulse=True)

        sleep(0.1)


if __name__ == "__main__":
    main()
