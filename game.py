import pygame, random, pickle
from enum import Enum
from board import Board
from bot import Bot

class PlayerOptions(Enum):
    HUMAN  = 1
    BOT    = 2
    RANDOM = 3

# Game Control Variables
PLAYER_X = PlayerOptions.BOT
PLAYER_O = PlayerOptions.BOT
GAMES = 1000
BOT_MOVE_DELAY = 1
LOAD_PRETRAINED = True

# Board Display Variables
BOARD_MARGIN = 100
TOP_MARGIN = 50
TILE_WIDTH = 150
LINE_WEIGHT = 2
TIME_BETWEEN_GAMES = 1

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
        dim = (TILE_WIDTH+(2*LINE_WEIGHT)) * tilesPerRow + BOARD_MARGIN * 2

        # Get the screen to display the game
        self._screen = pygame.display.set_mode((dim,dim))

        # Create an instance of the game clock
        self._gameClock = pygame.time.Clock()

        self._moveTimer = BOT_MOVE_DELAY
        self._resetTimer = TIME_BETWEEN_GAMES

        # Set up game objects
        self._board = Board()

        if LOAD_PRETRAINED:
            self.loadBots()
        else:
            self._x_bot = Bot()
            self._o_bot = Bot()
            self._x_bot.usePunish()
            self._o_bot.usePunish()

        self._turn = True

        self._gamesPlayed = 0
        self._wins = [0,0,0]

        # Create board tiles for display
        self.makeBoard()
        self._stats = StatsDisplay(self)

        self._running = True

    def saveBots(self):
        pickle.dump(self._x_bot, open("x.bot", "wb" ))
        pickle.dump(self._o_bot, open("o.bot", "wb" ))

    def loadBots(self):
        self._x_bot = pickle.load(open("x.bot", "rb" ))
        self._o_bot = pickle.load(open("o.bot", "rb" ))

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

        self._stats.draw(self._screen)
        
        # Flip the display to the screen
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            # Quit the game if the event is of type QUIT
            if (event.type == pygame.QUIT):
                self._running = False

            if self._turn and PLAYER_X == PlayerOptions.HUMAN:
                self.handlePlayerMove(event)
            if not self._turn and PLAYER_O == PlayerOptions.HUMAN:
                self.handlePlayerMove(event)

    def update(self):
        ticks = self._gameClock.get_time() / 1000

        if not self._board.isGameOver():
            if self._turn and PLAYER_X != PlayerOptions.HUMAN:
                self.handleAiTurn(PLAYER_X, ticks)                
            if not self._turn and PLAYER_O != PlayerOptions.HUMAN:
                self.handleAiTurn(PLAYER_O, ticks)
        else:
            if self._gamesPlayed < GAMES:
                if self._resetTimer <= 0:
                    self.handleGameEnd()
                else:
                    self._resetTimer -= ticks

    def handleGameEnd(self):
        winner = self._board.getWinner()
        self.executeLearning(winner)
        self._wins[winner] += 1
        self._gamesPlayed += 1
        self._stats.update()
        self.resetGame()
        self._resetTimer = TIME_BETWEEN_GAMES

    def executeLearning(self, winner):
        self._x_bot.learn(winner==1 or winner==0)
        self._o_bot.learn(winner==2 or winner==0)
                
    def resetGame(self):
        self._board.reset()
        self.makeBoard()
        self._turn = True

    def handleAiTurn(self, player, ticks):
        if self._moveTimer <= 0:
            if player == PlayerOptions.RANDOM:
                move = self.getRandomMove()
            if player == PlayerOptions.BOT:
                if self._turn:
                    move = self.getBotMove(self._x_bot)
                else:
                    move = self.getBotMove(self._o_bot)
            self.executeMove(move)
            self._moveTimer = BOT_MOVE_DELAY
        else:
            self._moveTimer -= ticks

    def executeMove(self, move):
        mark = "X" if self._turn else "O"
        self._board.executeMove(move, mark)
        self.makeBoard()
        self._turn = not self._turn

    def makeBoard(self):
        tiles = []
        for i in range(3):
            for j in range(3):
                x = (TILE_WIDTH * (j)) + BOARD_MARGIN
                y = (TILE_WIDTH * (i)) + TOP_MARGIN
                mark = self._board._board[j][i]
                tiles.append(BoardTile((x,y), mark))
        self._tiles = tiles

    def getBotMove(self, bot):
        return bot.pickMove(self._board.getBoardState())

    def getRandomMove(self):
        while True:
            move = (random.randint(0,2), random.randint(0,2))
            if self._board.isFreeSpace(move):
                return move

class BoardTile():

    def __init__(self, pos, mark=0):
        self._pos = pos
        self._image = pygame.Surface((TILE_WIDTH + LINE_WEIGHT*2,
                                      TILE_WIDTH + LINE_WEIGHT*2))
        self._image.fill((0,0,0))
        move = pygame.Surface((TILE_WIDTH , TILE_WIDTH))
        move.fill((255,255,255))
        font = pygame.font.SysFont("Times New Roman", 40)
        if mark == "0": mark = " "
        t = font.render(mark, True, (0,0,0))
        x_pos = (TILE_WIDTH // 2) - (t.get_width() // 2)
        y_pos = (TILE_WIDTH // 2) - (t.get_height() // 2)
        move.blit(t, (x_pos,y_pos))
        self._image.blit(move, (LINE_WEIGHT, LINE_WEIGHT))

    def draw(self, screen):
        screen.blit(self._image, self._pos)

class StatsDisplay():

    def __init__(self, game):

        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._game = game
        self._top = (TILE_WIDTH+(2*LINE_WEIGHT)) * 3 + TOP_MARGIN
        self.update()

    def draw(self, screen):

        # Draw Total Games Played
        x = (screen.get_width() // 2) - (self._played.get_width() // 2)
        screen.blit(self._played, (x, self._top))

        # Draw X's Wins
        x = (screen.get_width() // 2) - (self._xwins.get_width() // 2)
        y = self._top + self._played.get_height() + 5
        screen.blit(self._xwins, (x, y))

        # Draw O's Wins
        x = (screen.get_width() // 2) - (self._owins.get_width() // 2)
        y += self._xwins.get_height() + 5
        screen.blit(self._owins, (x, y))

        # Draw the draws
        x = (screen.get_width() // 2) - (self._draws.get_width() // 2)
        y += self._owins.get_height() + 5
        screen.blit(self._draws, (x, y))

    def update(self):

        total = max(1, self._game._gamesPlayed)

        # Format Total Games Played
        text = ("Games Played: %d" % (self._game._gamesPlayed,))
        self._played = self._font.render(text, True, (0,0,0))

        # Format X wins
        text = ("X Wins: %d - %.2f%%" % (self._game._wins[1],
                                       (self._game._wins[1]/total)*100))
        self._xwins = self._font.render(text, True, (0,0,0))

        # Format O wins
        text = ("O Wins: %d - %.2f%%" % (self._game._wins[2],
                                       (self._game._wins[2]/total)*100))
        self._owins = self._font.render(text, True, (0,0,0))

        # Format draws
        text = ("Draws: %d - %.2f%%" % (self._game._wins[0],
                                      (self._game._wins[0]/total)*100))
        self._draws = self._font.render(text, True, (0,0,0))


def main():
    game = Game()
    game.gameLoop()
    
if __name__ == "__main__":
    main()
