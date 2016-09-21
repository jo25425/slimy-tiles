from math import floor
from random import randint

EMPTY = '_'


class Board:

    def __init__(self, n, empty='_'):
        self.n = n
        self.puzzle = []

        def initLegalMoves(n):
            moves = {}
            for i in range(n**2):
                neighbours = []
                i_x, i_y = i % n, floor(i / n)
                if i_x > 0:  # right
                    neighbours.append(i-1)
                if i_x < n - 1:  # left
                    neighbours.append(i+1)
                if i_y > 0:  # top
                    neighbours.append(i-n)
                if i_y < n - 1:  # bottom
                    neighbours.append(i+n)
                moves[i] = tuple(sorted(neighbours))
            return moves

        def initManhattanTable(n):
            table = {}
            for i in range(n**2):
                for j in range(n**2):
                    i_x, j_x = i % n, j % n
                    i_y, j_y = floor(i / n), floor(j / n)
                    col_delta, row_delta = abs(i_x - j_x), abs(i_y - j_y)
                    table[(i, j)] = col_delta + row_delta
            return table

        self.legal_moves = initLegalMoves(self.n)
        self.man_table = initManhattanTable(self.n)

    def manhattan(self, a, b):
        return self.man_table.get((a, b))

    def makePuzzle(self, tiles):
        for i, row in enumerate(tiles):
            for j, tile in enumerate(row):
                self.puzzle.append({
                    'tile': tile,
                    'tile_index': i*self.n + j
                })
        self.puzzle[randint(0, self.n)]['tile_index'] = EMPTY
        return self.puzzle

    def printPuzzle(self):
        for i in range(self.n):
            tile_indexes = [str(self.puzzle[i*self.n + j]['tile_index'])
                            for j in range(self.n)]
            print('{1}{0}{1}'.format('|'.join(tile_indexes), '|'))
        print('')

    def findEmpty(self):
        for i, piece in enumerate(self.puzzle):
            if piece['tile_index'] == EMPTY:
                return i
        return None

    def getMoves(self):
        empty = self.findEmpty()
        return empty, self.legal_moves[empty]

    def makeMove(self, move):
        empty = self.findEmpty()
        if move in self.legal_moves[empty]:
            tmp_piece = self.puzzle[move]
            tmp_rect = tmp_piece['tile'].rect
            tmp_piece['tile'].rect = self.puzzle[empty]['tile'].rect
            # Make piece moving empty
            self.puzzle[move] = self.puzzle[empty]
            self.puzzle[move]['tile'].rect = tmp_rect
            # Fill empty with moving piece
            self.puzzle[empty] = tmp_piece

# def cost(board, depth):
#     # estimate future cost by sum of tile displacements
#     future = 0
#     for pos in range(N**2):
#         occupant = board[pos]
#         if occupant != EMPTY:
#             correct_pos = BASIC_CONFIGURATION.index(occupant)
#             displacement = manhattan(pos, correct_pos)
#             future += displacement
#     past = depth
#     return past + future*3
