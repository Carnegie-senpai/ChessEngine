import chess
from GUI import BoardDisplay
from random import randrange
from PyQt5.QtWidgets import QApplication

board = chess.Board()
print(board.board_fen())

print(board.can_claim_draw())
print(board.can_claim_fifty_moves())
print(board.can_claim_threefold_repetition())

itr = 0
while not board.is_checkmate() and not board.can_claim_draw() and not itr > 1000:
    itr+=1
    legalMoves=[]
    for i in board.generate_legal_moves():
        legalMoves.append(i.uci())
    board.push_uci(legalMoves[randrange(0, len(legalMoves))])

print(board)
print("itrations to completion",itr)
app=QApplication([])
window=BoardDisplay(boardstate = board.board_fen())
window.show()
app.exec()
