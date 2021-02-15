import pygame
from board import Board
from bot import Bot

BOARD_MARGIN = 100
TILE_WIDTH = 150
LINE_WEIGHT = 2

class Game():

    def __init__(self):

        # Initialize the module
        pygame.init()
        pygame.font.init()

        # Set the title of the window
        pygame.display.set_caption('Tic-Tac-Toe')

        # Set the tile dimensions and the margins around the board
        tilesPerRow = 3

        # Calculate an appropriate window size
        dim = TILE_WIDTH * tilesPerRow + BOARD_MARGIN * 2

        # Get the screen to display the game
        self._screen = pygame.display.set_mode((dim,dim))

        # Create an instance of the game clock
        self._gameClock = pygame.time.Clock()

        # Set up game objects
        self._board = Board()
        self._x_bot = Bot()
        self._o_bot = Bot()

        self._turn = True

        # Create board tiles for display
        self.makeBoard()

        self._running = True

    def gameLoop(self):
        while self._running:
            self._gameClock.tick()
            self.draw()
            self.handleEvents()
            self.update()
        pygame.quit()

    def draw(self):
        # Color the screen background
        self._screen.fill((150,240,255))

        # Draw the board tiles
        for t in self._tiles:
            t.draw(self._screen)
            
        # Flip the display to the screen
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            # Quit the game if the event is of type QUIT
            if (event.type == pygame.QUIT):
                self._running = False

    def update(self):
        ticks = self._gameClock.get_time() / 1000

    def makeBoard(self):
        tiles = []
        for i in range(3):
            for j in range(3):
                x = (TILE_WIDTH * (j)) + BOARD_MARGIN
                y = (TILE_WIDTH * (i)) + BOARD_MARGIN
                mark = self._board._board[j][i]
                tiles.append(BoardTile((x,y), int(mark)))
        self._tiles = tiles

class BoardTile():

    def __init__(self, pos, mark=0):
        self._pos = pos
        self._image = pygame.Surface((TILE_WIDTH + LINE_WEIGHT*2,
                                      TILE_WIDTH + LINE_WEIGHT*2))
        self._image.fill((0,0,0))
        move = pygame.Surface((TILE_WIDTH , TILE_WIDTH))
        move.fill((255,255,255))
        font = pygame.font.SysFont("Times New Roman", 20)
        if mark == 0: mark = " "
        elif mark == 1: mark = "X"
        else: mark = "O"
        t = font.render(mark, True, (0,0,0))
        x_pos = (TILE_WIDTH // 2) - (t.get_width() // 2)
        y_pos = (TILE_WIDTH // 2) - (t.get_height() // 2)
        move.blit(t, (x_pos,y_pos))
        self._image.blit(move, (LINE_WEIGHT, LINE_WEIGHT))

    def draw(self, screen):
        screen.blit(self._image, self._pos)


def main():
    game = Game()
    game.gameLoop()
    
if __name__ == "__main__":
    main()
