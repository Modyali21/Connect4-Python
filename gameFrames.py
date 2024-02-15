import tkinter as tk
from tkinter.font import Font
from Prouning import minMaxWithProuning
from State import State
from heuristic import eval_score_four_consecutive
from methods import minMax
from mybutton import MyButton
from constant import *


class Connect4(tk.Canvas):
    def __init__(
        self,
        master,
        rowSize: int = 7,
        columnSize: int = 6,
        holeSize: int = 50,
        padx: int = 10,
        pady: int = 10,
        background: str = "blue",
        emptyHole: str = "white",
        player1: str = "red",
        player2: str = "yellow",
    ):
        super().__init__(
            master=master,
            background=background,
            highlightthickness=0,
            bd=0,
            width=((rowSize * holeSize) + (rowSize + 1) * padx),
            height=((columnSize * holeSize) + (columnSize + 1) * pady),
        )

        self.drawnState = []
        self.player1 = player1
        self.player2 = player2

        for i in range(rowSize):
            self.drawnState.append([])
            for j in range(columnSize):
                tmp = self.create_oval(
                    padx * (i + 1) + i * holeSize,
                    pady * (j + 1) + j * holeSize,
                    padx * (i + 1) + (i + 1) * holeSize,
                    pady * (j + 1) + (j + 1) * holeSize,
                    fill=emptyHole,
                    width=0,
                )
                self.drawnState[i].append(tmp)

    def makeAction(self, row: int, column: int, isPlayer1: bool):
        color = self.player1 if isPlayer1 else self.player2
        self.itemconfig(self.drawnState[column][row], fill=color)


