import chess
from ChessBoard import ChessBoard
from random import randrange
from PyQt5.QtWidgets import QApplication
itr = 0
app = QApplication([])
chessBoard = ChessBoard()
chessBoard.show()

    
while not chessBoard.board.is_checkmate() and not chessBoard.board.can_claim_draw() and not itr > 1000:
    itr += 1
    legalMoves = []
    for i in chessBoard.board.generate_legal_moves():
        legalMoves.append(i.uci())
    chessBoard.push_uci(legalMoves[randrange(0, len(legalMoves))])

print(chessBoard.board.fen())
app.exec()
