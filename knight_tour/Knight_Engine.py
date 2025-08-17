import time
import pygame as p

Width = Height = 520
Dimension = 8
SQ_Size = Height // Dimension
IMAGES = {}


def draw_board(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for row in range(Dimension):
        for column in range(Dimension):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_Size, row * SQ_Size, SQ_Size, SQ_Size))


def load_images():
    IMAGES['wN'] = p.transform.scale(
        p.image.load("/Users/chidanandh/Desktop/Python folders/knight_tour/knight_tour/Chess pieces/wN.png"),
        (SQ_Size, SQ_Size))


def draw_pieces(screen, board):
    for row in range(Dimension):
        for column in range(Dimension):
            piece = board[row][column]
            if piece != "--" and piece != "!!":
                screen.blit(IMAGES[piece], p.Rect(column * SQ_Size, row * SQ_Size, SQ_Size, SQ_Size))
            elif piece == "!!":
                p.draw.circle(screen, p.Color("blue"),
                              (column * SQ_Size + SQ_Size // 2, row * SQ_Size + SQ_Size // 2),
                              SQ_Size // 4)


def draw_green_lines(screen, moves):
    for move in moves:
        start_x = move.startColumn * SQ_Size + SQ_Size // 2
        start_y = move.startRow * SQ_Size + SQ_Size // 2
        end_x = move.endColumn * SQ_Size + SQ_Size // 2
        end_y = move.endRow * SQ_Size + SQ_Size // 2
        p.draw.line(screen, p.Color("green"), (start_x, start_y), (end_x, end_y), 2)


class GameState:
    def __init__(self):
        self.Board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.knight_directions = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2))

    def get_knight_moves(self, r, c):
        moves = []
        for d in self.knight_directions:
            end_row = r + d[0]
            end_column = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                if self.Board[end_row][end_column] == '--':
                    moves.append(Move((r, c), (end_row, end_column), self.Board))
        return moves

    def get_shortest_moves(self, moves):
        future_moves = []

        for f_moves in moves:
            inner_list = []
            end_r = f_moves.endRow 
            end_c = f_moves.endColumn

            for d in self.knight_directions:
                end_row = end_r + d[0]
                end_column = end_c + d[1]
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    if self.Board[end_row][end_column] == '--':
                        inner_list.append(Move((end_r, end_c), (end_row, end_column), self.Board))

            future_moves.append(inner_list)

        if not future_moves:
            return None

        min_length = min(len(inner_list) for inner_list in future_moves)
        movable_space = [inner_list for inner_list in future_moves if len(inner_list) == min_length]

        if movable_space and movable_space[0]:
            first_move = movable_space[0][0]
            return first_move.startRow, first_move.startColumn

        return None

    def knight_tour_finisher(self, screen, row, col):
        self.Board[row][col] = 'wN'

        possible_moves = self.get_knight_moves(row, col)
        while possible_moves:
            shortest_move = self.get_shortest_moves(possible_moves)
            if shortest_move is None:
                return
            end_row, end_col = shortest_move
            self.Board[end_row][end_col] = 'wN'
            self.Board[row][col] = '!!'

            time.sleep(1)

            row, col = end_row, end_col
            possible_moves = self.get_knight_moves(row, col)
            self.draw_game_state(screen)
            draw_green_lines(screen, possible_moves)
            p.display.flip()
            time.sleep(1)

    def knight_tour(self, screen,  row, col):
        self.Board[row][col] = 'wN'

        possible_moves = self.get_knight_moves(row, col)
        shortest_move = self.get_shortest_moves(possible_moves)
        if shortest_move is None:
            return
        end_row, end_col = shortest_move
        self.Board[end_row][end_col] = 'wN'
        self.Board[row][col] = '!!'  # Set the old position to empty

        draw_green_lines(screen, possible_moves)
        self.draw_game_state(screen)
        p.display.flip()

    def get_knight_location(self):
        for i in range(8):
            for j in range(8):
                if self.Board[i][j] == 'wN':
                    return i, j

    def draw_game_state(self, screen):
        draw_board(screen)
        draw_pieces(screen, self.Board)


class Move:
    Ranks_To_Rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    Rows_To_Ranks = {v: k for k, v in Ranks_To_Rows.items()}
    Files_To_Col = {"a": 7, "b": 6, "c": 5, "d": 4,
                    "e": 3, "f": 2, "g": 1, "h": 0}
    Col_To_Files = {v: k for k, v in Files_To_Col.items()}

    def __init__(self, start_sq, end_sq, board):
        self.startRow = start_sq[0]
        self.startColumn = start_sq[1]
        self.endRow = end_sq[0]
        self.endColumn = end_sq[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]

        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        return self.get_rank_files(self.startRow, self.startColumn) + self.get_rank_files(self.endRow, self.endColumn)

    def get_rank_files(self, r, c):
        return self.Col_To_Files[c] + self.Rows_To_Ranks[r]
