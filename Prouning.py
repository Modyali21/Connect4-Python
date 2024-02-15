from heuristic import heuristic
from constant import *
from State import State
import random
import copy


def minMaxWithProuning(
    state: State, maxDepth, turn, alpha=float("-inf"), beta=float("inf")
):
    newState = copy.deepcopy(state)
    if maxDepth == 0 or state.isTerminalState():
        return heuristic(newState), newState
    return (
        MinWithProuning(newState, alpha, beta, maxDepth)
        if turn == AI
        else MaxWithProuning(newState, alpha, beta, maxDepth)
    )


def MaxWithProuning(state: State, alpha, beta, depth):
    v = float("-inf")
    n: State = []
    state.getActions(AI)
    for neighbour in state.children:
        vDash = minMaxWithProuning(neighbour, depth - 1, AI, alpha, beta)[0]
        if vDash > v:
            v = vDash
            n = neighbour
        if vDash >= beta:
            return v, neighbour
        alpha = max(alpha, vDash)
    return v, n


def MinWithProuning(state: State, alpha, beta, depth):
    v = float("inf")
    n: State = []
    state.getActions(PLAYER)
    for neighbour in state.children:
        vDash = minMaxWithProuning(neighbour, depth - 1, PLAYER, alpha, beta)[0]
        if vDash < v:
            v = vDash
            n = neighbour
        if vDash <= alpha:
            return v, neighbour
        beta = min(beta, vDash)
    return v, n
