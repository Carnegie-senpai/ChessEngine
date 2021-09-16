import math
from math import sqrt
from typing import Union

from numpy import log as ln


class MCTree:
    def __init__(
        self,
        fenData: str,
        totalValue: float = 0,
        visits: int = 0,
        parent: Union[None, "MCTree"] = None,
        children: list['MCTree'] = [],
        selectionConstant: float = 2
    ):
        self.totalValue = totalValue
        self.visits = visits
        self.parent = parent
        self.children = children
        self.selectionConstant = selectionConstant
        self.fenData = fenData

    def avg(self) -> float:
        return self.totalValue/self.visits

    def ucb(self) -> float:
        if self.visits == 0:
            return math.inf
        return self.avg() + self.selectionConstant * sqrt(ln(self.parent.visits)/self.visits)

    def getBestChild(self) -> 'MCTree':
        """Recursively returns the best child MCTree according to the ucb formula
        """
        # base case which stops recursion
        if (self.isLeaf()):
            return self

        if (len(self.children) == 1):
            return self.children[0].getBestChild()

        bestChild = self.children[0]
        bestChildUCB = bestChild.ucb()
        for child in self.children[1:]:
            childUCB = child.ucb()
            if childUCB > bestChildUCB:
                bestChild = child
                bestChildUCB = childUCB
        return bestChild.getBestChild()

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
