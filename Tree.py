import math
from math import sqrt
from typing import Union
import chess
from numpy import log as ln
import uuid


class MCTree:
    def __init__(
        self,
        board: Union[None,chess.Board] = None,
        move: Union[None,chess.Move] = None,
        totalValue: Union[None,float] = None,
        visits: Union[None,int] = None,
        parent: Union[None, "MCTree"] = None,
        children: Union[None,list['MCTree']] = None,
        selectionConstant: Union[None, float] = None
    ):
        self.id = uuid.uuid4()
        if (totalValue == None):
            self.totalValue = 0
        else:
            self.totalValue = totalValue
        if (visits == None):
            self.visits = 0
        else:
            self.visits = visits
        if parent == None:
            self.parent = None
        else:
            self.parent = parent
        if children == None:
            self.children = []
        else:
            self.children = children
        if selectionConstant == None:
            self.selectionConstant = 2
        else:
            self.selectionConstant = selectionConstant
        if board == None:
            self.board = chess.Board()
        else:
            self.board = board
        if move == None:
            self.move = None
        else:
            self.move = move

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
                visits=0,
                move=move
            ))

    def maxChild(self):
        max = self.children[0]
        for child in self.children:
            if child.totalValue > max.totalValue:
                max = child
        return max

    def __repr__(self, level = 0) -> str:
        ret =  '\t' * level
        if self.move:
            ret += self.move.uci() 
        ret +="\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

