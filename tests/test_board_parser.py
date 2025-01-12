import chess

from connectaboard.board_parser import (
    BoardParser,
    SeenCounter,
    Square,
    SquareChange,
    SquareState,
    _board2squares,
)


def test_board2squares():
    board = chess.Board()
    squares = _board2squares(board)
    assert squares[chess.A1] == Square(SquareState.WHITE, chess.A1)
    assert squares[chess.E4] == Square(SquareState.EMPTY, chess.E4)
    assert squares[chess.H8] == Square(SquareState.BLACK, chess.H8)


def test_square_from_piece():
    board = chess.Board()
    piece = board.piece_at(chess.E4)
    square = Square.from_piece(piece, chess.E4)
    assert square.state == SquareState.EMPTY

    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))
    piece = board.piece_at(chess.E4)
    square = Square.from_piece(piece, chess.E4)
    assert square.state == SquareState.WHITE

    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.BLACK))
    piece = board.piece_at(chess.E4)
    square = Square.from_piece(piece, chess.E4)
    assert square.state == SquareState.BLACK


def test_square_from_raw():
    raw_state = SquareState.WHITE.value
    square = Square.from_raw(raw_state, chess.E4)
    assert square.state == SquareState.WHITE


def test_square_change():
    prev = Square(SquareState.WHITE, chess.E4)
    new = Square(SquareState.BLACK, chess.E4)
    change = SquareChange(prev, new)
    assert change.prev == SquareState.WHITE
    assert change.new == SquareState.BLACK
    assert change.square == chess.E4


def test_board_parser_initial_state():
    board = chess.Board()
    parser = BoardParser(board)
    squares = parser._previous_state
    pieces = board.piece_map()

    assert len(squares) == 64
    for square in squares:
        piece = pieces.get(square.square)
        if not piece:
            assert square.state == SquareState.EMPTY
        elif piece.color == chess.WHITE:
            assert square.state == SquareState.WHITE
        else:
            assert square.state == SquareState.BLACK


def test_board_parser_parse_no_change():
    board = chess.Board()
    parser = BoardParser(board)

    raw_board = tuple(square.state.value for square in parser._previous_state)
    print(raw_board)
    state = parser.parse(raw_board)

    assert state.changed == ()
    assert state.move is None


def test_board_parser_parse_with_move():
    board = chess.Board()
    parser = BoardParser(board)

    # Simulate a move: e2 to e4
    board.push(chess.Move.from_uci("e2e4"))
    squares = _board2squares(board)
    raw_board = tuple(square.state.value for square in squares)
    state = parser.parse(raw_board)

    assert len(state.changed) == 2
    assert state.move == chess.Move.from_uci("e2e4")

    parser.accept_state(state)
    state = parser.parse(raw_board)
    assert len(state.changed) == 0
    assert state.move is None


def test_board_parser_accept_state():
    board = chess.Board()
    parser = BoardParser(board)

    raw_board = tuple(square.state.value for square in parser._previous_state)
    state = parser.parse(raw_board)

    parser.accept_state(state)
    assert parser._previous_state == state.board


def test_seen_counter():
    inital = (0,)
    new = (1,)
    seen_counter = SeenCounter(inital, 3)
    assert not seen_counter.has_been_seen_n_times(inital)
    assert not seen_counter.has_been_seen_n_times(inital)
    assert seen_counter.has_been_seen_n_times(inital)

    assert not seen_counter.has_been_seen_n_times(new)
    assert not seen_counter.has_been_seen_n_times(new)
    assert seen_counter.has_been_seen_n_times(new)
