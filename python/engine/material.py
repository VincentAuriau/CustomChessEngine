from engine.color import Color


class Piece(object):

    def __init__(self, white, x, y):
        self.white = white
        self.killed = False

        self.x = x
        self.y = y

    def piece_deepcopy(self):
        copied_piece = Piece(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def is_white(self):
        return self.white

    def is_killed(self):
        return self.killed

    def set_killed(self):
        self.killed = True

    def piece_move_authorized(self, start, end):
        if start.get_x() == end.get_x() and start.get_y() == end.get_y():
            return False
        else:
            return True

    def can_move(self, board, move):
        is_movement_authorized = self.piece_move_authorized(move.start, move.end)
        return is_movement_authorized

    def get_potential_moves(self, x, y):
        return None

    def get_str(self):
        return '     '

    def draw(self):
        value = self.get_str()
        if self.is_white():
            return Color.GREEN + value + Color.WHITE
        else:
            return Color.RED + value + Color.WHITE


class Pawn(Piece):

    type = "pawn"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_moved = False  # if the pawn has yet been moved or not to keep ?
        self.last_move_is_double = False  # check for en passant, if last move was a double tap

    def piece_deepcopy(self):
        copied_piece = Pawn(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.has_moved = self.has_moved
        copied_piece.last_move_is_double = self.last_move_is_double
        return copied_piece

    def piece_move_authorized(self, start, end):
        if end.get_piece() is not None:
            # check if there is not another piece of same color
            ###print(end.get_piece(), start.get_piece())
            if end.get_piece().is_white() == self.is_white():
                ###print("PAWN TAKING PIECE OF SAME COLOR")
                return False
            else:
                # Pawn can only take an adversary piece in diagonal
                dx = end.get_x() - start.get_x()
                dy = end.get_y() - start.get_y()
                if dx == 1 and abs(dy) == 1 and self.is_white():
                    return True
                elif dx == -1 and abs(dy) == 1 and not self.is_white():
                    return True
                else:
                    ###print("PAWN NOT TAKING OTHER PIECE IN DIAGONAL")
                    return False

        else:
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()
            if dx == 1 and dy == 0 and self.is_white():
                return True
            elif dx == -1 and dy == 0 and not self.is_white():
                return True

            else:
                if start.get_x() == 1 and dx == 2 and dy == 0 and self.is_white():
                    return True
                elif start.get_x() == 6 and dx == -2 and dy == 0 and not self.is_white():
                    return True
                else:
                    ###print("PAWN MOVE NOT AUTHORIZED WITH DX %i and DY %i" %(dx, dy))
                    return False

    def can_move(self, board, move):
        authorized_move = self.piece_move_authorized(move.start, move.end)
        ###print("move authorized ?", authorized_move)
        if not authorized_move:
            """to remove ?"""
            crossed_cell = board.get_cell(move.start.get_x(), move.end.get_y())
            crossed_piece = crossed_cell.get_piece()
            if isinstance(crossed_piece, Pawn):
                if crossed_piece.last_move_is_double and crossed_piece.is_white() != self.is_white():
                    # Revoir comment on update cet attribut last_move_is_double
                    authorized_move = True
                    move.complementary_passant = crossed_cell
        else:
            dx = move.end.get_x() - move.start.get_x()

            if dx > 1:
                if board.get_cell(move.start.get_x()+1, move.start.get_y()).get_piece() is not None:
                    ###print('Pawn line of sight blocked')
                    return False
            elif dx < -1:
                if board.get_cell(move.start.get_x()-1, move.start.get_y()).get_piece() is not None:
                    ###print('Pawn line of sight blocked')
                    return False
        """
        if move.end.get_x() == 7 and self.is_white():
            move.transform_pawn = True
        elif move.end.get_x() == 0 and not self.is_white():
            move.transform_pawn = True
        """
        return authorized_move

    def get_potential_moves(self, x, y):
        possible_moves = []
        if self.is_white():
            possible_moves.append((x + 1, y))
            if y - 1 >= 0:
                possible_moves.append((x + 1, y - 1))
            if y + 1 <= 7:
                possible_moves.append((x + 1, y + 1))

            if x == 1:
                possible_moves.append((x + 2, y))
        else:
            possible_moves.append((x - 1, y))

            if y - 1 >= 0:
                possible_moves.append((x - 1, y - 1))
            if y + 1 <= 7:
                possible_moves.append((x - 1, y + 1))
            if x == 6:
                possible_moves.append((x - 2, y))

        return possible_moves

    def get_str(self):
        return '  P  '


class Bishop(Piece):

    type = "bishop"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        copied_piece = Bishop(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        if start.get_x() == end.get_x() and start.get_y() == end.get_y():
            return False
        else:
            if end.get_piece() is not None:
                if end.get_piece().is_white() == self.is_white():
                    return False
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()
            if abs(dx) == abs(dy):
                return True
            else:
                return False

    def can_move(self, board, move):
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()
            for i in range(1, abs(dx)):
                x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    ###print('Bishop line of sight blocked')
                    return False
            return True
        else:
            return False

    def get_potential_moves(self, x, y):
        possible_moves = []

        nx = x - 1
        ny = y - 1
        while nx >= 0 and ny >= 0:
            possible_moves.append((nx, ny))
            nx -= 1
            ny -= 1

        nx = x - 1
        ny = y + 1
        while nx >= 0 and ny <= 7:
            possible_moves.append((nx, ny))
            nx -= 1
            ny += 1

        nx = x + 1
        ny = y - 1
        while nx <= 7 and ny >= 0:
            possible_moves.append((nx, ny))
            nx += 1
            ny -= 1

        nx = x + 1
        ny = y + 1
        while nx <= 7 and ny <= 7:
            possible_moves.append((nx, ny))
            nx += 1
            ny += 1

        return possible_moves

    def get_str(self):
        return '  B  '


class Rook(Piece):

    type = "rook"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_moved = False

    def piece_deepcopy(self):
        copied_piece = Rook(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.has_moved = self.has_moved
        return copied_piece

    def piece_move_authorized(self, start, end):
        if start.get_x() == end.get_x() and start.get_y() == end.get_y():
            return False
        else:
            if end.get_piece() is not None:
                if end.get_piece().is_white() == self.is_white():
                    return False
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()
            if dx == 0 or dy == 0:
                return True
            else:
                return False

    def can_move(self, board, move):
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()
            for i in range(1, abs(dx)):
                x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                y_trajectory = move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    ###print('Rook line of sight blocked')
                    return False
            for i in range(1, abs(dy)):
                x_trajectory = move.start.get_x()
                y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    ###print('Rook line of sight blocked')
                    return False
            return True
        else:
            return False

    def get_potential_moves(self, x, y):
        possible_moves = []

        nx = x - 1
        while nx >= 0:
            possible_moves.append((nx, y))
            nx -= 1

        ny = y + 1
        while ny <= 7:
            possible_moves.append((x, ny))
            ny += 1

        nx = x + 1
        while nx <= 7:
            possible_moves.append((nx, y))
            nx += 1

        ny = y - 1
        while ny >= 0:
            possible_moves.append((x, ny))
            ny -= 1

        return possible_moves

    def get_str(self):
        return '  R  '


class Knight(Piece):

    type = "knight"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        copied_piece = Knight(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = start.get_x() - end.get_x()
        dy = start.get_y() - end.get_y()
        return abs(dx) * abs(dy) == 2

    def can_move(self, board, move):
        return self.piece_move_authorized(move.start, move.end)

    def get_str(self):
        return '  N  '

    def get_potential_moves(self, x, y):
        possible_moves = []

        combos = [(2, 1), (1, 2), (-2, 1), (2, -1), (-2, -1), (-1, 2), (1, -2), (-1, -2)]
        for nx, ny in combos:
            if 0 <= nx+x <= 7 and 0 <= ny+y <= 7:
                possible_moves.append((x+nx, y+ny))

        return possible_moves


class Queen(Piece):

    type = "queen"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        copied_piece = Queen(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        if start.get_x() == end.get_x() and start.get_y() == end.get_y():
            return False
        else:
            if end.get_piece() is not None:
                if end.get_piece().is_white() == self.is_white():
                    return False
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()

            return (dx == 0) or (dy == 0) or (abs(dx) == abs(dy))

    def can_move(self, board, move):
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()
            if dx == 0 or dy == 0:
                for i in range(1, abs(dx)):
                    x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                    y_trajectory = move.start.get_y()
                    if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                        ###print('Queen line of sight blocked')
                        return False
                for i in range(1, abs(dy)):
                    x_trajectory = move.start.get_x()
                    y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                    if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                        ###print('Queen line of sight blocked')
                        return False
                return True
            elif abs(dx) == abs(dy):
                for i in range(1, abs(dx)):
                    x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                    y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                    if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                        ###print('Queen line of sight blocked')
                        return False
                return True
        else:
            return False

    def get_potential_moves(self, x, y):
        possible_moves = []

        nx = x - 1
        ny = y - 1
        while nx >= 0 and ny >= 0:
            possible_moves.append((nx, ny))
            nx -= 1
            ny -= 1

        nx = x - 1
        ny = y + 1
        while nx >= 0 and ny <= 7:
            possible_moves.append((nx, ny))
            nx -= 1
            ny += 1

        nx = x + 1
        ny = y - 1
        while nx <= 7 and ny >= 0:
            possible_moves.append((nx, ny))
            nx += 1
            ny -= 1

        nx = x + 1
        ny = y + 1
        while nx <= 7 and ny <= 7:
            possible_moves.append((nx, ny))
            nx += 1
            ny += 1

        nx = x - 1
        while nx >= 0:
            possible_moves.append((nx, y))
            nx -= 1

        nx = x + 1
        while nx <= 7:
            possible_moves.append((nx, y))
            nx += 1

        ny = y - 1
        while ny >= 0:
            possible_moves.append((x, ny))
            ny -= 1

        ny = y + 1
        while ny <= 7:
            possible_moves.append((x, ny))
            ny += 1

        return possible_moves

    def get_str(self):
        return '  Q  '


class King(Piece):

    type = "king"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.castling_done = False
        self.has_moved = False

    def piece_deepcopy(self):
        copied_piece = King(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.castling_done = self.castling_done
        copied_piece.has_moved = self.has_moved
        return copied_piece

    def set_castling_done(self, castling_done):
        self.castling_done = castling_done

    def piece_move_authorized(self, start, end):
        if start.get_x() == end.get_x() and start.get_y() == end.get_y():
            return False
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()

        if abs(dx) < 2 and abs(dy) < 2:
            return True
        else:
            return False

    def can_move(self, board, move):
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            if move.end.is_threatened(board, self.is_white()):
                ###print('King cannot move to a threatened cell')
                return False
            else:
                return True
        else:
            ###print('King moving, not threatened in new cell but cannot move toward it, move not authorized')

            if not self.castling_done and not self.has_moved and (move.end.y == 6 or move.end.y == 2):
                if move.end.y == 6:  # Roque vers la droite
                    rook_to_move = board.get_cell(move.start.x, 7).get_piece()
                    rook_starting_coordinates = (move.start.x, 7)
                    rook_ending_coordinates = (move.start.x, 5)
                    if isinstance(rook_to_move, Rook):
                        must_be_empty_cells = [board.get_cell(move.start.x, 5), board.get_cell(move.start.x, 6)]
                        must_not_be_threatened_cells = [board.get_cell(move.start.x, 4),
                                                        board.get_cell(move.start.x, 5),
                                                        board.get_cell(move.start.x, 6)]
                    else:
                        ###print('Rook has moved cannot do castling', rook_to_move)
                        return False

                elif move.end.y == 2:  # Roque vers la gauche
                    rook_to_move = board.get_cell(move.start.x, 0).get_piece()
                    rook_starting_coordinates = (move.start.x, 0)
                    rook_ending_coordinates = (move.start.x, 3)
                    if isinstance(rook_to_move, Rook):
                        must_be_empty_cells = [board.get_cell(move.start.x, 1), board.get_cell(move.start.x, 2),
                                               board.get_cell(move.start.x, 3)]
                        must_not_be_threatened_cells = [board.get_cell(move.start.x, 2),
                                                        board.get_cell(move.start.x, 3),
                                                        board.get_cell(move.start.x, 4)]
                    else:
                        ###print('Rook to move issue', rook_to_move)
                        return False

                else:
                    ###print('Weird move ordinate', move.end.x, move.end.y)
                    return False

                empty_cells_check = True
                not_threatened_cells = True
                for cll in must_be_empty_cells:
                    if cll.get_piece() is not None:
                        empty_cells_check = False
                for cll in must_not_be_threatened_cells:
                    if cll.is_threatened(board, self.is_white()):
                        not_threatened_cells = False

                conditions_to_castling = [not rook_to_move.has_moved, empty_cells_check, not_threatened_cells]
                if all(conditions_to_castling):
                    move.complementary_castling = rook_to_move,  board.get_cell(rook_starting_coordinates[0],
                                                                                rook_starting_coordinates[1]), \
                                                  board.get_cell(rook_ending_coordinates[0], rook_ending_coordinates[1])
                    return True
                else:
                    ###print('Conditions for castling:')
                    ###print('Rook has moved:', rook_to_move.has_moved)
                    ###print('Cells in between empty:', empty_cells_check)
                    ###print('Cells in between not threatened:', not_threatened_cells)
                    return False
            return False


    def get_potential_moves(self, x, y):
        possible_moves = []

        combos = [(1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (-1, 0)]
        for nx, ny in combos:
            if 0 <= x+nx <= 7 and 0 <= y+ny <= 7:
                possible_moves.append((nx+x, ny+y))

        if not self.has_moved:
            possible_moves.append((x, 1))
            possible_moves.append((x, 6))

        return possible_moves

    def get_str(self):
        return '  K  '

    def is_checked(self, board):
        return board.get_cell(self.x, self.y).is_threatened(board, self.white)

    # def is_checked_mate(self, board):
    #     if not self.is_checked(board):
    #         return False
    #
    #     for i in range(8):
    #         for j in range(8):
    #             piece = board.get_cell(i, j).get_piece()
    #             if piece is not None:
    #                 if piece.is_white() == self.is_white():
    #                     for move in piece.get_potential_moves(piece.x, piece.y):
    #                         selected_move = Move(None, board.get_cell(i, j),
    #                                              board.get_cell(move[0], move[1]))
    #                         verified_move = piece.can_move(board, selected_move)
    #
    #                         if verified_move:
    #                             copied_board = board.copy()

