# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys

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
                 matrix: np.ndarray((10, 10)), init=False, sorted_hints=[]):
        """O construtor deve receber os valores das pistas (rows_left e
        columns_left) e o tabuleiro (board) e inicializar as variáveis
        de instância."""
        self.rows_left = rows_left
        self.rows_to_fill = [10] * 10
        self.columns_left = columns_left
        self.columns_to_fill = [10] * 10
        self.boats_left = boats_left   # [1p,2p,3p,4p]
        self.matrix = matrix
        if init:
            self.initialize(sorted_hints)
        else:
            pass    # TODO

    """Representação interna de um tabuleiro de Bimaru."""

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

    # TODO: outros metodos da classe

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
    board = Board.parse_instance()
    #problem = Bimaru(board)
    goal_node = depth_first_tree_search(Bimaru(board))
    print(board.matrix)

    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
