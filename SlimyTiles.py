import sys
import pygame_sdl2 as pygame
from Tile import Tile
from Board import Board, EMPTY


if not pygame.font:
    print('Fatal Error: Pygame fonts disabled.')
    sys.exit()

KEY_TO_CHAR = {
    pygame.K_a: 'a',
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd'
}
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 0)
INSTRUCTIONS_COLOR = (150, 220, 100)
LABELS_COLOR = (0, 0, 0)
GRID_THICKNESS = 2
TILES_PER_LINE = 3
IMAGE_SIZE = 512
TEXT_BOX_HEIGHT = 50


class SlimyTiles:
    '''The main SlimyTiles class: This class handles the initialisation and
    creating of the game'''

    def __init__(self, tiles_per_line=TILES_PER_LINE):

        pygame.init()

        self.width = IMAGE_SIZE - IMAGE_SIZE % tiles_per_line \
            + (tiles_per_line - 1) * GRID_THICKNESS
        self.height = IMAGE_SIZE - IMAGE_SIZE % tiles_per_line \
            + (tiles_per_line - 1) * GRID_THICKNESS \
            + TEXT_BOX_HEIGHT

        self.tiles = [[None for x in range(TILES_PER_LINE)]
                      for y in range(TILES_PER_LINE)]
        self.board = Board(TILES_PER_LINE)

        self.instructions_font = None
        self.labels_font = None

        # Create the screen
        # set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
        self.screen = pygame.display.set_mode((self.width, self.height))

    def go(self):
        '''This is the main game method'''

        self.make_tiles()
        self.board.makePuzzle(self.tiles)

        # Create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(BACKGROUND_COLOR)

        # Define fonts
        self.instructions_font = pygame.font.SysFont('silom', 24)
        self.labels_font = pygame.font.SysFont('impact', 80)

        # Initial valid moves
        empty_slot, valid_moves = self.board.getMoves()
        self.board.printPuzzle()

        # The main game loop contains all in-game actions
        changed = True
        while True:

            # Event handling
            for event in pygame.event.get():

                if event.type == pygame.QUIT \
                   or event.type == pygame.KEYDOWN \
                   and event.key == pygame.K_ESCAPE:
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key in KEY_TO_CHAR:
                    move_index = self.label_to_int(KEY_TO_CHAR[event.key])
                    if 0 <= move_index < len(valid_moves):
                        self.board.makeMove(valid_moves[move_index])
                        empty_slot, valid_moves = self.board.getMoves()
                        self.board.printPuzzle()
                        changed = True

            # Rendering, if refresh needed
            if changed:
                self.render(valid_moves)
                changed = False

    def render(self, valid_moves):
        # 1) Background
        self.screen.blit(self.background, (0, 0))

        # 2) Tiles
        for piece in self.board.puzzle:
            if piece['tile_index'] != EMPTY:
                tile = piece['tile']
                self.screen.blit(tile.surface, tile.rect)

        # 3) Grid
        self.draw_grid()

        # 4) Text
        if pygame.font:

            # On the grid: tile labels
            labels = [self.int_to_label(i) for i in range(len(valid_moves))]
            for l, m in zip(labels, valid_moves):
                t = self.board.getTileFromPosition(m)
                text = self.labels_font.render(l, True, LABELS_COLOR)
                text_pos = text.get_rect(
                    centerx=t.rect.x + t.rect.width/2,
                    centery=t.rect.y + t.rect.height/2
                )
                self.screen.blit(text, text_pos)

            # At the bottom: possible moves
            s = 'You can move tiles ' + \
                ' or '.join([', '.join(labels[:-1]), labels[-1]])
            text = self.instructions_font.render(s, True, INSTRUCTIONS_COLOR,
                                                 BACKGROUND_COLOR)
            text_pos = text.get_rect(
                centerx=self.width / 2,
                centery=self.height - TEXT_BOX_HEIGHT/2
            )
            self.screen.blit(text, text_pos)

        pygame.display.flip()

    def int_to_label(self, i):
        return chr(i + ord('a'))

    def label_to_int(self, c):
        return ord(c) - ord('a')

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

        tile_width = IMAGE_SIZE / TILES_PER_LINE
        tile_height = IMAGE_SIZE / TILES_PER_LINE

        # Horizontal lines
        for i in range(1, len(self.tiles)):
            points = [
                (0, i * tile_height + (i-1) * GRID_THICKNESS),
                (self.width, i * tile_height + (i-1) * GRID_THICKNESS)
            ]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)
        # Vertical lines
        for j in range(1, len(self.tiles[0])):
            points = [
                (j * tile_width + (j-1) * GRID_THICKNESS, 0),
                (j * tile_width + (j-1) * GRID_THICKNESS, self.width)
            ]
            pygame.draw.lines(self.screen, GRID_COLOR,
                              closed, points, GRID_THICKNESS)


if __name__ == '__main__':
    MainWindow = SlimyTiles()
    MainWindow.go()
