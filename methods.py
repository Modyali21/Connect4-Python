from heuristic import heuristic
from State import State
from constant import *
import copy


def minMax(state: State, maxDepth: int, turn: str):
    newState = copy.deepcopy(state)
    if maxDepth == 0 or newState.isTerminalState():
        return heuristic(newState), newState
    return min_minMax(newState, maxDepth) if turn == AI else max_minMax(newState, maxDepth)


def min_minMax(state: State, maxDepth: int):
    value = float("inf")
    n: State = None
    state.getActions(PLAYER)
    for child in state.children:
        v = min(value, minMax(child, maxDepth - 1, PLAYER)[0])
        if v < value:
            value = v
            n = child
    return value, n


def max_minMax(state: State, maxDepth: int):
    value = float("-inf")
    n: State = None
    state.getActions(AI)
    for child in state.children:
        v = max(value, minMax(child, maxDepth - 1, AI)[0])
        if v > value:
            value = v
            n = child
    return value, n



state = State([
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
            ])
f = open('output.txt', 'w')
state.generateTree(3,PLAYER,f)
f.close()



