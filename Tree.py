import math
from math import sqrt
from typing import Union
import chess
from numpy import log as ln
import uuid


class MCTree:
    def __init__(
        self,
        board: chess.Board = chess.Board(),
        totalValue: float = 0,
        visits: int = 0,
        parent: Union[None, "MCTree"] = None,
        children: list['MCTree'] = [],
        selectionConstant: float = 2
    ):
        self.id = uuid.uuid4()
        self.totalValue = totalValue
        self.visits = visits
        self.parent = parent
        self.children = children
        self.selectionConstant = selectionConstant
        self.board = board

    def avg(self) -> float:
        return self.totalValue/self.visits

    def ucb(self) -> float:
        if self.visits == 0:
            return math.inf
        if self.parent == None:
            parentVisits = 0
        else:
            parentVisits = self.parent.visits
        return self.avg() + self.selectionConstant * sqrt(ln(parentVisits)/self.visits)

    def getBestChild(self, recurse=0) -> 'MCTree':
        """Recursively returns the best child MCTree according to the ucb formula
        """
        # base case which stops recursion
        if (recurse > 10):
            return self
        if (self.isLeaf()):
            return self

        if (len(self.children) == 1):
            return self.children[0].getBestChild(recurse+1)

        bestChild = self.children[0]
        bestChildUCB = bestChild.ucb()
        for child in self.children[1:]:
            childUCB = child.ucb()
            if childUCB > bestChildUCB:
                bestChild = child
                bestChildUCB = childUCB
        return bestChild.getBestChild(recurse+1)

    def isLeaf(self) -> bool:
        return len(self.children) == 0

    def isRoot(self) -> bool:
        return self.parent == None

    def backPropogate(self, simulationResult: float):
        """Backpropogates the result of a simulation to all parent nodes
        """
        self.totalValue += simulationResult
        self.visits += 1
        parent = self.parent

        while (parent != None):
            parent.totalValue += self.totalValue
            parent.visits += self.visits
            parent = parent.parent

    def expand(self):
        """Expands children to be all legal moves from this board position
        """
        if self.children != []:
            raise Exception("Cannot expand non-leaf node")

        for move in self.board.generate_legal_moves():
            boardCopy = chess.Board(self.board.fen())
            boardCopy.push_uci(move.uci())
            self.children.append(MCTree(
                board=boardCopy,
                parent=self,
                selectionConstant=self.selectionConstant,
                children=[],
                totalValue=0,
                visits=0
            ))
