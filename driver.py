
import random
from board import Board
from bot import Bot

class Driver():

    def __init__(self):
        self._game = Board()
        self._x_bot = Bot()
        self._x_bot.useReward()
        self._x_bot.usePunish()
        self._o_bot = Bot()
        self._turn = True
        self._wins = [0,0,0]

    def resetGame(self):
        self._game.reset()

    def gameLoop(self, silent=False):
        
        if not silent: print(self._game)

        while not self._game.isGameOver():

            # Display whose turn it is
            mark = "X" if self._turn else "O"
            if not silent: print("%s's Turn:" % (mark,))

            if mark == "X":
                #move = self.getPlayerMove()
                move = self.getBotMove(self._x_bot)
            else:
                #move = self.getRandomMachineMove()
                move = self.getBotMove(self._o_bot)

            # Carry out the move
            if move == None: break
            self._game.executeMove(move, mark)

            # Alternate turns
            self._turn = not self._turn

            if not silent: print(self._game)
            
    def handleGameEnd(self, silent=False):
        winner = self._game.getWinner()
        self.executeLearning(winner)
        if not silent: self.showResults(winner)
        self._wins[winner] += 1

    def executeLearning(self, winner):
        self._x_bot.learn(winner==1)
        #self._o_bot.learn(winner==2)

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
        print("Total Games: %d" % (totalGames,))
        print("Draws: %d\nX Wins: %d\nO Wins: %d" % (self._wins[0],
                                                     self._wins[1],
                                                     self._wins[2]))

def main():
    d = Driver()
    for i in range(1000000):
        d.gameLoop(True)
        d.handleGameEnd(True)
        #if i % 1000 == 0: print(len(d._x_bot._brain))
        d.resetGame()
    d.showEndResults()

if __name__ == "__main__":
    main()
        

    
    