class GameFrame(tk.Frame):
    connect4: Connect4
    buttons: list[MyButton]
    buttonsFrame: tk.Frame
    holeSize: int
    padx: int
    pady: int
    topEffect: tk.Canvas
    player1: str
    scoreFrame: tk.Frame
    font: Font
    backButton: MyButton
    previousFrame: tk.Frame
    state: State
    winner: tk.Label

    def __init__(
        self,
        master,
        previousFrame: tk.Frame = None,
        background: str = "#DDEBE6",
        outerPadx: int = 10,
        outerPady: int = 10,
        rowSize: int = 7,
        columnSize: int = 6,
        holeSize: int = 50,
        padx: int = 10,
        pady: int = 10,
        emptyHole: str = "#DDEBE6",
        player1: str = "#fc7e68",
        player2: str = "#254689",
        gameBackground: str = "#5f9ea0",
        withProning: bool = False,
        maxDepth: int = 3,
    ):
        super().__init__(
            master=master, background=background, padx=outerPadx, pady=outerPady
        )
        self.previousFrame = previousFrame
        self.holeSize = holeSize
        self.padx = padx
        self.pady = pady
        self.player1 = player1
        self.font = Font(family="Yu Gothic UI Semibold", size=20, weight="bold")
        self.state = State(
            [
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
            ]
        )
        self.withProning = withProning
        self.maxDepth = maxDepth

        if withProning:
            self.method = minMaxWithProuning
        else:
            self.method = minMax

        self.connect4 = Connect4(
            master=self,
            rowSize=rowSize,
            columnSize=columnSize,
            holeSize=holeSize,
            padx=padx,
            pady=pady,
            emptyHole=emptyHole,
            player1=player1,
            player2=player2,
            background=gameBackground,
        )

        self.topEffect = tk.Canvas(
            self,
            background=background,
            width=self.connect4["width"],
            height=holeSize + pady,
            highlightthickness=0,
            bd=0,
        )

        self.buttonsFrame = tk.Frame(self, background=background, padx=padx // 2)
        self.buttons = []
        self.scoreFrame = tk.Frame(self, background=background)

        self.playerLabel = tk.Label(
            self.scoreFrame,
            background=background,
            text="Player score: 0",
            foreground=gameBackground,
            font=self.font,
        )

        self.computerLabel = tk.Label(
            self.scoreFrame,
            background=background,
            text="Computer score: 0",
            foreground=gameBackground,
            font=self.font,
        )

        for i in range(rowSize):
            tmp = MyButton(
                self.buttonsFrame,
                width=holeSize,
                height=holeSize,
                txt=str(i),
                font=self.font,
                buttonColor=background,
                hover=True,
                enterCommand=lambda col=i: self.hover(col),
                leaveCommand=self.leave,
                command=lambda col=i: self.action(col),
                hoverStyle={"textColor": player1},
            )
            tmp.pack(padx=padx // 2, anchor="center", side="left")
            self.buttons.append(tmp)

        self.backButton = MyButton(
            self,
            font=self.font,
            txt="\u276E",
            buttonColor=gameBackground,
            textColor=background,
            width=60,
            height=60,
            cornerRadius=20,
            hover=True,
            command=self.goBack,
            enterCommand=lambda: self.backButton.setText("\u276E go back"),
            leaveCommand=lambda: self.backButton.setText("\u276E"),
            padx=10,
            pady=10,
        )

        self.winner = tk.Label(
            self,
            background=background,
            text="",
            foreground=gameBackground,
            font=self.font,
        )

        self.backButton.pack(anchor="w")
        self.playerLabel.pack(anchor="w")
        self.computerLabel.pack(anchor="w")
        self.scoreFrame.pack(anchor="w", pady=10)
        self.topEffect.pack()
        self.connect4.pack()
        self.buttonsFrame.pack(anchor="center")

    def action(self, column):
        row = self.state.addToColumn(column, PLAYER)
        if row < 0:
            print("error")
        else:
            self.connect4.makeAction(row, column, True)
            self.updateScore()
            self.leave()
            self.disable()
            self.update()
            if not self.state.isTerminalState():
                self.aiTurn()
            else:
                print("finished")
                self.announceWinner()

    def updateScore(self):
        player = eval_score_four_consecutive(self.state.state_board, PLAYER)
        computer = eval_score_four_consecutive(self.state.state_board, AI)
        self.playerLabel.config(text="Player score: " + str(player))
        self.computerLabel.config(text="Computer score: " + str(computer))

    def announceWinner(self):
        self.buttonsFrame.destroy()
        player = eval_score_four_consecutive(self.state.state_board, PLAYER)
        computer = eval_score_four_consecutive(self.state.state_board, AI)
        if player > computer:
            self.winner.configure(text="winner is player")
            self.winner.pack()
        elif player < computer:
            self.winner.configure(text="winner is computer")
            self.winner.pack()
        else:
            self.winner.configure(text="it is a tie")
            self.winner.pack()

    def aiTurn(self):
        self.state = self.method(self.state, self.maxDepth, AI)[1]
        row, col = self.state.generatingAction
        self.connect4.makeAction(row, col, False)
        self.updateScore()
        if not self.state.isTerminalState():
            self.enable()
        else:
            print("finished")
            self.announceWinner()

    def hover(self, i):
        startx = self.padx * (i + 1) + i * self.holeSize
        self.save = self.topEffect.create_oval(
            startx,
            0,
            startx + self.holeSize,
            self.holeSize,
            width=0,
            fill=self.player1,
            tags="toDelete",
        )

    def leave(self):
        for i in self.topEffect.find_withtag("toDelete"):
            self.topEffect.delete(i)

    def disable(self):
        for button in self.buttons:
            button.disable()

    def enable(self):
        for button in self.buttons:
            button.enable()

    def goBack(self):
        if self.previousFrame is not None:
            self.destroy()
            self.previousFrame.pack(fill="both", expand=True, anchor="center")
            self.master.update()


if __name__ == "__main__":
    x = tk.Tk()
    x.title("AI assignment 2")
    x.config(background="#DDEBE6")
    GameFrame(x).pack(anchor="center", expand=False)
    x.update()
    x.minsize(width=x.winfo_width(), height=x.winfo_height())
    x.mainloop()
