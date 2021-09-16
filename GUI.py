import chess
import chess.svg

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class BoardDisplay(QWidget):
    def __init__(self, boardstate: str = "", svg: str = ""):
        super().__init__()
        self.setGeometry(100, 100, 1100, 1100)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)
        if (svg == ""):
            if (boardstate != ""):
                self.chessboard = chess.Board(boardstate)
            else:
                self.chessboard = chess.Board()
            self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        else:
            self.chessboardSvg = svg.encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


if __name__ == "__main__":
    app = QApplication([])
    window = BoardDisplay()
    window.show()
    app.exec()
