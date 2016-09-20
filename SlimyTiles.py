import sys
import pygame_sdl2 as pygame
from threading import Timer
from Tile import Tile
from Board import Board, EMPTY

GRID_COLOR = (255, 255, 0)
GRID_THICKNESS = 2
TILES_PER_LINE = 3
IMAGE_SIZE = 512


class SlimyTiles:
    '''The main SlimyTiles class: This class handles the initialisation and
    creating of the game'''

    def __init__(self,
                 width=(IMAGE_SIZE + (TILES_PER_LINE - 1) * GRID_THICKNESS),
                 height=(IMAGE_SIZE + (TILES_PER_LINE - 1) * GRID_THICKNESS)):
        pygame.init()

        self.width = width
        self.height = height
        self.tiles = [[None for x in range(TILES_PER_LINE)]
                      for y in range(TILES_PER_LINE)]
        self.board = Board(TILES_PER_LINE)

        # Create the screen
        # set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
        self.screen = pygame.display.set_mode((self.width, self.height))

    def go(self):
        '''This is the main game method'''

        self.make_tiles()
        self.board.makePuzzle(self.tiles)

        # Try out getting valid moves
        empty_slot, valid_moves = self.board.getMoves()
        print(empty_slot, valid_moves)

        # Create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # The main game loop contains all in-game actions
        while True:

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Rendering
            self.render()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.draw_grid()

        for piece in self.board.puzzle:
            if piece['tile_index'] != EMPTY:
                tile = piece['tile']
                self.screen.blit(tile.surface, tile.rect)

        pygame.display.flip()

    def make_tiles(self):
        tile_size = IMAGE_SIZE / TILES_PER_LINE

        for i in range(TILES_PER_LINE):
            for j in range(TILES_PER_LINE):
                rect_src = pygame.Rect(j * tile_size, i * tile_size,
                                       tile_size, tile_size)
                rect_dest = pygame.Rect(j * (tile_size + GRID_THICKNESS),
                                        i * (tile_size + GRID_THICKNESS),
                                        tile_size, tile_size)
                self.tiles[i][j] = Tile(rect_src, rect_dest)

    def draw_grid(self):
        closed = False

        tile_width = self.width / TILES_PER_LINE
        tile_height = self.height / TILES_PER_LINE

        # Horizontal lines
        for i in range(1, len(self.tiles)):
            points = [(0, i * tile_height), (self.width, i * tile_height)]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)
        # Vertical lines
        for j in range(1, len(self.tiles[0])):
            points = [(j * tile_width, 0), (j * tile_width, self.width)]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)


if __name__ == '__main__':
    MainWindow = SlimyTiles()
    MainWindow.go()
