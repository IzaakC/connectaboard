import chess


def attacking_squares_for_piece_at(
    piece: chess.Piece, square: chess.Square
) -> list[chess.Square]:
    """
    Get a list of squares a piece can move to on an otherwise empty board.

    Args:
        piece (chess.Piece): The piece whose moves we want to calculate.
        square (chess.Square): The square where the piece is located.

    Returns:
        list[chess.Square]: A list of squares the piece can move to.
    """
    # Create an empty board
    board = chess.Board()
    board.clear_board()

    # Place the piece on the given square
    board.set_piece_at(square, piece)

    # Get all squares the piece can attack (valid moves)
    return list(board.attacks(square))


def get_rook_move_for_castling(king_move: chess.Move) -> chess.Move:
    """Calculate the rook's move for castling based on the king's move."""

    if king_move.from_square == chess.E1:
        if king_move.to_square == chess.G1:  # Kingside castling
            return chess.Move(chess.H1, chess.F1)
        elif king_move.to_square == chess.C1:  # Queenside castling
            return chess.Move(chess.A1, chess.D1)
    elif king_move.from_square == chess.E8:
        if king_move.to_square == chess.G8:  # Kingside castling
            return chess.Move(chess.H8, chess.F8)
        elif king_move.to_square == chess.C8:  # Queenside castling
            return chess.Move(chess.A8, chess.D8)

    raise ValueError(f"The given move is not a castling move. ({king_move})")
