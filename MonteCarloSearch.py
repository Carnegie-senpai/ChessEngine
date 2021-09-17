from Tree import MCTree
import chess
from random import randrange
import ChessBoard
from PyQt5.QtWidgets import QApplication
from typing import Union


def playRandomGame(board: chess.Board):
    boardCopy = chess.Board(board.fen())
    itr = 0
    while not boardCopy.is_game_over() and not itr > 300:
        itr += 1
        legalMoves = []
        for i in boardCopy.generate_legal_moves():
            legalMoves.append(i.uci())
        boardCopy.push_uci(legalMoves[randrange(0, len(legalMoves))])
    return boardCopy.outcome(), boardCopy


def MonteCarloIteration(tree: MCTree, color: bool):
    # Selection Phase
    selection = tree.getBestChild()

    # Expansion Phase
    selection.expand()
    # Simulation Phase
    toPlay = selection.children[randrange(0, len(selection.children))]
    result, temp = playRandomGame(toPlay.board)
    score = 1
    if result and result.winner == color:
        score = 10
    if result and result.winner == None:
        score = 5


    # Backpropogation Phase
    toPlay.backPropogate(score)


def MonteCarloSearch(board: chess.Board, limit: int, color: bool = True):
    """Finds the best move for a given board position using montecarlo tree search.
    Does not affect the board state
    color == True == white
    color == False == black
    """
    itr = 0
    boardCopy = chess.Board(board.fen())
    while itr < limit:
        itr += 1
        MonteCarloIteration(MCTree(boardCopy), color)


if __name__ == "__main__":
    board = chess.Board()
    # while not board.is_game_over():
    app = QApplication([])
    cb = ChessBoard.ChessBoard()
    cb.show()
    move = MonteCarloSearch(board, 100)
    app.exec()
