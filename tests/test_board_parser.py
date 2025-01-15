import chess

from connectaboard.board_parser import (
    BLACK,
    EMPTY,
    WHITE,
    BoardParser,
    SquareChange,
)


def test_board2raw():
    board = chess.Board()
    raw = BoardParser.board2raw(board)
    assert raw[chess.A1] == WHITE
    assert raw[chess.E4] == EMPTY
    assert raw[chess.H8] == BLACK


def test_square_change():
    change = SquareChange(WHITE, BLACK, chess.E4)
    assert change.prev == WHITE
    assert change.new == BLACK
    assert change.square == chess.E4


def test_board_parser_initial_state():
    board = chess.Board()
    parser = BoardParser(board)
    raw_state = parser._previous_state
    expected_state = BoardParser.board2raw(board)

    assert raw_state == expected_state
    assert len(raw_state) == 64


def test_board_parser_parse_no_change():
    board = chess.Board()
    parser = BoardParser(board)

    state = parser.parse(parser._previous_state)
    assert state.board == parser._previous_state
    assert state.changed == []
    assert state.move is None


def test_board_parser_parse_with_move():
    board = chess.Board()
    parser = BoardParser(board)

    # Simulate a move: e2 to e4
    board.push(chess.Move.from_uci("e2e4"))
    new_raw = BoardParser.board2raw(board)
    state = parser.parse(new_raw)

    assert len(state.changed) == 2
    assert state.move == chess.Move.from_uci("e2e4")

    parser.accept_state(state)
    state = parser.parse(new_raw)
    assert state.changed == []
    assert state.move is None


def test_board_parser_accept_state():
    board = chess.Board()
    parser = BoardParser(board)

    raw_state = parser._previous_state
    state = parser.parse(raw_state)

    parser.accept_state(state)
    assert parser._previous_state == state.board
