# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from copy import deepcopy

import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    def __init__(self, rows_left: list, columns_left: list, boats_left: list,
                 matrix: np.ndarray((10, 10)), init=False, sorted_hints=[], candidate_actions=None):
        """O construtor deve receber os valores das pistas (rows_left e
        columns_left) e o tabuleiro (board) e inicializar as variáveis
        de instância."""
        self.candidate_actions = candidate_actions
        self.rows_left = rows_left
        self.columns_left = columns_left
        self.boats_left = boats_left   # [1p,2p,3p,4p]
        self.matrix = matrix
        self.candidates_from_hints = {}
        if init:
           # self.rows_to_fill = [10] * 10
            #self.columns_to_fill = [10] * 10
            self.initialize(sorted_hints)
        else:
            pass    # TODO

    def copy(self):
        rows = self.rows_left.copy()
        cols = self.columns_left.copy()
        boats = self.boats_left.copy()
        matrix = self.matrix.copy()
        candidate_actions = deepcopy(self.candidate_actions)

        return Board(rows, cols, boats, matrix, candidate_actions=candidate_actions)

    """Representação interna de um tabuleiro de Bimaru."""

    def initialize(self, sorted_hints: list):
        for i in range(10):
            if self.rows_left[i] == 0:
                self.fill_row_with_water(i)
            if self.columns_left[i] == 0:
                self.fill_col_with_water(i)

        for hint in sorted_hints:
                # add piece & water inference to matrix
                piece = hint[2]
                hint_row = hint[0]
                hint_col = hint[1]
                # TODO: checks prev piece for already counted boat

                if piece == 1:  # if water don't check anything
                    self.place_water(hint_row, hint_col, "rlud")
                    continue

                prev_piece = self.matrix[hint_row, hint_col]
                if piece == prev_piece:  # already infered
                    continue

                if prev_piece == 0:  # if empty
                    self.place_piece(hint_row, hint_col, piece)  # Place hint
                else:  # it's undefined
                    self.replace_piece(hint_row, hint_col, piece)  # Replace hint



                if piece != 8:  # if not middle
                    if piece == 2:
                        self.remove_boat(1)  # mark boat of 1 piece as found

                    elif prev_piece == 9:  # if undefined
                        self.remove_boat(2)  # it's a 2p boat
                        del self.candidates_from_hints[(hint_row, hint_col)]
                        #remove from candidates

                    elif piece == 3:  # hint is Top
                        if hint_row == 8 and self.matrix[hint_row + 2, hint_col] == 1:  # if water 2 under or last row
                            self.place_piece(hint_row + 1, hint_col, 4)  # place Bottom
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        elif self.matrix[hint_row + 1, hint_col] == 9:  # if undefined below
                            self.remove_boat(3)  # it's a 3p boat because Middles are not present   (they're the last hints to be added)
                            self.replace_piece(hint_row + 1, hint_col, 8)  # replace with Middle
                        elif self.matrix[hint_row + 2, hint_col] == 9:  # if undefined 2 squares below
                            self.remove_boat(4)  # it's a 4p boat
                            self.place_piece(hint_row + 1, hint_col, 8)   # Place Middle FIXME: check if it's correct
                            self.replace_piece(hint_row + 2, hint_col, 8)   # replace with Middles
                        else:
                            self.place_piece(hint_row + 1, hint_col, 9, originator=(hint_row, hint_col, 3))  # place Undefined
                            self.infer_water(9, hint_row + 1, hint_col)

                    elif piece == 4:  # if Bottom
                        if hint_row == 1 and self.matrix[hint_row - 2, hint_col] == 1:  # if water 2 above or first row
                            self.place_piece(hint_row - 1, hint_col, 3)  # place Top
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        elif self.matrix[hint_row - 1, hint_col] == 9:  # if undefined below
                            self.remove_boat(3)  # it's a 3p boat because Middles are not present   (they're the last hints to be added)
                            self.replace_piece(hint_row - 1, hint_col, 8)  # place Middle
                        elif self.matrix[hint_row - 2, hint_col] == 9:  # if undefined 2 squares below
                            self.remove_boat(4)  # it's a 4p boat
                            self.place_piece(hint_row - 1, hint_col, 8)  # Fixme: check if it's correct
                            self.replace_piece(hint_row - 2, hint_col, 8)  # replace with Middles
                        else:
                            self.place_piece(hint_row - 1, hint_col, 9, originator=(hint_row,hint_col,4))  # place Undefined
                            self.infer_water(9, hint_row - 1, hint_col)

                    elif piece == 6:  # Left
                        if hint_col == 8 and self.matrix[hint_row, hint_col + 2] == 1:  # if water 2 left or last column
                            self.place_piece(hint_row, hint_col + 1, 7)     # place Right
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        elif self.matrix[hint_row, hint_col + 1] == 9:      # if undefined on the right
                            self.remove_boat(3)  # it's a 3p boat
                            self.replace_piece(hint_row, hint_col + 1, 8)   # replace with Middle
                        elif self.matrix[hint_row, hint_col + 2] == 9:      # if undefined 2 squares on the right
                            self.remove_boat(4)  # it's a 4p boat
                            self.place_piece(hint_row, hint_col + 1, 8)     # FIXME: check if it's correct
                            self.replace_piece(hint_row, hint_col + 2, 8)   # replace with Middles
                        else:
                            self.place_piece(hint_row, hint_col + 1, 9, originator=(hint_row, hint_col,6))      # place Undefined
                            self.infer_water(9, hint_row, hint_col + 1)

                    elif piece == 7:  # Right
                        if hint_col == 1 and self.matrix[hint_row, hint_col - 2] == 1:  # if water 2 right or first column
                            self.place_piece(hint_row, hint_col - 1, 6)     # place Left
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        elif self.matrix[hint_row, hint_col - 1] == 9:      # if undefined on the left
                            self.remove_boat(3)  # it's a 3p boat
                            self.replace_piece(hint_row, hint_col - 1, 8)   # replace with Middle
                        elif self.matrix[hint_row, hint_col - 2] == 9:  # if undefined 2 squares on the left
                            self.remove_boat(4)  # it's a 4p boat
                            self.place_piece(hint_row, hint_col - 1, 8)     # FIXME: check if it's correct
                            self.replace_piece(hint_row, hint_col - 2, 8)  # replace with Middles
                        else:
                            self.place_piece(hint_row, hint_col - 1, 9, originator=(hint_row, hint_col, 7))  # place Undefined
                            self.infer_water(9, hint_row, hint_col - 1)

                    self.infer_water(piece, hint_row, hint_col)

                else:   # if Middle
                    if prev_piece == 8:  # if Middle
                        continue            # FIXME NOT NEEEDED
                    # if first row or water above -> horizontal boat
                    if hint_row == 0 or self.matrix[hint_row - 1, hint_col] == 1 or hint_row == 9 or \
                                                                self.matrix[hint_row + 1, hint_col] == 1:

                        if hint_row == 0 or self.matrix[hint_row - 1, hint_col] == 1:
                            if hint_row != 9:
                                self.place_water(hint_row + 1, hint_col, "d", True)
                        else:
                            self.place_water(hint_row - 1, hint_col, "u", True)

                        right_piece = self.matrix[hint_row, hint_col + 1]
                        left_piece = self.matrix[hint_row, hint_col - 1]
                        if right_piece > 1:
                            if right_piece == 7:  # Right
                                if self.boats_left[3] == 0 or hint_col == 1 or self.matrix[hint_row, hint_col - 2] == 1:  # if no 4p boats left
                                    self.remove_boat(3)  # we can place a 3p boat
                                    self.place_piece(hint_row, hint_col - 1, 6)  # place Left - previously empty because if it could only have Left piece and in that case, the boat would have been already found
                                    # ^^ FIXME prob right but if there is error, we check
                                    self.infer_water(6, hint_row, hint_col - 1)
                            elif right_piece == 9:  # Undefined
                                self.remove_boat(4)  # it's a 4p boat
                                self.replace_piece(hint_row, hint_col + 1, 8)  # replace with Middle on right_piece position
                                self.place_piece(hint_row, hint_col - 1, 6) # place Left on left_piece position
                                # ^^ FIXME we pretty sure it's right but if there is error, we check
                                self.infer_water(6, hint_row, hint_col - 1)
                            else:  # right_piece is Middle
                                self.remove_boat(4)  # it's a 4p boat
                                self.place_piece(hint_row, hint_col - 1, 6)         # place Left
                                self.infer_water(6, hint_row, hint_col - 1)
                                if self.matrix[hint_row, hint_col + 2] == 0:    # if empty
                                    self.place_piece(hint_row, hint_col + 2, 7)     # place Right
                                else:
                                    self.replace_piece(hint_row, hint_col + 2, 7)   # replace with Right
                                self.infer_water(7, hint_row, hint_col + 2)

                        elif left_piece > 1:
                            if left_piece == 6:  # Left
                                if self.boats_left[3] == 0 or hint_col == 8 or self.matrix[hint_row, hint_col + 2] == 1:  # if no 4p boats left
                                    self.remove_boat(3)  # we can place a 3p boat
                                    self.place_piece(hint_row, hint_col + 1, 7)  # place Right - previously empty because if it could only have Right piece and in that case, the boat would have been already found
                                    self.infer_water(7, hint_row, hint_col + 1)
                            elif left_piece == 9:  # Undefined
                                self.remove_boat(4)  # it's a 4p boat
                                self.replace_piece(hint_row, hint_col - 1, 8)  # replace left_piece with Middle
                                self.place_piece(hint_row, hint_col + 1, 7)  # place Right on right_piece position FIXME: might be wrong
                                self.infer_water(7, hint_row, hint_col + 1)
                            else:  # Middle
                                self.remove_boat(4)  # it's a 4p boat
                                self.place_piece(hint_row, hint_col + 1,  7)  # place Right
                                self.infer_water(7, hint_row, hint_col + 1)
                                if self.matrix[hint_row, hint_col - 2] == 0:    # if empty
                                    self.place_piece(hint_row, hint_col - 2, 6)     # place Right
                                else:
                                    self.replace_piece(hint_row, hint_col - 2, 6)   # replace with Right    #FIXME INTERNAL
                                self.infer_water(6, hint_row, hint_col - 2)
                        else:   # No boats next to the hint
                            if self.boats_left[3] == 0:  # no more 4p boat
                                self.place_piece(hint_row, hint_col - 1, 6)  # place Left
                                self.infer_water(6, hint_row, hint_col - 1)
                                self.place_piece(hint_row, hint_col + 1, 7)  # place Right
                                self.infer_water(7, hint_row, hint_col + 1)
                                self.remove_boat(3)
                            else:
                                placed_left = False
                                if hint_col == 1 or self.matrix[hint_row, hint_col - 2] == 1:
                                    self.place_piece(hint_row, hint_col - 1, 6)  # place Left
                                    self.infer_water(6, hint_row, hint_col - 1)
                                    placed_left = True
                                else:
                                    self.place_piece(hint_row, hint_col - 1, 9, originator=(hint_row, hint_col, 8))  # place Undefined
                                    self.infer_water(9, hint_row, hint_col - 1)

                                if hint_col == 8 or self.matrix[hint_row, hint_col + 2] == 1:
                                    self.place_piece(hint_row, hint_col + 1, 7)  # place Right
                                    self.infer_water(7, hint_row, hint_col + 1)
                                    if placed_left:
                                        self.remove_boat(3)
                                else:
                                    self.place_piece(hint_row, hint_col + 1, 9, originator=(hint_row, hint_col, 8))  # place Undefined
                                    self.infer_water(9, hint_row, hint_col + 1)

                    # if first column or water to the left -> vertical boat
                    elif hint_col == 0 or self.matrix[hint_row, hint_col - 1] == 1 or hint_col == 9 or \
                                                                self.matrix[hint_row, hint_col + 1] == 1:
                        if hint_col == 0 or self.matrix[hint_row, hint_col - 1] == 1:
                            if hint_col != 9:
                                self.place_water(hint_row, hint_col + 1, "r", True)
                        else:
                            self.place_water(hint_row, hint_col - 1, "l", True)

                        up_piece = self.matrix[hint_row - 1, hint_col]
                        down_piece = self.matrix[hint_row + 1, hint_col]
                        if up_piece > 1:
                            if up_piece == 3:  # Top
                                if self.boats_left[3] == 0 or hint_row == 8 or self.matrix[hint_row + 2, hint_col] == 1:
                                    self.remove_boat(3)  # It's a 3p boat
                                    self.place_piece(hint_row + 1, hint_col, 4)  # place Bottom on down_piece position - - previously empty because if it could only have Bottom piece and in that case, the boat would have been already found
                                    self.infer_water(4, hint_row + 1, hint_col)
                            elif up_piece == 9:  # Undefined
                                self.remove_boat(4)  # it's a 4p boat
                                self.replace_piece(hint_row - 1, hint_col, 8)  # replace with Middle
                                self.place_piece(hint_row + 1, hint_col, 4)  # place Bottom on down_piece position FIXME: might be wrong
                                self.infer_water(4, hint_row + 1, hint_col)
                            else:  # Middle
                                self.remove_boat(4)  # it's a 4p boat
                                self.place_piece(hint_row - 2, hint_col, 3)  # place Top
                                self.infer_water(3, hint_row - 2, hint_col)
                                if self.matrix[hint_row + 1, hint_col] == 0:
                                    self.place_piece(hint_row + 1, hint_col, 4)  # place Bottom
                                else:
                                    self.replace_piece(hint_row + 1, hint_col, 4)  # replace with Bottom
                                self.infer_water(4, hint_row + 1, hint_col)
                        elif down_piece > 1:
                            if down_piece == 4:  # Bottom
                                if self.boats_left[3] == 0 or hint_row == 1 or self.matrix[hint_row - 2, hint_col] == 1:
                                    self.remove_boat(3)  # It's a 3p boat
                                    self.place_piece(hint_row - 1, hint_col, 3)  # place Top
                                    # ^^ FIXME prob right but if there is error, we check
                                    self.infer_water(3, hint_row - 1, hint_col)
                            elif down_piece == 9:  # Undefined
                                self.remove_boat(4)  # it's a 4p boat
                                self.replace_piece(hint_row + 1, hint_col, 8)  # replace with Middle
                                self.place_piece(hint_row - 1, hint_col, 3)  # place Top on up_piece position
                                # ^^ FIXME we pretty sure it's right but if there is error, we check
                                self.infer_water(3, hint_row - 1, hint_col)
                            else:  # down_piece is Middle
                                self.remove_boat(4)  # it's a 4p boat
                                self.place_piece(hint_row - 1, hint_col, 3)  # place Top
                                self.infer_water(3, hint_row - 1, hint_col)
                                if self.matrix[hint_row + 2, hint_col] == 0:    # if empty
                                    self.place_piece(hint_row + 2, hint_col, 4)  # place Bottom
                                else:
                                    self.replace_piece(hint_row + 2, hint_col, 4)  # replace with Bottom
                                self.infer_water(4, hint_row + 2, hint_col)
                        else:   # vertical and No boats next to the hint
                            if self.boats_left[3] == 0:  # no more 4p boat
                                self.place_piece(hint_row - 1, hint_col, 3)  # place Top
                                self.infer_water(3, hint_row - 1, hint_col)
                                self.place_piece(hint_row + 1, hint_col, 4)  # place Bottom
                                self.infer_water(4, hint_row + 1, hint_col)
                                self.remove_boat(3)
                            else:
                                placed_top = False
                                if hint_row == 1 or self.matrix[hint_row - 2, hint_col] == 1:
                                    self.place_piece(hint_row - 1, hint_col, 3)  # Top
                                    self.infer_water(3, hint_row - 1, hint_col)
                                    placed_top = True
                                else:
                                    self.place_piece(hint_row - 1, hint_col, 9, originator=(hint_row, hint_col, 8))  # place Undefined
                                    self.infer_water(9, hint_row - 1, hint_col)

                                if hint_row == 8 or self.matrix[hint_row + 2, hint_col] == 1:
                                    self.place_piece(hint_row + 1, hint_col, 4)  # Bottom
                                    self.infer_water(4, hint_row + 1, hint_col)
                                    if placed_top:
                                        self.remove_boat(3)
                                else:
                                    self.place_piece(hint_row + 1, hint_col, 9, originator=(hint_row, hint_col, 8))  # place Undefined
                                    self.infer_water(9, hint_row + 1, hint_col)

                    # Água da peça acabada de por
                    self.infer_water(piece, hint_row, hint_col)

                """
                # TODO: remove circles from boats_left
                for r, c in Board.infer_water(piece, hint_row, hint_col):
                    matrix[r, c] = 1  # water
                """
                # decrement rows and columns
                #self.decrement_row(hint_row)
                #self.decrement_column(hint_col)
        self.candidate_actions = self.get_actions_from_candidates()
        return


    def get_actions_from_candidates(self):
        """ Returns a list of actions from candidates """
        # [top left row, top left col, boat length, horizontal]  False - Vertical, True - Horizontal
        actions = []
        for key in self.candidates_from_hints:
            grouped_actions = []  # [top left row, top left column,
            action_count = 0
            originator = self.candidates_from_hints[key]

            max_boat_len = 2
            if originator[2] == 3:  # Originator was Top
                row = key[0] + 1    # row under undefined
                column = key[1]
                grouped_actions.append((originator[0], originator[1], max_boat_len, False))  # vertical
                action_count += 1
                for i in range(2):  # there's two more sizes
                    if row <= 9 and self.matrix[row, column] == 0:  # if empty
                        max_boat_len += 1
                        row += 1
                        if self.boats_left[max_boat_len - 1] > 0 and self.columns_left[column] >= max_boat_len - 2:
                            grouped_actions.append((originator[0], originator[1], max_boat_len, False))
                            action_count += 1
                        else:
                            break
                    else:
                        break
            elif originator[2] == 4:  # Originator was Bottom
                row = key[0]
                column = key[1]
                grouped_actions.append((row, column, max_boat_len, False))  # vertical
                action_count += 1
                for i in range(2):  # two more possible
                    row -= 1
                    if row >= 0 and self.matrix[row, column] == 0:  # if empty
                        max_boat_len += 1
                        if self.boats_left[max_boat_len - 1] > 0 and self.columns_left[column] >= max_boat_len - 2:
                            grouped_actions.append((row, column, max_boat_len, False))
                            action_count += 1
                        else:
                            break
                    else:
                        break
            elif originator[2] == 6:  # Originator was Left
                row = key[0]
                column = key[1] + 1
                grouped_actions.append((originator[0], originator[1], max_boat_len, True))  # Horizontal
                action_count += 1
                for i in range(2):  # there's two more sizes
                    if column <= 9 and self.matrix[row, column] == 0:  # if empty
                        max_boat_len += 1
                        column += 1
                        if self.boats_left[max_boat_len - 1] > 0 and self.columns_left[row] >= max_boat_len - 2:
                            grouped_actions.append((originator[0], originator[1], max_boat_len, True))
                            action_count += 1
                        else:
                            break
                    else:
                        break
            elif originator[2] == 7:  # Originator was Right
                row = key[0]
                column = key[1]
                grouped_actions.append((row, column, max_boat_len, True))  # Horizontal
                action_count += 1
                for i in range(2):  # two more possible
                    column -= 1
                    if column >= 0 and self.matrix[row, column] == 0:  # if empty
                        max_boat_len += 1
                        if self.boats_left[max_boat_len - 1] > 0 and self.columns_left[row] >= max_boat_len - 2:
                            grouped_actions.append((row, column, max_boat_len, True))
                            action_count += 1
                        else:
                            break
                    else:
                        break
            elif originator[2] == 8:  # Originator was Middle
                row = key[0]
                column = key[1]
                if row == originator[0]:  # Horizontal
                    if column < originator[1]:  # Undef Left of originator
                        if column < 7 and (row, column + 2) in self.candidates_from_hints:  # if there's another candidate
                            del self.candidates_from_hints[(row, column + 2)]  # remove it

                        grouped_actions.append((row, column, 3, True))  # Add 3  - Horizontal
                        action_count += 1
                        if self.boats_left[4 - 1] > 0 and self.columns_left[row] >= 4:  # if there's a 4p left
                            grouped_actions.append((row, column - 1, 4, True))  # Add 4  - Horizontal
                            action_count += 1
                            if self.matrix[row, column + 2] != 7:  # if not Right
                                grouped_actions.append((row, column, 4, True))  # Add 4  - Horizontal
                                action_count += 1
                    else:       # Undef Right of originator
                        if column > 1 and (row, column - 2) in self.candidates_from_hints:  # if there's another candidate
                            del self.candidates_from_hints[(row, column)]  # remove it
                            continue

                        grouped_actions.append((row, column - 2, 3, True))  # Add 3  - Horizontal
                        action_count += 1
                        if self.boats_left[4 - 1] > 0 and self.columns_left[row] >= 4:  # if there's a 4p left
                            grouped_actions.append((row, column - 2, 4, True))  # Add 4  - Horizontal
                            action_count += 1
                            if self.matrix[row, column - 2] != 6:  # if not Left
                                grouped_actions.append((row, column - 3, 4, True))  # Add 4  - Horizontal
                                action_count += 1
                else:  # Vertical
                    if row < originator[0]:  # Undef Top of originator
                        if row < 7 and (row + 2, column) in self.candidates_from_hints:  # if there's another candidate
                            del self.candidates_from_hints[(row + 2, column)]
                        grouped_actions.append((row, column, 3, False))  # Add 3  - Vertical
                        action_count += 1
                        if self.boats_left[4 - 1] > 0 and self.columns_left[column] >= 4:  # if there's a 4p left
                            grouped_actions.append((row - 1, column, 4, False))  # Add 4  - Vertical
                            action_count += 1
                            if self.matrix[row + 2, column] != 4:  # if not Bottom
                                grouped_actions.append((row, column, 4, False))  # Add 4  - Vertical
                                action_count += 1
                    else:  # Undef Bottom of originator
                        if row > 1 and (row - 2, column) in self.candidates_from_hints:  # if there's another candidate
                            del self.candidates_from_hints[(row, column)]  # remove it
                            continue
                        grouped_actions.append((row - 2, column, 3, False))  # Add 3  - Vertical
                        action_count += 1
                        if self.boats_left[4 - 1] > 0 and self.columns_left[column] >= 4:  # if there's a 4p left
                            grouped_actions.append((row - 2, column, 4, False))  # Add 4  - Vertical
                            action_count += 1
                            if self.matrix[row - 2, column] != 3:  # if not Top
                                grouped_actions.append((row - 3, column, 4, False))  # Add 4  - Vertical
                                action_count += 1

            if grouped_actions:
                actions.append((action_count, sorted(grouped_actions, key=lambda x: x[2])))

        return sorted(actions, key=lambda x: x[0])


    def fill_row_with_water(self, row_no: int):
        """ Fills row with water """
        direction = "lr"
        if row_no != 0:
            direction += "d"
        if row_no != 9:
            direction += "u"

        for col_no in range(10):
            if self.matrix[row_no, col_no] == 0:  # if not filled
                self.place_water(row_no, col_no, direction, True)
        return

    def fill_col_with_water(self, col_no: int):
        """ Fills column with water """
        direction = "ud"
        if col_no != 0:
            direction += "l"
        if col_no != 9:
            direction += "r"

        for row_no in range(10):
            if self.matrix[row_no, col_no] == 0:  # if not filled
                self.place_water(row_no, col_no, direction, True)
        return

    def place_piece(self, row: int, col: int, piece: int, originator=()):
        self.matrix[row, col] = piece  # place piece
        if originator:  # if undefined
            self.candidates_from_hints[(row, col)] = originator  # add to candidates
        self.decrement_row(row)
        self.decrement_column(col)
        #self.rows_to_fill[row] -= 1
        #self.columns_to_fill[col] -= 1
        return

    def replace_piece(self, row: int, col: int, piece: int):
        self.matrix[row, col] = piece  # place piece
        if self.candidates_from_hints and (row, col) in self.candidates_from_hints:  # if undefined
            del self.candidates_from_hints[(row, col)]  # remove from candidates
        return

    def remove_boat(self, size: int):
        boat_num = self.boats_left[size - 1]
        if boat_num <= 0:
            raise Exception("No boats of this size left")

        self.boats_left[size - 1] = boat_num - 1
        return

    def place_water(self, row: int, col: int, direction: str, has_middles = False):
        """ Places water and checks in the directions given """

        # If water already present, return
        if self.matrix[row, col] == 1:
            return

        # Place water
        self.matrix[row, col] = 1

        #self.rows_to_fill[row] -= 1
        #self.columns_to_fill[col] -= 1

        if "r" in direction:
            if col < 8:
                if self.matrix[row, col + 1] == 9:  # if undefined
                    two_right = self.matrix[row, col + 2]
                    if two_right > 1:  # boat on the right of undefined (M or R)
                        self.replace_piece(row, col + 1, 6)  # replace with Left
                        if not has_middles:
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        else:
                            if two_right == 7:  # if has Right
                                self.remove_boat(2)  # mark boat of 2 pieces as found
                            else:
                                three_right = self.matrix[row, col + 3]
                                if three_right == 7:  # if has Right
                                    self.remove_boat(3)  # mark boat of 3 pieces as found

            if has_middles and col < 9 and self.matrix[row, col + 1] == 8:
                if col < 8:
                    self.place_water(row, col + 2, "r", self.matrix, self.boats_left, has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if self.matrix[row - 1, col + 1] == 0:  # above middle not filled
                    if row == 1 or self.matrix[row - 2, col + 1] == 1:  # Water above
                        self.place_piece(row - 1, col + 1, 3)    # place Top
                        if row == 8 or self.matrix[row + 2, col + 1] == 1:  # If there is water below or last row
                            self.place_piece(row + 1, col + 1, 4)  # place Bottom
                            self.remove_boat(3)   # mark boat of 3 pieces as found
                    else:
                        self.place_piece(row - 1, col + 1, 9, originator=(row, col + 1, 8))  # place Undefined
                        self.infer_water(9, row - 1, col + 1)

                if self.matrix[row + 1, col + 1] == 0:  # below Middle not filled
                    if self.matrix[row + 2, col + 1] == 1 or row == 8:  # Water
                        self.place_piece(row + 1, col + 1, 4)    # place Bottom
                    else:
                        self.place_piece(row + 1, col + 1, 9, originator=(row, col + 1, 8))  # place Undefined
                        self.infer_water(9, row + 1, col + 1)



        if "l" in direction:
            if col > 1:
                if self.matrix[row, col - 1] == 9:  # if undefined
                    two_left = self.matrix[row, col - 2]
                    if two_left > 1:  # boat on the left of undefined ([M] or L)
                        self.replace_piece(row, col - 1, 7)  # replace Right
                        if two_left == 6:   # if has Left
                            self.remove_boat(2)  # mark boat of 2p as found
                        else:
                            three_left = self.matrix[row, col - 3]
                            if three_left == 6:  # if has Left
                                self.remove_boat(3)  # mark boat of 3 pieces as found

            ######
            if has_middles and col > 0 and self.matrix[row, col - 1] == 8:
                if col > 1:
                    self.place_water(row, col - 2, "l", has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if self.matrix[row - 1, col - 1] == 0:  # not filled
                    if row == 1 or self.matrix[row - 2, col - 1] == 1:  # Water above
                            self.place_piece(row - 1, col - 1, 3)  # place Top
                            if row == 8 or self.matrix[row + 2, col - 1] == 1:  # If there is water below or last row
                                self.place_piece(row + 1, col - 1, 4)  # place Bottom
                                self.remove_boat(3)  # mark boat of 3 pieces as found
                    else:
                        self.place_piece(row - 1, col - 1, 9, originator=(row, col - 1, 8))  # place Undefined
                        self.infer_water(9, row - 1, col - 1)

                if self.matrix[row + 1, col - 1] == 0:  # not filled
                    if self.matrix[row + 2, col - 1] == 1 or row == 8:  # Water
                        self.place_piece(row + 1, col - 1, 4)    # Place Bottom
                    else:
                        self.place_piece(row + 1, col - 1, 9, originator=(row, col - 1, 8))  # place Undefined
                        self.infer_water(9, row + 1, col - 1)

        if "u" in direction:
            if row > 1 and self.matrix[row - 1, col] == 9:  # if undefined
                two_up = self.matrix[row - 2, col]
                if two_up > 1:  # boat on the top of undefined ([M] or T)
                    self.replace_piece(row - 1, col, 4)  # replace Bottom # TODO: boat
                    if not has_middles:
                        self.remove_boat(2)  # mark boat of 2p as found
                    else:
                        if two_up == 3:  # if has Top
                            self.remove_boat(2)  # mark boat of 2p as found
                        else:
                            three_up = self.matrix[row - 3, col]
                            if three_up == 3:  # if has Top
                                self.remove_boat(3)  # mark boat of 3 pieces as found
            ######
            if has_middles and row > 0 and self.matrix[row - 1, col] == 8:
                if row > 1:
                    self.place_water(row - 2, col, "u", has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if self.matrix[row - 1, col - 1] == 0:  # Left of Middle not filled
                    if col == 1 or self.matrix[row - 1, col - 2] == 1:  # Water Left
                        self.place_piece(row - 1, col - 1, 6)  # place Left
                        if col == 8 or self.matrix[row - 1, col + 2] == 1:  # If there is water below or last row
                            self.place_piece(row - 1, col + 1, 7)  # place Right
                            self.remove_boat(3) # mark boat of 3 pieces as found
                    else:
                        self.place_piece(row - 1, col - 1, 9, originator=(row - 1, col, 8))  # place Undefined
                        self.infer_water(9, row - 1, col - 1)

                if self.matrix[row - 1, col + 1] == 0:  # right of middle not filled
                    if self.matrix[row - 1, col + 2] == 1 or col == 8:  # Water
                        self.place_piece(row - 1, col + 1, 7)  # becomes Right
                    else:
                        self.place_piece(row - 1, col + 1, 9, originator=(row - 1, col, 8))  # place Undefined
                        self.infer_water(9, row - 1, col + 1)

        if "d" in direction:
            if row < 8 and self.matrix[row + 1, col] == 9:  # if undefined
                two_down = self.matrix[row + 2, col]
                if two_down > 1:  # boat on the bottom of undefined ([M] or B)
                    self.replace_piece(row + 1, col, 3)  # replace above with Top
                    if not has_middles:
                        self.remove_boat(2)  # mark boat of 2p as found
                    else:
                        if two_down == 4:  # if has Bottom
                            self.remove_boat(2)  # mark boat of 2 pieces as found
                        else:
                            three_down = self.matrix[row + 3, col]
                            if three_down == 4:  # if has Top
                                self.remove_boat(3) # mark boat of 3 pieces as found
            ######
            if has_middles and row < 9 and self.matrix[row + 1, col] == 8:
                if row < 8:
                    self.place_water(row + 2, col, "d", has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if self.matrix[row + 1, col - 1] == 0:  # Left of Middle not filled
                    if col == 1 or self.matrix[row + 1, col - 2] == 1:  # Water Left
                        self.place_piece(row + 1, col - 1, 6)  # place Left
                        if col == 8 or self.matrix[row + 1, col + 2] == 1:  # If there is water below or last col
                            self.place_piece(row + 1, col + 1, 7)  # place Right
                            self.remove_boat(3)  # mark boat of 3 pieces as found
                    else:
                        self.place_piece(row + 1, col - 1, 9, originator=(row + 1, col, 8))  # place Undefined
                        self.infer_water(9, row + 1, col - 1)

                if self.matrix[row + 1, col + 1] == 0:  # not filled
                    if self.matrix[row + 1, col + 2] == 1 or col == 8:  # Water
                        self.place_piece(row + 1, col + 1, 7)  # place Right
                    else:
                        self.place_piece(row + 1, col + 1, 9, originator=(row + 1, col, 8))  # place Undefined
                        self.infer_water(9, row + 1, col + 1)

        return

    def decrement_row(self, row_no: int):
        """Decrements row number by 1."""
        pieces_left = self.rows_left[row_no]
        self.rows_left[row_no] = pieces_left - 1

        if pieces_left == 1:
            self.fill_row_with_water(row_no)
        if pieces_left <= 0:  # TODO: check if this is correct
            raise Exception("Integrity check failed: row has too many pieces")

        return

    def decrement_column(self, col_no: int):
        """Decrements column number by 1."""
        pieces_left = self.columns_left[col_no]
        self.columns_left[col_no] = pieces_left - 1

        if pieces_left == 1:
            self.fill_col_with_water(col_no)
        if pieces_left <= 0:  # TODO: check if this is correct
            raise Exception("Integrity check failed: row has too many pieces")

        return

    def get_value(self, row: int, col: int) -> str:
            """Devolve o valor na respetiva posição do tabuleiro."""
            # TODO
            pass

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        pass

    @staticmethod
    def translate_to_int(hint: str) -> int:
        """Traduz uma pista para um inteiro."""

        if hint == "W":  # Water
            return 1
        if hint == "C":  # Circle
            return 2
        if hint == "T":  # Top
            return 3
        if hint == "B":  # Bottom
            return 4
        if hint == "M":  # Middle
            return 8
        if hint == "L":  # Left
            return 6
        if hint == "R":  # Right
            return 7
        """
        if hint == "undef": // internal use
            return 9
        """

        raise ValueError("Hint not valid")

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """

        boats_left = [4, 3, 2, 1]
        # init matrix
        matrix = np.zeros((10, 10), dtype=np.ubyte)

        # read rows and columns
        rows = [int(i) for i in input().split()[1:]]
        columns = [int(i) for i in input().split()[1:]]

        # read hints
        hint_no = int(input())
        hints = []
        for i in range(hint_no):
            hint = input().split()[1:]  # [row, col, hint]
            hint[0] = int(hint[0])
            hint[1] = int(hint[1])
            hint[2] = Board.translate_to_int(hint[2])
            hints.append(hint)

        hints.sort(key=lambda x: x[2])

        return Board(rows, columns, boats_left, matrix, True, hints)

    def infer_water(self, piece, row_no, col_no, has_middles=True):
        if piece == 1:  # water
            return
        else:
            if row_no > 0:
                if col_no > 0:
                    self.place_water(row_no - 1, col_no - 1, "lu", has_middles)
                if col_no < 9:
                    self.place_water(row_no - 1, col_no + 1, "ru", has_middles)
            if row_no < 9:
                if col_no > 0:
                    self.place_water(row_no + 1, col_no - 1, "ld", has_middles)
                if col_no < 9:
                    self.place_water(row_no + 1, col_no + 1, "rd", has_middles)

            if piece == 8 or piece == 9:  # middle or # undefined
                return

            if piece != 4 and row_no > 0:  # not Bottom and not first row
                self.place_water(row_no - 1, col_no, "u", has_middles)

            if piece != 3 and row_no < 9:  # not Top and not last row
                self.place_water(row_no + 1, col_no, "d", has_middles)

            # add L and R
            if piece != 7 and col_no > 0:  # not Right
                self.place_water(row_no, col_no - 1, "l", has_middles)
                if piece == 6:  # left
                    return

            if col_no < 9:
                self.place_water(row_no, col_no + 1, "r", has_middles)

        return

    def get_max_boat_size(self) -> int:
        """Devolve o tamanho máximo de barco que ainda pode ser colocado."""
        # get max available boat size
        for i in range(len(self.boats_left)):
            if self.boats_left[3 - i] > 0:
                return 4 - i  # max boat size

    def actions(self):
        """Devolve uma lista de ações"""
        # get max available boat size
        max_boat = self.get_max_boat_size()  # max boat size

        if self.candidate_actions:
            return self.candidate_actions[0][1]
        else:
            # init actions
            actions = []
            # (row_lu, col_lu, size, dir)   dir = true -> horizontal, dir = false -> vertical
            for i in range(10):  # for each row
                if self.rows_left[i] >= max_boat:  # has space for max_boat
                    no_consecutive_squares = 0
                    cols = 0
                    cols_with_middle = []
                    while cols < 10:       # for each column in the row
                        # check if square is empty or if it is a middle square after an empty one
                        # (if middle belongs to vertical boat, it'll be next to water and no_cons_sq = 0
                        if self.matrix[i][cols] == 0:
                            no_consecutive_squares += 1
                        elif no_consecutive_squares > 0 and self.matrix[i][cols] == 8:  # if there's middle
                            no_consecutive_squares += 1
                            cols_with_middle.append(cols)
                        else:
                            no_consecutive_squares = 0
                        cols += 1
                        if no_consecutive_squares >= max_boat and cols not in cols_with_middle and \
                                                        cols - max_boat not in cols_with_middle:  # not ending in a Middle
                            actions.append((i, cols - max_boat, max_boat, True))

                if self.columns_left[i] >= max_boat:
                    no_consecutive_squares = 0
                    row = 0
                    rows_with_middle = []
                    while row < 10:
                        if self.matrix[row][i] == 0:
                            no_consecutive_squares += 1
                        elif no_consecutive_squares > 0 and self.matrix[row][i] == 8:
                            no_consecutive_squares += 1
                            rows_with_middle.append(row)
                        else:
                            no_consecutive_squares = 0
                        row += 1
                        if no_consecutive_squares >= max_boat and row not in rows_with_middle and row-max_boat not in rows_with_middle:
                            actions.append((row - max_boat, i, max_boat, False))

        return actions

    def place_and_check(self, row_no, col_no, piece):
        """Place piece in matrix and check if it needs to replace"""
        prev_piece = self.matrix[row_no][col_no]
        if prev_piece == 0:
            self.place_piece(row_no, col_no, piece)
            self.infer_water(piece, row_no, col_no)
        elif prev_piece == 9:
            self.replace_piece(row_no, col_no, piece)
            self.infer_water(piece, row_no, col_no)
        elif prev_piece == piece:
            pass
        else:
            raise ValueError("place_and_check: Another piece already placed in that position")
        return

    def update_candidates(self):
        if self.candidate_actions:
            self.candidate_actions.pop(0)
        return

    def place_boat(self, action):
        """ action = (top left row, top left col, size, horizontal?)"""

        # for different sizes
        if action[2] == 1:
            self.place_and_check(action[0], action[1], 2)  # place circle
        elif action[2] == 2:
            if action[3]:  # If horizontal
                self.place_and_check(action[0], action[1], 6)  # place left
                self.place_and_check(action[0], action[1] + 1, 7)  # place left
            else:
                self.place_and_check(action[0], action[1], 3)  # place left
                self.place_and_check(action[0] + 1, action[1], 4)  # place left
        elif action[2] == 3:
            if action[3]:   # If Horizontal
                self.place_and_check(action[0], action[1], 6)       # place Left
                self.place_and_check(action[0], action[1] + 1, 8)   # place Middle
                self.place_and_check(action[0], action[1] + 2, 7)   # place Right
            else:           # if Vertical
                self.place_and_check(action[0], action[1], 3)       # place Top
                self.place_and_check(action[0] + 1, action[1], 8)   # place Middle
                self.place_and_check(action[0] + 2, action[1], 4)   # place Bottom
        else:       # size = 4
            if action[3]:   # If Horizontal
                self.place_and_check(action[0], action[1], 6)       # place Left
                self.place_and_check(action[0], action[1] + 1, 8)   # place Middle
                self.place_and_check(action[0], action[1] + 2, 8)   # place Middle
                self.place_and_check(action[0], action[1] + 3, 7)   # place Right
            else:
                self.place_and_check(action[0], action[1], 3)       # place Top
                self.place_and_check(action[0] + 1, action[1], 8)   # place Middle
                self.place_and_check(action[0] + 2, action[1], 8)   # place Middle
                self.place_and_check(action[0] + 3, action[1], 4)   # place Bottom

        self.remove_boat(action[2])

        return


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        return state.board.actions()


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = state.board.copy()

        new_board.place_boat(action)
        new_board.update_candidates()

        return BimaruState(new_board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        for i in state.board.boats_left:
            if i:
                return False

        for i in range(4):
            if state.board.boats_left[i] != 0:
                return False
            if state.board.rows_left[i] != 0:
                return False
            if state.board.columns_left[i] != 0:
                return False

        for i in range(4, 10):
            if state.board.rows_left[i] != 0:
                return False
            if state.board.columns_left[i] != 0:
                return False

        return True



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    board = Board.parse_instance()
    problem = Bimaru(board)
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    goal_node = depth_first_tree_search(Bimaru(board))

    # Imprimir para o standard output no formato indicado.



