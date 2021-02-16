
import random, pickle, time
from enum import Enum
from board import Board
from bot import Bot

class PlayerOptions(Enum):
    HUMAN  = 1
    BOT    = 2
    RANDOM = 3

# Control Flags
SILENT = True
PLAYER_X = PlayerOptions.BOT
PLAYER_O = PlayerOptions.BOT
GAMES = 100000
LOAD_PRETRAINED = True
SAVE_TRAINING = True
BOT_MOVE_DELAY = 0

class Driver():

    def __init__(self):
        
        self._game = Board()
        
        self._x_bot = Bot()
        self._o_bot = Bot()
        #self._x_bot.useReward()
        self._x_bot.usePunish()
        #self._o_bot.useReward()
        self._o_bot.usePunish()

        self._turn = True
        self._wins = [0,0,0]

    def resetGame(self):
        self._game.reset()
        self._turn = True

    def gameLoop(self, silent=False):
        
        if not silent: print(self._game, end="\n\n")

        while not self._game.isGameOver():

            # Display whose turn it is
            mark = "X" if self._turn else "O"
            if not silent: print("%s's Turn:" % (mark,))

            if mark == "X":
                if PLAYER_X == PlayerOptions.HUMAN:
                    move = self.getPlayerMove()
                elif PLAYER_X == PlayerOptions.BOT:
                    move = self.getBotMove(self._x_bot)
                    time.sleep(BOT_MOVE_DELAY)
                elif PLAYER_X == PlayerOptions.RANDOM:
                    move = self.getRandomMachineMove()
                    time.sleep(BOT_MOVE_DELAY)
            else:
                if PLAYER_O == PlayerOptions.HUMAN:
                    move = self.getPlayerMove()
                elif PLAYER_O == PlayerOptions.BOT:
                    move = self.getBotMove(self._o_bot)
                    time.sleep(BOT_MOVE_DELAY)
                elif PLAYER_O == PlayerOptions.RANDOM:
                    move = self.getRandomMachineMove()
                    time.sleep(BOT_MOVE_DELAY)

            # Carry out the move
            if move == None: break
            self._game.executeMove(move, mark)

            # Alternate turns
            self._turn = not self._turn

            if not silent: print(self._game, end="\n\n")
            
    def handleGameEnd(self, silent=False):
        winner = self._game.getWinner()
        self.executeLearning(winner)
        if not silent: self.showResults(winner)
        self._wins[winner] += 1

    def executeLearning(self, winner):
        self._x_bot.learn(winner==1 or winner==0)
        self._o_bot.learn(winner==2 or winner==0)
        #print(len(self._o_bot._brain))

    def showResults(self, winner):
        if winner ==  0:
           print("It was a draw!")
        else:
            mark = "X" if winner==1 else "O"
            print("%s has won!" % (mark))
        
    def getPlayerMove(self):
        # Collect user input until valid
        while True:
            # Get move from user
            print("What is your move?")
            row = int(input("Row: "))
            column = int(input("Column: "))
            if 0 <= row <= 2 and 0 <= column <= 2:
                if self._game.isFreeSpace((row, column)):
                    return (row, column)
                print("The space (%d,%d) is not available" % (row, column))
            else:
                print("The move (%d,%d) is not valid" % (row, column))

    def getRandomMachineMove(self):
        while True:
            move = (random.randint(0,2), random.randint(0,2))
            if self._game.isFreeSpace(move):
                return move

    def getBotMove(self, bot):
        return bot.pickMove(self._game.getBoardState())

    def showEndResults(self):
        totalGames = sum(self._wins)
        def calculatePercent(i):
            return (i / totalGames) * 100
        print("Total Games: %d" % (totalGames,))
        labels = ["Draws","X Wins","O Wins"]
        for x in range(3):
            print("%-6s: %2d%% - %d" % (labels[x],
                                        calculatePercent(self._wins[x]),
                                        self._wins[x]))

    def saveBots(self):
        pickle.dump(self._x_bot, open("x.bot", "wb" ))
        pickle.dump(self._o_bot, open("o.bot", "wb" ))

    def loadBots(self):
        self._x_bot = pickle.load(open("x.bot", "rb" ))
        self._o_bot = pickle.load(open("o.bot", "rb" ))

    def getXBot(self):
        return self._x_bot

    def getOBot(self):
        return self._o_bot



def main():
    d = Driver()
    if LOAD_PRETRAINED:
        d.loadBots()
    for _ in range(GAMES):
        d.gameLoop(SILENT)
        d.handleGameEnd(SILENT)
        d.resetGame()
        if not SILENT:
            print("\n" + "-"*20 + "\n")
    d.showEndResults()
    if SAVE_TRAINING:
        d.saveBots()

if __name__ == "__main__":
    main()
        

    
    
