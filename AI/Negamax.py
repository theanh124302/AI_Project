import AI.Score
import random

CHECKMATE = 1000
STALEMATE = 0
def findBestMove(game_state, valid_moves, return_queue, DEPTH):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, DEPTH, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * AI.Score.scoreBoard(game_state)
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, DEPTH, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score
