import copy
from constant import *
from termcolor import colored

class State:
    def __init__(
        self,
        board,
        rows=6,
        cols=7,
        score=0,
        generatingAction=(-1, -1),
        movesNumber: int = 0,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.score = score
        self.state_board = board
        self.children: list[State] = []
        self.generatingAction: tuple[int, int] = generatingAction
        self.movesNumber: int = movesNumber

    def display(self):
        for row in self.state_board:
            print(row)

    def addToColumn(self, column, player):
        if 0 <= column < self.cols:
            for row in range(self.rows - 1, -1, -1):
                if self.state_board[row][column] == "-":
                    self.state_board[row][column] = player
                    self.movesNumber += 1
                    return row
            return -1
        else:
            return -1

    def get_pieces_in_each_column(self):
        pieces_in_each_column = [0] * self.cols

        for col in range(self.cols):
            for row in range(self.rows):
                if self.state_board[row][col] != "-":
                    pieces_in_each_column[col] += 1

        return pieces_in_each_column

    def getActions(self, turn):
        elements_in_cols = self.get_pieces_in_each_column()
        for col in range(7):
            for row in range(self.rows - 1, -1, -1):
                if (elements_in_cols[col] < 6) and (self.state_board[row][col] == "-"):
                    child_board = [row[:] for row in self.state_board]
                    child_board[row][col] = self.getOpponent(turn)
                    child_state = State(
                        child_board,
                        generatingAction=(row, col),
                        movesNumber=self.movesNumber + 1,
                    )
                    self.children.append(child_state)
                    break

    def getOpponent(self, player):
        return AI if player == PLAYER else PLAYER

    def isTerminalState(self) -> bool:
        return self.movesNumber == self.rows * self.cols
    @property
    def print2DArray(self):
        result_string = '\n'.join(', '.join(map(str, row)) for row in self.state_board)
        return result_string

    def generateTree(self,height,turn,file,depth=0):
        try :
            for row in self.state_board :
                r = '   '*depth**2 + ' '.join(row)+"\n"
                # print(r)
                file.write(r)
            file.write("\n")
            self.getActions(turn)
            if(depth<height) :
                for child in self.children :
                    child.generateTree(height,self.getOpponent(turn),file,depth+1)
        except Exception:
            print("error")
        