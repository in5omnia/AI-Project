# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2
import numpy as np
import sys
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
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows_left: list, columns_left: list, boats: list, matrix: np.ndarray):

        self.rows_left = rows_left
        self.columns_left = columns_left
        self.boats_left = boats  # [1p, 2p, 3p, 4p]
        self.matrix = matrix
        return
        infer_matrix()

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

    def infer_matrix(self):
        #
        return

    @staticmethod
    def fill_row_with_water(row_no: int, matrix: np.ndarray, rows_left: list, cols_left: list, boats_left: list):
        """Enche linha/coluna de água."""
        ver = ""
        if row_no != 0:
            ver += "d"
        if row_no != 9:
            ver += "u"

        for i in range(10):
            pos = matrix[i, row_no]
            if pos == 0:  # if not filled
                boats_left, rows_left, cols_left = Board.place_water(i, row_no, ver, matrix, boats_left, rows_left, cols_left, True)


        """
        for i in range(10):
            pos = matrix[row_no, i]
            if pos == 0:  # if empty
                matrix[row_no, i] = 1  # turn into water
                # verify under and above
                if under:
                    pos_under = matrix[row_no + 1, i]
                    if pos_under == 8:  # if middle
                        matrix[row_no + 2, i] = 1  # turn into water - horizontal boat

                    elif pos_under == 9:  # if undefined
                        count = 0  # starts at 0 because of index
                        for add in range(1, 3):  # check if we're completing a boat
                            if matrix[row_no + 1 + add, i] == 4:  # bottom - boat is complete TODO: we are not checking boundaries
                                count += 1
                                matrix[row_no + 1, i] = 3  # becomes Top
                                boats_left[count] -= 1  # mark boat as found
                                break
                            elif matrix[row_no + 1 + add, i] == 8:  # middle - there is a boat
                                count += 1
                                matrix[row_no + 1, i] = 3  # becomes Top

                if above:
                    pos_above = matrix[row_no - 1, i]
                    if pos_above == 8:  # if middle
                        matrix[row_no - 2, i] = 1  # turn into water - horizontal boat
                    if pos_above == 9:  # undefined
                        count = 0  # starts at 0 because of index
                        for add in range(1, 3):  # check if we're completing a boat
                            if matrix[row_no - 1 - add, i] == 3:  # top - boat is complete
                                count += 1
                                matrix[row_no - 1, i] = 4  # becomes Bottom
                                boats_left[count] -= 1  # mark boat as found
                                break
                            elif matrix[row_no - 1 - add, i] == 8:  # middle - there is a boat
                                count += 1
                                matrix[row_no - 1, i] = 4  # becomes Bottom
        """

        return boats_left, rows_left, cols_left

    @staticmethod
    def fill_col_with_water(col_no: int, matrix: np.ndarray, rows_left: list, cols_left: list, boats_left: list):
        """Enche linha/coluna de água."""
        ver = ""
        if col_no != 0:
            ver += "l"
        if col_no != 9:
            ver += "r"

        for i in range(10):
            pos = matrix[i, col_no]
            if pos == 0:  # if not filled
                boats_left, rows_left, cols_left = Board.place_water(i, col_no, ver, matrix, boats_left, rows_left, cols_left, True)

                """
                matrix[i, col_no] = 1  # turn into water
                # verify under and above
                if right:
                    pos_right = matrix[i, col_no + 1]
                    if pos_right == 8:  # if middle
                        matrix[i, col_no + 2] = 1  # turn into water - horizontal boat
                        # TODO might be icky pk nem verificamos se ja la estava alguma coisa
                        #  (same em fill_row_with_water)
                    elif pos_right == 9:  # if undefined
                        count = 0  # starts at 0 because of index
                        for add in range(1, 3):  # check if we're completing a boat
                            if matrix[i, col_no + 1 + add] == 4:  # bottom - boat is complete TODO: we are not checking boundaries
                                count += 1
                                matrix[i, col_no + 1] = 3  # becomes Top
                                boats_left[count] -= 1  # mark boat as found
                                break
                            elif matrix[i, col_no + 1 + add] == 8:  # middle - there is a boat
                                count += 1
                                matrix[i, col_no + 1] = 3  # becomes Top

                if left:
                    pos_left = matrix[i, col_no - 1]
                    if pos_left == 8:  # if middle
                        matrix[i, col_no - 2] = 1  # turn into water - horizontal boat
                    if pos_left == 9:  # undefined
                        count = 0  # starts at 0 because of index
                        for add in range(1, 3):  # check if we're completing a boat
                            if matrix[i, col_no - 1 - add] == 3:  # top - boat is complete
                                count += 1
                                matrix[i, col_no - 1] = 4  # becomes Bottom
                                boats_left[count] -= 1  # mark boat as found
                                break
                            elif matrix[i, col_no - 1 - add] == 8:  # middle - there is a boat
                                count += 1
                                matrix[i, col_no - 1] = 4  # becomes Bottom
                """

        return boats_left, rows_left, cols_left

    @staticmethod
    def decrement_row(row_no: int, rows_left: list, matrix: np.ndarray, boats_left: list):
        """Decrementa o valor da linha em 1."""
        pieces_left = rows_left[row_no]
        rows_left[row_no] = pieces_left - 1

        if pieces_left == 1:
            boats_left = Board.fill_row_with_water(row_no, matrix, boats_left)
        if pieces_left <= 0:  # TODO: check if this is correct
            raise Exception("Integrity check failed: row has too many pieces")

        return rows_left, boats_left

    @staticmethod
    def decrement_column(col_no: int, columns_left: list, rows_left: list, matrix: np.ndarray, boats_left: list):
        """Decrementa o valor da coluna em 1."""
        pieces_left = columns_left[col_no]
        columns_left[col_no] = pieces_left - 1

        if pieces_left == 1:
            boats_left, columns_left, rows_left = Board.fill_col_with_water(col_no, matrix, rows_left, columns_left, boats_left)
        if pieces_left <= 0:  # TODO: check if this is correct
            raise Exception("Integrity check failed: column has too many pieces")
        return boats_left, rows_left, columns_left

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
    def infer_water(piece: int, r: int, c: int):
        """Inferir o posições de agua a partir de uma peça e a sua posição."""
        water_inference = []
        if piece == 1:  # water
            pass
        else:
            if r > 0:
                if c > 0:
                    water_inference.append((r - 1, c - 1, "ul"))
                if c < 9:
                    water_inference.append((r - 1, c + 1, "ur"))
            if r < 9:
                if c > 0:
                    water_inference.append((r + 1, c - 1, "dl"))
                if c < 9:
                    water_inference.append((r + 1, c + 1, "dr"))

            if piece == 8 or piece == 9:  # middle or # undefined
                return water_inference

            if piece != 4 and r > 0:  # not Bottom and not first row
                water_inference.append((r - 1, c, "u"))

            if piece != 3 and r < 9:  # not Top and not last row
                water_inference.append((r + 1, c, "d"))

            # add L and R
            if piece != 7 and c > 0:  # not Right
                water_inference.append((r, c - 1, "l"))
                if piece == 6:  # left
                    return water_inference

            if c < 9:
                water_inference.append((r, c + 1, "r"))

        return water_inference


    @staticmethod
    def place_water(row: int, col: int, direction: str, matrix: np.ndarray, boats_left: list, rows_left: list, cols_left: list, has_middles: bool = False):
        """ Coloca agua na posição indicada e faz inferência para a direção indicada."""

        # already placed
        if matrix[row, col] == 1:
            return boats_left, rows_left, cols_left

        # Place water
        matrix[row, col] = 1

        if "r" in direction:
            if col < 8:
                if matrix[row, col + 1] == 9:  # if undefined
                    two_right = matrix[row, col + 2]
                    if two_right > 1:  # boat on the right of undefined (M or R)
                        matrix[row, col + 1] = 6  # replace with Left
                        if not has_middles:
                            boats_left[1] -= 1  # mark boat of 2 pieces as found
                        else:
                            if two_right == 7:  # if has Right
                                boats_left[1] -= 1  # mark boat of 2 pieces as found
                            else:
                                three_right = matrix[row, col + 3]
                                if three_right == 7:  # if has Right
                                    boats_left[2] -= 1  # mark boat of 3 pieces as found

            if has_middles and col < 9 and matrix[row, col + 1] == 8:
                if col < 8:
                    boats_left, rows_left, cols_left = Board.place_water(row, col + 2, "r", matrix, boats_left, has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if matrix[row - 1, col + 1] == 0:  # above middle not filled
                    if row == 1 or matrix[row - 2, col + 1] == 1:  # Water above
                        matrix[row - 1, col + 1] = 3  # place Top
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                        if row == 8 or matrix[row + 2, col + 1] == 1:  # If there is water below or last row
                            matrix[row + 1, col + 1] = 4  # place Bottom
                            rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                            boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                            boats_left[2] -= 1   # mark boat of 3 pieces as found
                    else:
                        matrix[row - 1, col + 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row - 1, col + 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

                if matrix[row + 1, col + 1] == 0:  # below Middle not filled
                    if matrix[row + 2, col + 1] == 1 or row == 8:  # Water
                        matrix[row + 1, col + 1] = 4    # place Bottom
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                    else:
                        matrix[row + 1, col + 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row + 1, col + 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)



        if "l" in direction:
            if col > 1:
                if matrix[row, col - 1] == 9:  # if undefined
                    two_left = matrix[row, col - 2]
                    if two_left > 1:  # boat on the left of undefined ([M] or L)
                        matrix[row, col - 1] = 7  # place Right # TODO: boat
                        if not has_middles:
                            boats_left[2] -= 1  # mark boat as found
                        else:
                            if two_left == 6:  # if has Left
                                boats_left[1] -= 1  # mark boat of 2 pieces as found
                            else:
                                three_left = matrix[row, col - 3]
                                if three_left == 6:  # if has Left
                                    boats_left[2] -= 1  # mark boat of 3 pieces as found
            ######
            if has_middles and col > 0 and matrix[row, col - 1] == 8:
                if col > 1:
                    boats_left, rows_left, cols_left = Board.place_water(row, col - 2, "l", matrix, boats_left, rows_left, cols_left, has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if matrix[row - 1, col - 1] == 0:  # not filled
                    if row == 1 or matrix[row - 2, col - 1] == 1:  # Water above
                            matrix[row - 1, col - 1] = 3  # place Top
                            rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                            boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                            if row == 8 or matrix[row + 2, col - 1] == 1:  # If there is water below or last row
                                matrix[row + 1, col - 1] = 4  # place Bottom
                                rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                                boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                                boats_left[2] -= 1   # mark boat of 3 pieces as found
                    else:
                        matrix[row - 1, col - 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row - 1, col - 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)


                if matrix[row + 1, col - 1] == 0:  # not filled
                    if matrix[row + 2, col - 1] == 1 or row == 8:  # Water
                        matrix[row + 1, col - 1] = 4    # Place Bottom
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                    else:
                        matrix[row + 1, col - 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row + 1, col - 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

        if "u" in direction:
            if row > 1 and matrix[row - 1, col] == 9:  # if undefined
                two_up = matrix[row - 2, col]
                if two_up > 1:  # boat on the top of undefined ([M] or T)
                    matrix[row - 1, col] = 4  # place Bottom # TODO: boat
                    if not has_middles:
                        boats_left[2] -= 1  # mark boat as found
                    else:
                        if two_up == 3:  # if has Top
                            boats_left[1] -= 1  # mark boat of 2 pieces as found
                        else:
                            three_up = matrix[row - 3, col]
                            if three_up == 3:  # if has Top
                                boats_left[2] -= 1  # mark boat of 3 pieces as found
            ######
            if has_middles and row > 0 and matrix[row - 1, col] == 8:
                if row > 1:
                    boats_left, rows_left, cols_left = Board.place_water(row - 2, col, "u", matrix, boats_left, rows_left, cols_left, has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if matrix[row - 1, col - 1] == 0:  # Left of Middle not filled
                    if col == 1 or matrix[row - 1, col - 2] == 1:  # Water Left
                        matrix[row - 1, col - 1] = 6  # place Left
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        if col == 8 or matrix[row - 1, col + 2] == 1:  # If there is water below or last row
                            matrix[row - 1, col + 1] = 7  # place Right
                            rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                            boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                            boats_left[2] -= 1  # mark boat of 3 pieces as found
                    else:
                        matrix[row - 1, col - 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row - 1, col - 1):
                            boats_left, rows_left, columns_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

                if matrix[row - 1, col + 1] == 0:  # right of middle not filled
                    if matrix[row - 1, col + 2] == 1 or col == 8:  # Water
                        matrix[row - 1, col + 1] = 7  # becomes Right
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                    else:
                        matrix[row - 1, col + 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row - 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row - 1, col + 1):
                            boats_left, rows_left, columns_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

        if "d" in direction:
            if row < 8 and matrix[row + 1, col] == 9:  # if undefined
                two_down = matrix[row + 2, col]
                if two_down > 1:  # boat on the bottom of undefined ([M] or B)
                    matrix[row + 1, col] = 3  # replace Top with Top
                    if not has_middles:
                        boats_left[2] -= 1  # mark boat as found
                    else:
                        if two_down == 4:  # if has Bottom
                            boats_left[1] -= 1  # mark boat of 2 pieces as found
                        else:
                            three_down = matrix[row + 3, col]
                            if three_down == 4:  # if has Top
                                boats_left[2] -= 1  # mark boat of 3 pieces as found
            ######
            if has_middles and row < 9 and matrix[row + 1, col] == 8:
                if row < 8:
                    boats_left, rows_left, cols_left = Board.place_water(row + 2, col, "d", matrix, boats_left, rows_left, cols_left, has_middles)
                # Middle piece is vertical Boat - add undefined pieces above and below

                if matrix[row + 1, col - 1] == 0:  # Left of Middle not filled
                    if col == 1 or matrix[row + 1, col - 2] == 1:  # Water Left
                        matrix[row + 1, col - 1] = 6  # place Left
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        if col == 8 or matrix[row + 1, col + 2] == 1:  # If there is water below or last col
                            matrix[row + 1, col + 1] = 7  # place Right
                            rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                            boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                            boats_left[2] -= 1  # mark boat of 3 pieces as found
                    else:
                        matrix[row + 1, col - 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col - 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row + 1, col - 1):
                            boats_left, rows_left, columns_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

                if matrix[row + 1, col + 1] == 0:  # not filled
                    if matrix[row + 1, col + 2] == 1 or col == 8:  # Water
                        matrix[row + 1, col + 1] = 7  # place Right
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                    else:
                        matrix[row + 1, col + 1] = 9  # place Undefined
                        rows_left, boats_left = Board.decrement_row(row + 1, rows_left, matrix, boats_left)
                        boats_left, rows_left, cols_left = Board.decrement_column(col + 1, cols_left, rows_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, row + 1, col + 1):
                            boats_left, rows_left, columns_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, has_middles)

        return boats_left, rows_left, cols_left

    @staticmethod
    def infer_from_hints(hints: list, matrix: np.ndarray):
        # TODO
        pass


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
        rows_left = [int(i) for i in input().split()[1:]]
        cols_left = [int(i) for i in input().split()[1:]]

        # fill rows and columns with water if needed
        for i in range(10):
            if rows_left[i] == 0:
                boats_left, rows_left, cols_left = Board.fill_row_with_water(i, matrix, rows_left, cols_left, boats_left)
            if cols_left[i] == 0:
                boats_left, rows_left, cols_left = Board.fill_col_with_water(i, matrix, rows_left, cols_left, boats_left)

        hint_no = int(input())
        hints = []
        for i in range(hint_no):
            hint = input().split()[1:]  # [row, col, hint]
            hint[0] = int(hint[0])
            hint[1] = int(hint[1])
            hint[2] = Board.translate_to_int(hint[2])
            hints.append(hint)

        hints.sort(key=lambda x: x[2])  # sort by hint by type so that circles are first and middle last

        for hint in hints:
            # add piece & water inference to matrix
            piece = hint[2]
            prev_piece = matrix[hint[0], hint[1]]
            # TODO: checks prev piece for already counted boat
            if piece == prev_piece:  # already infered
                continue

            matrix[hint[0], hint[1]] = piece  # place hint piece regardless

            if piece == 1:  # if water don't check anything
                continue

            if piece != 8:  # if not middle
                if prev_piece == 9:  # if undefined
                    boats_left[1] -= 1  # it's a 2p boat

                elif piece == 3: # if Top
                    if hint[0] == 8 and matrix[hint[0] + 2, hint[1]] == 1: # if water 2 under or last row
                        matrix[hint[0] + 1, hint[1]] = 4  # place Bottom
                        boats_left[1] -= 1  # mark boat of 2 pieces as found
                    elif matrix[hint[0] + 1, hint[1]] == 9: # if undefined below
                        boats_left[2] -= 1  # it's a 3p boat
                        matrix[hint[0] + 1, hint[1]] = 8  # place Middle
                    elif matrix[hint[0] + 2, hint[1]] == 9:  # if undefined 2 squares below
                        boats_left[3] -= 1  # it's a 4p boat
                        matrix[hint[0] + 1: hint[0] + 3, hint[1]] = 8  # place Middles
                    else:
                        matrix[hint[0] + 1, hint[1]] = 9  # place Undefined
                        for r, c, dir in Board.infer_water(9, hint[0] + 1, hint[1]):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)

                elif piece == 4:    # if Bottom
                    if hint[0] == 1 and matrix[hint[0] - 2, hint[1]] == 1: # if water 2 above or first row
                        matrix[hint[0] - 1, hint[1]] = 3  # place Top
                        boats_left[1] -= 1  # mark boat of 2 pieces as found
                    elif matrix[hint[0] - 1, hint[1]] == 9: # if undefined below
                        boats_left[2] -= 1  # it's a 3p boat
                        matrix[hint[0] - 1, hint[1]] = 8  # place Middle
                    elif matrix[hint[0] - 2, hint[1]] == 9:  # if undefined 2 squares below
                        boats_left[3] -= 1  # it's a 4p boat
                        matrix[hint[0] - 1: hint[0] - 3, hint[1]] = 8  # place Middles
                    else:
                        matrix[hint[0] - 1, hint[1]] = 9  # place Undefined
                        for r, c, dir in Board.infer_water(9, hint[0] - 1, hint[1]):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)

                elif piece == 6:  # Left
                    if hint[1] == 8 and matrix[hint[0], hint[1] + 2] == 1:  # if water 2 left or last column
                        matrix[hint[0], hint[1] + 1] = 7  # place Right
                        boats_left[1] -= 1  # mark boat of 2 pieces as found
                    elif matrix[hint[0], hint[1] + 1] == 9:  # if undefined on the right
                        boats_left[2] -= 1  # it's a 3p boat
                        matrix[hint[0], hint[1] + 1] = 8  # place Middle
                    elif matrix[hint[0], hint[1] + 2] == 9:  # if undefined 2 squares on the right
                        boats_left[3] -= 1  # it's a 4p boat
                        matrix[hint[0], hint[1] + 1: hint[1] + 3] = 8  # place Middles
                    else:
                        matrix[hint[0], hint[1] + 1] = 9
                        for r, c, dir in Board.infer_water(9, hint[0], hint[1] + 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)

                elif piece == 7:  # Right
                    if hint[1] == 1 and matrix[hint[0], hint[1] - 2] == 1:  # if water 2 right or first column
                        matrix[hint[0], hint[1] - 1] = 6  # place Left
                        boats_left[1] -= 1  # mark boat of 2 pieces as found
                    elif matrix[hint[0], hint[1] - 1] == 9:  # if undefined on the left
                        boats_left[2] -= 1  # it's a 3p boat
                        matrix[hint[0], hint[1] - 1] = 8  # place Middle
                    elif matrix[hint[0], hint[1] - 2] == 9:  # if undefined 2 squares on the left
                        boats_left[3] -= 1  # it's a 4p boat
                        matrix[hint[0], hint[1] - 1: hint[1] - 3] = 8  # place Middles
                    else:
                        matrix[hint[0], hint[1] - 1] = 9
                        for r, c, dir in Board.infer_water(9, hint[0], hint[1] - 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)


                for r, c, dir in Board.infer_water(piece, hint[0], hint[1]):
                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left)

            else:       # if middle
                if prev_piece == 8:  # if Middle
                    continue
                # if first row or water above -> horizontal boat
                if hint[0] == 0 or matrix[hint[0] - 1, hint[1]] == 1 or hint[0] == 9 or matrix[hint[0] + 1, hint[1]] == 1:
                    if hint[0] == 0 or matrix[hint[0] - 1, hint[1]] == 1:
                        if hint[0] != 9:
                            boats_left, rows_left, columns_left = Board.place_water(hint[0] + 1, hint[1], "d", matrix, boats_left, rows_left, cols_left, True)
                    else:
                        boats_left, rows_left, columns_left = Board.place_water(hint[0] -1, hint[1], "u", matrix, boats_left, rows_left, cols_left, True)

                    right_piece = matrix[hint[0], hint[1] + 1]
                    left_piece = matrix[hint[0], hint[1] - 1]
                    if right_piece > 1:
                        if right_piece == 7:    # Right
                            if boats_left[3] == 0 or hint[1] == 1 or matrix[hint[0], hint[1] - 2] == 1:  # if no 4p boats left
                                boats_left[2] -= 1  # we can place a 3p boat
                                matrix[hint[0], hint[1] - 1] = 6 # place Left
                                for r, c, dir in Board.infer_water(6, hint[0], hint[1] - 1):
                                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        elif right_piece == 9:  # Undefined
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0], hint[1] + 1] = 8  # place Middle
                            matrix[hint[0], hint[1] - 1] = 6  # place Left
                            for r, c, dir in Board.infer_water(6, hint[0], hint[1] - 1):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:               # Middle
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0], hint[1] - 1] = 6  # place Left
                            matrix[hint[0], hint[1] + 2] = 7  # place Right
                            for r, c, dir in Board.infer_water(6, hint[0], hint[1] - 1):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                            for r, c, dir in Board.infer_water(7, hint[0], hint[1] + 2):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                    elif left_piece > 1:
                        if left_piece == 6:  # Left
                            if boats_left[3] == 0 or hint[1] == 8 or matrix[hint[0], hint[1] + 2] == 1:  # if no 4p boats left
                                boats_left[2] -= 1  # we can place a 3p boat
                                matrix[hint[0], hint[1] + 1] = 7  # place Right
                                for r, c, dir in Board.infer_water(7, hint[0], hint[1] + 1):
                                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        elif left_piece == 9:  # Undefined
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0], hint[1] - 1] = 8  # place Middle
                            matrix[hint[0], hint[1] + 1] = 7  # place Right
                            for r, c, dir in Board.infer_water(7, hint[0], hint[1] + 1):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:  # Middle
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0], hint[1] - 2] = 6  # place Left
                            matrix[hint[0], hint[1] + 1] = 7  # place Right
                            for r, c, dir in Board.infer_water(6, hint[0], hint[1] - 2):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                            for r, c, dir in Board.infer_water(7, hint[0], hint[1] + 1):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                    else:
                        matrix[hint[0], hint[1] - 1] = 9    # place Undefined
                        rows_left, boats_left = Board.decrement_row(hint[0], rows_left, matrix, boats_left)
                        cols_left, boats_left = Board.decrement_row(hint[1] - 1, cols_left, matrix, boats_left)
                        matrix[hint[0], hint[1] + 1] = 9    # place Undefined
                        rows_left, boats_left = Board.decrement_row(hint[0], rows_left, matrix, boats_left)
                        cols_left, boats_left = Board.decrement_row(hint[1] + 1, cols_left, matrix, boats_left)
                        for r, c, dir in Board.infer_water(9, hint[0], hint[1] - 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        for r, c, dir in Board.infer_water(9, hint[0], hint[1] + 1):
                            boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                # if first column or water to the left -> vertical boat
                elif hint[1] == 0 or matrix[hint[0], hint[1] - 1] == 1 or hint[1] == 9 or matrix[hint[0], hint[1] + 1] == 1:
                    # TODO place water to the right
                    if hint[1] == 0 or matrix[hint[0], hint[1] - 1] == 1:
                        if hint[1] != 9:
                            boats_left, rows_left, columns_left = Board.place_water(hint[0], hint[1] + 1, "r", matrix, boats_left, rows_left, cols_left, True)
                    else:
                        boats_left, rows_left, columns_left = Board.place_water(hint[0], hint[1] -1, "l", matrix, boats_left, rows_left, cols_left, True)

                    up_piece = matrix[hint[0] - 1, hint[1]]
                    down_piece = matrix[hint[0] + 1, hint[1]]
                    if up_piece > 1:
                        if up_piece == 3:   # Top
                            if boats_left[3] == 0 or hint[0] == 8 or matrix[hint[0] + 2, hint[1]] == 1:
                                boats_left[2] -= 1   # It's a 3p boat
                                matrix[hint[0] + 1, hint[1]] = 4 # place Bottom
                                for r, c, dir in Board.infer_water(4, hint[0] + 1, hint[1]):
                                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        elif up_piece == 9:     # Undefined
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0] - 1, hint[1]] = 8  # place Middle
                            matrix[hint[0] + 1, hint[1]] = 4  # place Bottom
                            for r, c, dir in Board.infer_water(4, hint[0] + 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:        # Middle
                            boats_left[3] -= 1   # it's a 4p boat
                            matrix[hint[0] - 2, hint[1]] = 3  # place Top
                            matrix[hint[0] + 1, hint[1]] = 4  # place Bottom
                            for r, c, dir in Board.infer_water(3, hint[0] - 2, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                            for r, c, dir in Board.infer_water(4, hint[0] + 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                    elif down_piece > 1:
                        if down_piece == 4:     # Bottom
                            if boats_left[3] == 0 or hint[0] == 1 or matrix[hint[0] - 2, hint[1]] == 1:
                                boats_left[2] -= 1  # It's a 3p boat
                                matrix[hint[0] - 1, hint[1]] = 3  # place Top
                                for r, c, dir in Board.infer_water(3, hint[0] - 1, hint[1]):
                                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        elif down_piece == 9:   # Undefined
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0] + 1, hint[1]] = 8    # Middle
                            matrix[hint[0] - 1, hint[1]] = 3    # Top
                            for r, c, dir in Board.infer_water(3, hint[0] - 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:    # Middle
                            boats_left[3] -= 1  # it's a 4p boat
                            matrix[hint[0] - 1, hint[1]] = 3 # place Top
                            matrix[hint[0] + 2, hint[1]] = 4  # place Bottom
                            for r, c, dir in Board.infer_water(4, hint[0] + 2, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                            for r, c, dir in Board.infer_water(3, hint[0] - 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                    else:
                        if hint[0] == 1 or matrix[hint[0] - 2, hint[1]] == 1:
                            matrix[hint[0] - 1, hint[1]] = 3    # Top
                            for r, c, dir in Board.infer_water(3, hint[0] - 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:
                            matrix[hint[0] - 1, hint[1]] = 9    # place Undefined
                            for r, c, dir in Board.infer_water(9, hint[0] - 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)

                        if hint[0] == 8 or matrix[hint[0] + 2, hint[1]] == 1:
                            matrix[hint[0] + 1, hint[1]] = 4    # Bottom
                            for r, c, dir in Board.infer_water(4, hint[0] + 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)
                        else:
                            matrix[hint[0] + 1, hint[1]] = 9    # place Undefined
                            for r, c, dir in Board.infer_water(9, hint[0] + 1, hint[1]):
                                boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)

                # Água da peça acabada de por
                for r, c, dir in Board.infer_water(piece, hint[0], hint[1]):
                    boats_left, rows_left, cols_left = Board.place_water(r, c, dir, matrix, boats_left, rows_left, cols_left, True)



            """
            # TODO: remove circles from boats_left
            for r, c in Board.infer_water(piece, hint[0], hint[1]):
                matrix[r, c] = 1  # water
            """
            # decrement rows and columns
            rows_left, boats_left = Board.decrement_row(hint[0], rows_left, matrix, boats_left)
            boats_left, rows_left, columns_left = Board.decrement_column(hint[1], cols_left, rows_left, matrix, boats_left)


        #matrix[1,5] = 0
        #Board.place_water(1+1, 5 + 1, "u", matrix, boats_left, True)
        #infer_from_hints(non_water_hints, matrix)
        return Board(rows_left, cols_left, boats_left, matrix)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    b = Board.parse_instance()
    print(b.matrix)

    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
