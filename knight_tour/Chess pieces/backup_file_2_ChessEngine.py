"""
This class is responsible for storing all information about current game state of a Chess game. It will also be
responsible for determining the valid moves at the current state and also keep the move log.
"""
import copy


class GameState:
    def __init__(self):
        self.Board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'B': self.get_bishop_moves,
                               'N': self.get_knight_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.Redo_Stack = []
        self.Undo_STack = []
        self.White_To_Move = True
        self.Bin = []
        self.Move_Log = []
        self.isCheck = False
        self.Pins = []
        self.Checks = []
    '''
    Takes a move as a parameter and executes it (This won't work for castling and enpassant)
    '''
    def make_move(self, move):
        # This method is used prevent modification of 'previous board pos' if the board is modified
        self.Undo_STack.append(copy.deepcopy(self.Board))
        self.Board[move.startRow][move.startColumn] = "--"
        self.Board[move.endRow][move.endColumn] = move.pieceMoved
        self.Move_Log.append(move)  # log the moves to undo
        self.White_To_Move = not self.White_To_Move  # swap players
        # update the kings location
        if move.pieceMoved == 'wK':
            self.White_King_Location = (move.endRow, move.endColumn)
        elif move.pieceMoved == 'bK':
            self.Black_King_Location = (move.endRow, move.endColumn)
        # print(self.Undo_STack[-1])

    def undo_move(self):
        # With this modified function reversing castling and enpassant is possible
        if len(self.Move_Log) != 0:
            # self.Board = self.prev_board_pos[0]
            # self.Board[move.startRow][move.startColumn] = move.pieceMoved
            # self.Board[move.endRow][move.endColumn] = move.pieceCaptured
            # move = self.Move_Log.pop()

            self.Bin.append(self.Move_Log.pop())
            self.Redo_Stack.append(copy.deepcopy(self.Board))
            self.Board = self.Undo_STack.pop()
            self.White_To_Move = not self.White_To_Move
            # if move.pieceMoved == 'wK':
            #     self.White_King_Location = (move.startRow, move.startColumn)
            # elif move.pieceMoved == 'bK':
            #     self.Black_King_Location = (move.endRow, move.endColumn)

    def redo_move(self):
        if self.Redo_Stack:
            self.Undo_STack.append(copy.deepcopy(self.Board))
            self.Board = self.Redo_Stack.pop()
            self.Move_Log.append(self.Bin.pop())
            self.White_To_Move = not self.White_To_Move
            # move = self.Move_Log[-1]
            # if move.pieceMoved == 'wK':
            #     self.White_King_Location = (move.endRow, move.endColumn)
            # elif move.pieceMoved == 'bK':
            #     self.Black_King_Location = (move.endRow, move.endColumn)
    '''
    All the moves considering checks 
    '''
    # def get_valid_moves_naive_algorithm(self):
    #     moves = self.get_all_possible_moves()
    #     for i in range(len(moves)-1, -1, -1):
    #         self.make_move(moves[i])
    #
    #
    #     return moves
    def get_valid_moves(self):
        all_moves = self.get_all_possible_moves()
        return self.get_safe_moves(all_moves)

    def get_safe_moves(self, moves):
        self.safe_moves = []
        for move in moves:
            self.make_move(move)
            if not self.is_king_in_check():
                self.safe_moves.append(move)
            self.undo_move()
        return self.safe_moves
    '''
    All the moves not considering checks
    '''
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.Board)):  # Number of rows
            for c in range(len(self.Board[r])):  # number of cols in given row
                turn = self.Board[r][c][0]
                if (turn == 'w' and self.White_To_Move) or (turn == 'b' and not self.White_To_Move):
                    piece = self.Board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves
    '''
    This function will get all the pawn moves 
    '''
    def get_pawn_moves(self, r, c, moves):
        if self.White_To_Move:  # White pawn moves
            if (self.Board[r-1][c] == '--') and (r - 1 >= 0):  # one square pawn advance
                moves.append(Move((r, c), (r-1, c), self.Board))
                if r == 6 and self.Board[r-2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.Board))
            if (c - 1 >= 0) and (r - 1 >= 0):  # Captures to the left
                if (self.Board[r - 1][c - 1] != '--') and (self.Board[r - 1][c - 1][0] == 'b'):
                    moves.append(Move((r, c), (r-1, c-1), self.Board))
            if (c + 1 <= 7) and (r - 1 >= 0):  # Captures to right
                if (self.Board[r - 1][c + 1] != '--') and (self.Board[r - 1][c + 1][0] == 'b'):
                    moves.append(Move((r, c), (r - 1, c + 1), self.Board))
            if r == 0:
                self.Board[r][c] = 'wQ'

        else:
            if r == 7:
                self.Board[r][c] = 'bQ'
            if self.Board[r + 1][c] == '--':  # one square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.Board))
                if r == 1 and self.Board[r + 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.Board))
            if (c + 1 <= 7) and (r + 1 <= 7):  # Captures to Right
                if (self.Board[r + 1][c + 1] != '--') and (self.Board[r + 1][c + 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c + 1), self.Board))
            if (c - 1 > 0) and (r + 1 < 7):  # Captures to Left
                if (self.Board[r + 1][c - 1] != '--') and (self.Board[r + 1][c - 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c - 1), self.Board))

    def get_rook_moves(self, r, c, moves):
        # directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        # enemy_piece_row = []
        # present_row_location = r
        # present_col_location = c
        # # for row in range(7):
        #     if (self.Board[row][c] != '--') and (self.Board[row][c][0] == enemy_color):
        #         moves.append(Move((r, c), (row, c), self.Board))
        #         break
        #     elif self.Board[row][c] == '--':
        #         moves.append(Move((r, c), (row, c), self.Board))
        # for col in range(7):
        #     if (self.Board[r][col] != '--') and (self.Board[r][col][0] == enemy_color):
        #         moves.append(Move((r, c), (r, col), self.Board))
        #         break
        #     elif self.Board[r][col] == '--':
        #         moves.append(Move((r, c), (r, col), self.Board))
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_column = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.Board[end_row][end_column]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                        break
                    else:  # if friendly piece was encountered
                        break
                else:  # out of the board case
                    break

    def get_bishop_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_column = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_place = self.Board[end_row][end_column]
                    if end_place == '--':
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                    elif end_place[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                        break
                    else:  # if friendly piece was encountered
                        break
                else:  # out of the board case
                    break

    def get_knight_moves(self, r, c, moves):
        directions = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for d in directions:
            end_row = r + d[0]
            end_column = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                enemy_piece = self.Board[end_row][end_column]
                if self.Board[end_row][end_column] == '--':
                    moves.append(Move((r, c), (end_row, end_column), self.Board))
                elif enemy_piece[0] == enemy_color:
                    moves.append(Move((r, c), (end_row, end_column), self.Board))

    def get_queen_moves(self, r, c, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for d in direction:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_column = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_place = self.Board[end_row][end_column]
                    if end_place == '--':
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                    elif end_place[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_column), self.Board))
                        break
                    else:  # if friendly piece was encountered
                        break
                else:  # out of the board case
                    break

    def get_king_moves(self, r, c, moves):
        king_direction = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for i in range(8):
            end_row = r + king_direction[i][0]
            end_column = c + king_direction[i][1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_place = self.Board[end_row][end_column]
                if end_place == '--':
                    moves.append(Move((r, c), (end_row, end_column), self.Board))
                elif end_place[0] == enemy_color:
                    moves.append(Move((r, c), (end_row, end_column), self.Board))

    def find_kings(self):
        wk_location = None
        bk_location = None

        for row in range(len(self.Board)):
            for col in range(len(self.Board[row])):
                if self.Board[row][col] == "wK":
                    wk_location = (row, col)
                elif self.Board[row][col] == "bK":
                    bk_location = (row, col)

        if self.White_To_Move:
            return wk_location
        else:
            return bk_location

    def is_king_in_check(self):
        location = self.find_kings()
        if location is None:
            return False  # No king found, not in check
        r, c = location
        # check in all diagonals
        diagonal_direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        non_diagonal_direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for d in diagonal_direction:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_column = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_place = self.Board[end_row][end_column]
                    if end_place == '--':
                        continue
                    elif (end_place[0] == enemy_color) and (end_place[1] == 'Q' or end_place[1] == 'B'):
                        return True
                    else:
                        break
        for n in non_diagonal_direction:
            for i in range(1, 8):
                end_row = r + n[0] * i
                end_column = c + n[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.Board[end_row][end_column]
                    if end_piece == '--':
                        continue
                    elif (end_piece[0] == enemy_color) and (end_piece[1] == 'Q' or end_piece[1] == 'R'):
                        return True

                    else:  # if friendly piece was encountered
                        break
                else:  # out of the board case
                    break
        l_directions = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2))
        enemy_color = 'b' if self.White_To_Move else 'w'
        for v in l_directions:
            end_row = r + v[0]
            end_column = c + v[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                enemy_piece = self.Board[end_row][end_column]
                if self.Board[end_row][end_column] == '--':
                    continue
                elif (enemy_piece[0] == enemy_color) and (enemy_piece[1] == 'N'):
                    return True


class Move:
    # Maps keys to vals
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
        # print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        return self.get_rank_files(self.startRow, self.startColumn) + self.get_rank_files(self.endRow, self.endColumn)

    def get_rank_files(self, r, c):
        return self.Col_To_Files[c] + self.Rows_To_Ranks[r]
