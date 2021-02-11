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

        self._losingState = False

        self._reward = False
        self._punish = False

    def usePunish(self):
        self._punish = True

    def useReward(self):
        self._reward = True

    def pickMove(self, state):
        # Allow the bot to learn the moves naturally
        if not state in self._brain:
            self._brain[state] = self.getMoves(state)

        # Get the possible moves
        possibleMoves = self._brain[state]
        if possibleMoves == []:
            # Hope opponent doesn't play perfectly
            # and make a random move
            self._losingState = True
            possibleMoves = self.getMoves(state)
        move = random.choice(possibleMoves)
        if not self._losingState:
            self._lastMove = (state, move)
        return move

    def learn(self, won):
        if self._lastMove != None:
            state, move = self._lastMove
            if won:
                if self._reward:
                    for _ in range(3):
                        self._brain[state].append(move)
            else:
                if self._punish:
                    if move in self._brain[state]:
                        self._brain[state].remove(move)
        self._losingState = False

    def getMoves(self, state):
        moves = []
        n = 3
        for i, space in enumerate(state):
            if space == "0":
                #Add the move to the state
                row = i // n
                column = i % n
                moves.append((row, column))
        return moves



