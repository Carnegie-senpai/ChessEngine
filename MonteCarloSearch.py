from Tree import MCTree
import chess
from random import randrange


def playRandomGame(board: chess.Board):
    boardCopy = chess.Board(board.fen())
    itr = 0
    while not boardCopy.is_game_over() and not itr > 300:
        itr += 1
        legalMoves = []
        for i in boardCopy.generate_legal_moves():
            legalMoves.append(i.uci())
        boardCopy.push_uci(legalMoves[randrange(0, len(legalMoves))])
    return boardCopy.outcome()


def MonteCarloIteration(tree: MCTree):
    # Selection Phase
    selection = tree.getBestChild()

    # Expansion Phase
    selection.expand()
    # Simulation Phase
    toPlay = selection.children[randrange(0, len(selection.children))]
    result = playRandomGame(toPlay.board)
    # Backpropogation Phase
    toPlay.backPropogate(randrange(0,100))


def MonteCarloSearch(board: chess.Board, limit: int):
    """Finds the best move for a given board position using montecarlo tree search.
    Does not affect the board state
    """
    itr = 0
    boardCopy = chess.Board(board.fen())
    while itr < limit:
        itr += 1
        MonteCarloIteration(MCTree(boardCopy))


if __name__ == "__main__":
    board = chess.Board()
    # while not board.is_game_over():
    move = MonteCarloSearch(board,100)
