
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.stack = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition:
            return True

        possible_moves = self.gm.getMovables()

        if len(self.currentState.children) == 0: #no more moves in stack
            for i in possible_moves:
                self.gm.makeMove(i)
                updated_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, i)
                if updated_state not in self.visited.keys():
                    self.visited[updated_state] = False
                updated_state.parent = self.currentState
                self.currentState.children.append(updated_state)
                self.gm.reverseMove(i)

        for i in self.currentState.children[::-1]: #peruse stack (FILO)
            if self.visited[i] == False:
                self.stack.appendleft(i)

        new_state = self.stack.popleft()
        moves = new_state.requiredMovable

        while self.currentState.nextChildToVisit == len(self.currentState.children):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState == self.currentState.parent

        new_state.parent.nextChildToVisit += 1
        self.gm.makeMove(moves)
        self.currentState = new_state

        if self.currentState.state == self.victoryCondition: #check if reached goal
            return True

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition:
            return True

        possible_moves = self.gm.getMovables()

        if len(self.currentState.children) == 0: #no more moves in queue
            for i in possible_moves:
                self.gm.makeMove(i)
                updated_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, i)
                if updated_state not in self.visited.keys():
                    self.visited[updated_state] = False
                    updated_state.parent = self.currentState
                    self.currentState.children.append(updated_state)
                self.gm.reverseMove(i)

        for i in self.currentState.children: #step through queue (FIFO)
            if self.visited[i] == False:
                self.queue.append(i)

        new_state = self.queue.popleft()
        moves = new_state.requiredMovable
        backwards_moves = deque()

        if new_state.depth == self.currentState.depth:
            curr_state = new_state
        else:
            curr_state = new_state.parent
            backwards_moves.appendleft(moves)

        while self.currentState != curr_state: #move backwards in queue
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            backwards_moves.appendleft(curr_state.requiredMovable)
            curr_state = curr_state.parent

        for i in backwards_moves:
            self.gm.makeMove(i)

        self.currentState = new_state

        if self.currentState.state == self.victoryCondition: #check if reached goal
            return True

        return False
