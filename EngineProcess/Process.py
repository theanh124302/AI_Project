import pygame as p
import EngineProcess.Engine
import AI.Negamax
import AI.MiniMax
import AI.Score
import AI.Random
import AI.MCTS
import AI.PVS
import time
import sys
from multiprocessing import Process, Queue

class ChessGame:
    def __init__(self):
        self.BOARD_WIDTH = 512
        self.BOARD_HEIGHT = 512
        self.MOVE_LOG_PANEL_WIDTH = 250
        self.MOVE_LOG_PANEL_HEIGHT = self.BOARD_HEIGHT
        self.DIMENSION = 8
        self.SQUARE_SIZE = self.BOARD_HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.level = 0
        self.algorithm = 1

    def main(self):
        self.level = 2
        p.init()
        screen = p.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        screen.fill(p.Color("white"))
        game_state = EngineProcess.Engine.GameState()
        valid_moves = game_state.getValidMoves()
        move_made = False  # flag variable for when a move is made
        self.loadImages()  # do this only once before while loop
        running = True
        square_selected = ()
        player_clicks = []
        game_over = False
        ai_thinking = False
        move_undone = False
        move_finder_process = None
        player_one = True
        player_two = False
        while running:
            human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if e.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos()
                        col = location[0] // self.SQUARE_SIZE
                        row = location[1] // self.SQUARE_SIZE
                        if square_selected == (row, col):
                            square_selected = ()
                            player_clicks = []
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)
                        if len(player_clicks) == 2 and human_turn:
                            move = EngineProcess.Engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    square_selected = ()
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]

                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        game_state.undoMove()
                        move_made = True
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:
                        game_state = EngineProcess.Engine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_0:
                        if not ai_thinking:
                            self.level = 0
                            print("Random move")
                    if e.key == p.K_1:
                        if not ai_thinking:
                            self.level = 1
                            print("Easy")
                    if e.key == p.K_2:
                        if not ai_thinking:
                            self.level = 2
                            print("Medium")
                    if e.key == p.K_3:
                        if not ai_thinking:
                            self.level = 3
                            print("Hard")
                    if e.key == p.K_4:
                        if not ai_thinking:
                            self.level = 4
                            print("Very hard")
                    if e.key == p.K_5:
                        if not ai_thinking:
                            self.level = 5
                            print("Master")
                    if e.key == p.K_m:
                        if not ai_thinking:
                            self.algorithm = 1
                            print("Minimax")
                    if e.key == p.K_n:
                        if not ai_thinking:
                            self.algorithm = 2
                            print("Negamax")
                    if e.key == p.K_c:
                        if not ai_thinking:
                            self.algorithm = 3
                            print("Monte Carlo Tree Search")
                    # if e.key == p.K_p:
                    #     if not ai_thinking:
                    #         self.algorithm = 4
                    #         print("Principal Variation Search")
                    if e.key == p.K_a:
                        if not ai_thinking:
                            if self.algorithm == 1:
                                print("Minimax")
                            if self.algorithm == 2:
                                print("Negamax")
                            if self.algorithm == 3:
                                print("Monte Carlo Tree Search")
                            if self.algorithm == 4:
                                print("Principal Variation Search")
            # AI move finder
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    start_time = time.time()
                    ai_thinking = True

                    return_queue = Queue()
                    if self.algorithm == 1:
                        move_finder_process = Process(
                            target=AI.MiniMax.findBestMove,
                            args=(game_state, valid_moves, return_queue, self.level)
                        )
                    if self.algorithm == 2:
                        move_finder_process = Process(
                            target=AI.Negamax.findBestMove,
                            args=(game_state, valid_moves, return_queue, self.level)
                        )
                    if self.algorithm == 3:
                        move_finder_process = Process(
                            target=AI.MCTS.findBestMove,
                            args=(game_state, return_queue, self.level*200)
                        )
                    if self.algorithm == 4:
                        move_finder_process = Process(
                            target=AI.PVS.findBestMove,
                            args=(game_state, valid_moves, return_queue, self.level)
                        )
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = AI.Score.findRandomMove(valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    ai_thinking = False
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print("Thời gian đi nước vừa rồi:", elapsed_time, "giây")
            if move_made:
                #self.drawMoveLog(game_state)
                valid_moves = game_state.getValidMoves()
                move_made = False
                move_undone = False

            self.drawGameState(screen, self.level, game_state, valid_moves, square_selected)
            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    self.drawEndGameText(screen, "Black wins by checkmate")
                else:
                    self.drawEndGameText(screen, "White wins by checkmate")

            elif game_state.stalemate:
                game_over = True
                self.drawEndGameText(screen, "Stalemate")
            p.display.flip()
    def drawGameState(self, screen, level, game_state, valid_moves, square_selected):
        self.drawBoard(screen, level)  # draw squares on the board
        self.highlightSquares(screen, game_state, valid_moves, square_selected)
        self.drawPieces(screen, game_state.board)  # draw pieces on top of those squares

    def drawBoard(self, screen, level_color):
        if level_color == 0:
            colors = [(255, 255, 255), (12, 226, 118)]
        if level_color == 1:
            colors = [(255, 255, 255), (124, 202, 30)]
        if level_color == 2:
            colors = [(255, 255, 255), (215, 226, 30)]
        if level_color == 3:
            colors = [(255, 255, 255), (117, 27, 240)]
        if level_color == 4:
            colors = [(255, 255, 255), (255, 0, 0)]
        if level_color == 5:
            colors = [(255, 255, 255), (255, 0, 170)]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                color = colors[((row + column) % 2)]
                p.draw.rect(screen, color, p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                                  self.SQUARE_SIZE, self.SQUARE_SIZE))

    def highlightSquares(self, screen, game_state, valid_moves, square_selected):
        if len(game_state.move_log) > 0:
            last_move = game_state.move_log[-1]
            s = p.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (last_move.end_col * self.SQUARE_SIZE, last_move.end_row * self.SQUARE_SIZE))
        if square_selected != ():
            row, col = square_selected
            if game_state.board[row][col][0] == (
                    'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
                # highlight selected square
                s = p.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
                s.fill(p.Color('blue'))
                screen.blit(s, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                # highlight moves from that square
                s.fill(p.Color('yellow'))
                for move in valid_moves:
                    if move.start_row == row and move.start_col == col:
                        screen.blit(s, (move.end_col * self.SQUARE_SIZE, move.end_row * self.SQUARE_SIZE))

    def drawPieces(self, screen, board):
        """
        Draw the pieces on the board using the current game_state.board
        """
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(self.IMAGES[piece],
                                p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                       self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawMoveLog(self, game_state):
        print(game_state.move_log[len(game_state.move_log) - 1])

    def drawEndGameText(self, screen, text):
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, False, p.Color("gray"))
        text_location = p.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT).move(
            self.BOARD_WIDTH / 2 - text_object.get_width() / 2,
            self.BOARD_HEIGHT / 2 - text_object.get_height() / 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color('black'))
        screen.blit(text_object, text_location.move(2, 2))

    def loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),
                                                   (self.SQUARE_SIZE, self.SQUARE_SIZE))


