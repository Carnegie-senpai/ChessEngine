import chess
import chess.svg

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class ChessBoard(QWidget):
    def __init__(self, boardstate: str = "", svg: str = ""):
        super().__init__()
        self.setGeometry(100, 100, 1100, 1100)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)

        if boardstate:
            self.board = chess.Board(boardstate)
        else:
            self.board = chess.Board()

        if (svg == ""):
            self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
        else:
            self.chessboardSvg = svg.encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
    
    def push_uci(self,uci:str):
        self.board.push_uci(uci)
        self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        self.update()
    

if __name__ == "__main__":
    app = QApplication([])
    chessBoard = ChessBoard()
    chessBoard.show()
    app.exec()
