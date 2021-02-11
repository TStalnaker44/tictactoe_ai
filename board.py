

class Board():

    def __init__(self):
        self._n = 3
        self._board = [["0" for x in range(3)] for x in range(3)]

    def reset(self):
        self._board = [["0" for x in range(3)] for x in range(3)]

    def getBoardState(self):
        return "".join([item for lyst in self._board for item in lyst])

    def getBoard(self):
        return self._board

    def isFreeSpace(self, space):
        row, column = space
        return self._board[row][column] == "0"

    def executeMove(self, move, mark):
        row, column = move
        self._board[row][column] = mark

    def __str__(self):
        n = self._n
        state = self.getBoardState()
        state = state.replace("1", "X")
        state = state.replace("2", "O")
        state = state.replace("0", " ")
        formatTemplate = ("%s|%s|%s\n-----\n"*3)[:-7]
        return (formatTemplate % (*list(state),))

    def isGameOver(self):
        if self.getWinner() != 0: return True
        for row in self._board:
            for entry in row:
                if entry == "0": return False
        return True

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
