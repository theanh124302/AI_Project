import AI.Score
import random

CHECKMATE = 1000
STALEMATE = 0


def findBestMove(game_state, valid_moves, return_queue, DEPTH):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    alpha = -CHECKMATE
    beta = CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -PVS(game_state, next_moves, DEPTH - 1, -beta, -alpha, 1 if game_state.white_to_move else -1)
        game_state.undoMove()
        if score > alpha:
            alpha = score
            next_move = move
    return_queue.put(next_move)


def PVS(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    if depth == 0:
        return turn_multiplier * AI.Score.scoreBoard(game_state)
    if depth <0:
        return
    max_score = -CHECKMATE
    for i, move in enumerate(valid_moves):
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()

        if i == 0:
            score = -PVS(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        else:
            score = -PVS(game_state, next_moves, depth - 1, -alpha - 1, -alpha, -turn_multiplier)
            if alpha < score < beta:
                score = -PVS(game_state, next_moves, depth - 1, -beta, -score, -turn_multiplier)

        game_state.undoMove()

        if score > max_score:
            max_score = score

        if score > alpha:
            alpha = score

        if alpha >= beta:
            break

    return max_score
