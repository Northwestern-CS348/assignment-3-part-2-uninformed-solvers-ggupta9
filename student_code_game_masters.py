from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg_1 = []
        peg_2 = []
        peg_3 = []

        for i in self.kb.facts:
            if i.statement.predicate == 'on':
                disk = i.statement.terms[0].term.element
                n = int(disk[-1:])
                if i.statement.terms[1].term.element == 'peg1':
                    peg_1.append(n)
                elif i.statement.terms[1].term.element == 'peg2':
                    peg_2.append(n)
                elif i.statement.terms[1].term.element == 'peg3':
                    peg_3.append(n)

        peg_1.sort()
        peg_1 = tuple(peg_1)
        peg_2.sort()
        peg_2 = tuple(peg_2)
        peg_3.sort()
        peg_3 = tuple(peg_3)

        return (peg_1,peg_2,peg_3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement): #if move is legal

            peg_1 = movable_statement.terms[1].term.element
            peg_2 = movable_statement.terms[2].term.element
            disk = movable_statement.terms[0].term.element
            disks_below = parse_input('fact: (ontopof ' + disk + ' ?x)')
            bindings_list = self.kb.kb_ask(disks_below)
            curr_top = parse_input('fact: (top ?x ' + peg_2 + ')')
            old_fact = parse_input('fact: (on ' + disk + ' ' + peg_1 + ')')
            new_fact = parse_input('fact: (on ' + disk + ' ' + peg_2 + ')')
            bindings_list_2 = self.kb.kb_ask(curr_top)
            self.kb.kb_retract(old_fact)
            self.kb.kb_assert(new_fact)
            old_empty = parse_input('fact: (empty ' + peg_2 + ')')
            new_empty = parse_input('fact: (empty ' + peg_1 + ')')
            empty_list = parse_input('fact: (on ?x ' + peg_1 + ')')
            bindings_list_3 = self.kb.kb_ask(empty_list)
            self.kb.kb_retract(old_empty)

            if not bindings_list_3: #if not empty
                self.kb.kb_assert(new_empty)

            if bindings_list_2: #if on top
                curr_top_disk = bindings_list_2[0].bindings[0].constant.element
                peg_top = parse_input('fact: (top ' + curr_top_disk + ' ' + peg_2 + ')')
                self.kb.kb_retract(peg_top)

            moved_disk = parse_input('fact: (top ' + disk + ' ' + peg_1 + ')')
            move_top = parse_input('fact: (top ' + disk + ' ' + peg_2 + ')')
            self.kb.kb_retract(moved_disk)
            self.kb.kb_assert(move_top)

            if bindings_list: #if in between
                disks_below = []

                for i in bindings_list:
                    disks_below.append(i.bindings[0].constant.element)
                small_disk = disks_below[0]

                for i in disks_below:
                    smaller_disks = parse_input('fact: (smaller ' + small_disk + ' ' + i + ')')
                    bindings_list_2 = self.kb.kb_ask(smaller_disks)

                    if not bindings_list_2:
                        small_disk = i

                new_top = parse_input('fact: (top ' + small_disk + ' ' + peg_1 + ')')
                self.kb.kb_assert(new_top)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row_1 = [0,0,0]
        row_2 = [0,0,0]
        row_3 = [0,0,0]

        for i in self.kb.facts:
            if i.statement.predicate == 'pos':
                curr_tile = i.statement.terms[0].term.element
                n = curr_tile[-1:]
                if n == 'y':
                    n = -1
                else:
                    n = int(n)
                col_list = i.statement.terms[1].term.element
                column = int(col_list[-1:])
                if i.statement.terms[2].term.element == 'pos1':
                    row_1[column-1] = n
                elif i.statement.terms[2].term.element == 'pos2':
                    row_2[column - 1] = n
                elif i.statement.terms[2].term.element == 'pos3':
                    row_3[column - 1] = n

        row_1 = tuple(row_1)
        row_2 = tuple(row_2)
        row_3 = tuple(row_3)

        return (row_1, row_2, row_3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement): #if move is legal

            #tile and coordinate initialization
            curr_tile = movable_statement.terms[0].term.element
            column_1 = movable_statement.terms[1].term.element
            row_1 = movable_statement.terms[2].term.element
            column_2 = movable_statement.terms[3].term.element
            row_2 = movable_statement.terms[4].term.element
            #fact perusal
            old_fact_1 = parse_input('fact: (pos empty ' + column_2 + ' ' + row_2 + ')')
            old_fact_2 = parse_input('fact: (pos ' + curr_tile + ' ' + column_1 + ' ' + row_1 + ')')
            new_fact_1 = parse_input('fact: (pos empty ' + column_1 + ' ' + row_1 + ')')
            new_fact_2 = parse_input('fact: (pos ' + curr_tile + ' ' + column_2 + ' ' + row_2 + ')')
            #assertions
            self.kb.kb_retract(old_fact_1)
            self.kb.kb_retract(old_fact_2)
            self.kb.kb_assert(new_fact_1)
            self.kb.kb_assert(new_fact_2)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
