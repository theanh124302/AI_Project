import random
import math
import AI.Score
import numpy as np

CHECKMATE = 1000
STALEMATE = 0

class Node:
    def __init__(self, game_state, move=None, parent=None):
        self.game_state = game_state
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

def findBestMove(game_state, return_queue, simulations):
    root = Node(game_state)
    for i in range(simulations):
        selected_node = selectNode(root)
        expanded_node = expandNode(selected_node)
        simulation_result = simulate(expanded_node)
        backpropagate(expanded_node, simulation_result)
    best_move = getBestMove(root)
    return_queue.put(best_move)

def selectNode(node):
    while node.children:
        if not all(child.visits for child in node.children):
            return expandNode(node)
        node = getBestUCB(node.children)
    return node

def expandNode(node):
    unvisited_moves = [move for move in node.game_state.getValidMoves() if move not in [child.move for child in node.children]]
    if unvisited_moves:
        move = random.choice(unvisited_moves)
        node.game_state.makeMove(move)
        game_state = node.game_state
        child_node = Node(game_state, move, node)
        node.children.append(child_node)
        return child_node
    return node

def simulate(node):
    game_state = node.game_state
    valid_moves = game_state.getValidMoves()
    depth = 0
    while valid_moves and depth < 100:  # Maximum simulation depth
        random_move = random.choice(valid_moves)
        game_state.makeMove(random_move)
        valid_moves = game_state.getValidMoves()
        depth += 1
    return AI.Score.scoreBoard(game_state)

def backpropagate(node, score):
    while node:
        node.visits += 1
        node.score += score
        node = node.parent

def getBestUCB(children):
    visits = np.array([child.visits for child in children])
    scores = np.array([child.score for child in children])
    exploitation = scores / visits
    exploration = np.sqrt(np.log(np.sum(visits)) / visits)
    ucb = exploitation + exploration
    best_child_idx = np.argmax(ucb)
    return children[best_child_idx]

def getBestMove(node):
    best_score = float('-inf')
    best_move = None
    for child in node.children:
        score = child.score / child.visits
        if score > best_score:
            best_score = score
            best_move = child.move
    return best_move
