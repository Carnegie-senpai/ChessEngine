import chess

board = chess.Board()
print(board.board_fen())

print(board.can_claim_draw())
print(board.can_claim_fifty_moves())
print(board.can_claim_threefold_repetition())

for i in board.generate_legal_moves():
    print(i)

print(board)