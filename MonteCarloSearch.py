from dataclasses import is_dataclass
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


def MonteCarloIteration(tree: MCTree, color: chess.Color):
    """Modifies the tree that it is passed
    """
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


def MonteCarloSearch(board: chess.Board, limit: int, color: chess.Color = chess.WHITE):
    """Finds the best move for a given board position using montecarlo tree search.
    Does not affect the board state
    color == True == white
    color == False == black
    """
    itr = 0
    boardCopy = chess.Board(board.fen())
    tree = MCTree(boardCopy)
    print("Start Tree \n",tree)
    while itr < limit:
        itr += 1
        MonteCarloIteration(tree, color)
    print("Tree: \n",tree)
    return tree.maxChild().move


if __name__ == "__main__":
    board = chess.Board()
    # while not board.is_game_over():
    try:
        itr = 0
        while (not board.is_game_over() and itr < 5):
            print("Turn: ",board.turn)
            move = MonteCarloSearch(board, 10, board.turn)
            if (move != None):
                if (not board.is_legal(move)):
                    raise Exception("ILLEGAL MOVE")
                board.push(move)
            print(itr)
            itr+=1
    except Exception as e:
        print("Error running game: ", e)
    app = QApplication([])
    cb = ChessBoard.ChessBoard(board.fen())
    cb.show()
    app.exec()
