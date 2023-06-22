import AI.Score
import random

CHECKMATE = 1000
STALEMATE = 0

def findBestMove(game_state, valid_moves, return_queue, DEPTH):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveMinMax(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, DEPTH, game_state.white_to_move)
    return_queue.put(next_move)
def findMoveMinMax(game_state, valid_moves, depth, alpha, beta, DEPTH, white_to_move):
    global next_move
    if depth == 0:
        return AI.Score.scoreBoard(game_state)
    if white_to_move:
        maxScore = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, alpha, beta, DEPTH, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
            alpha = max(alpha, maxScore)
            if alpha >= beta:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, alpha, beta, DEPTH, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
            beta = min(beta, minScore)
            if alpha >= beta:
                break
        return minScore
