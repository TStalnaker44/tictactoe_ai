"""
Board State represented as a string
 0 = Blank Space
 1 = Player One (X)
 2 = Player Two (O)

 Moves represented as (x,y)

"""
import pprint, random, math

class Bot():

    def __init__(self):
        self._brain = {}
        self._lastMove = None
        self._moveMemory = []
        self._forfeit = False

        self._reward = True
        self._punish = True
        self._longTermMemory = True

    def usePunish(self, punish):
        self._punish = punish

    def useReward(self, reward):
        self._reward = reward
        
    def useLongTermMemory(self, mem):
        self._longTermMemory = mem

    def pickMove(self, turn, state):
        # Allow the bot to learn the moves naturally
        if not turn in self._brain:
            self._brain[turn] = {}
        if not state in self._brain[turn]:
            self._brain[turn][state] = getMoves(state, turn)

        # Get the possible moves
        possibleMoves = self._brain[turn][state]
        if possibleMoves == []:
            self._forfeit = True
            #self._lastMove = None
            return None #The bot forfeits in losing state
        move = random.choice(possibleMoves)
        self._lastMove = (turn, state, move)
        self._moveMemory.append(self._lastMove)
        return move

    def learn(self, won):
        if self._lastMove != None:
            turn, state, move = self._lastMove
            if won:
                if self._reward:
                    if self._longTermMemory:
                        for memory in self._moveMemory:
                            turn, state, move = memory
                            for x in range(3):
                                self._brain[turn][state].append(move)
                        self._moveMemory = []
                    else:
                        for x in range(3):
                            self._brain[turn][state].append(move)
                        self._moveMemory = []
            else:
                if self._punish:
                    if move in self._brain[turn][state]:
                        self._brain[turn][state].remove(move)

class Board():

    def __init__(self):
        self._n = 3
        self._board = [["0" for x in range(3)] for x in range(3)]

    def getBoardState(self):
        return "".join([item for lyst in self._board for item in lyst])

    def executeMove(self, move, mark):
        x, y = move
        self._board[x][y] = mark

    def printBoard(self):
        n = self._n
        state = self.getBoardState()
        state = state.replace("1", "X")
        state = state.replace("2", "O")
        state = state.replace("0", " ")
        formatTemplate = ("%s|%s|%s\n-----\n"*3)[:-7]
        print(formatTemplate % (*list(state),))

    def isGameOver(self, turn):
        n = self._n
        if not "2" in self._board or \
           not "1" in self._board or \
           "2" in self._board[(n*n)-n:n*n] or \
           "1" in self._board[0:n] or \
           getMoves(self.getBoardState(), turn) == []:
            return True
        else:
            return False

    def getWinner(self):
        
        ## Check for three across
        state = self.getBoardState()
        for i in range(3):
            row = state[(i*3):(i+1)*3]
            if row == "XXX": return 1
            if row == "OOO": return 2
        
        ## Check for three down
        for column in range(len(self._board)):
          xCount = 0;
          oCount = 0;
          for row in range(len(self._board)):
            entry = self._board[row][column]
            if entry == "X":
              xCount += 1
            if entry == "O":
              oCount += 1
          if xCount == 3: return 1
          if oCount == 3: return 2
        
        ## Check the down diagonal
        xCount = 0
        oCount = 0
        for i in range(len(self._board)):
            entry = self._board[i][i]
            if entry == "X":
                xCount += 1
            if entry == "O":
                oCount += 1
        if xCount == 3: return 1
        if oCount == 3: return 2
        
        ## Check the up diagonal
        xCount = 0
        oCount = 0
        for row in range(len(self._board)):
            column = (len(self._board)-1) - row
            entry = self._board[row][column]
            if entry == "X":
                xCount += 1
            if entry == "O":
                oCount += 1
        if xCount == 3: return 1
        if oCount == 3: return 2
        return 0
