'''
Responsible for storing all the information about the current state of a chess game, also responsible for determining the valid moves at the curret state, also keep a move log.
'''
class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters.
        #the first character represent the color of the piece, 'b', 'w'.
        #the second character represent the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'.
        #'--' represent the empty spaces.
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        self.whiteToMove = True
        self.moveLog = []
        

#Takes a Move as a parameter and executes it (this will not worl for castling, paw promotion and en-passant).
              
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap turn
        
        
# Undo the last move made.

    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns to black
            

    
#All moves considering checks.
    
    def getValidMoves(self):
        return self.getAllPossibleMoves() #modify later

#All moves without considering checks.

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rolls.
            for c in range(len(self.board[r])): #number of cols in giver row.
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #call the appropriate move function based on piece type
        return moves

#Get all the pawn moves for the pawn located at rol, col and add these moves to the list.

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves.
            if self.board[r-1][c] == '--': #1 square to advance.
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square pawn advance.
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #captures to the left.
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture.
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #capture to the right.
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture.
                    moves.append(Move((r, c), (r-1, c+1),self.board))
                   
                                
                                
#Get all the rook moves for the rook located at rol, col and add these moves to the list.

    def getRookMoves(self, r, c, moves):
        pass
    
#Get all the knight moves for the knight located at rol, col and add these moves to the list.

    def getKnightMoves(self, r, c, moves):
        pass
    
#Get all the bishop moves for the bishop located at rol, col and add these moves to the list.

    def getBishopMoves(self, r, c, moves):
        pass
    
#Get all the queen moves for the queen located at rol, col and add these moves to the list.

    def getQueenMoves(self, r, c, moves):
        pass
    
#Get all the king moves for the king located at rol, col and add these moves to the list.

    def getKingMoves(self, r, c, moves):
        pass

class Move():
    #maps keys to values
    #key : value
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRank = {v: k for k, v in ranksToRows.items()}
    filesToCol = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                  'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCol.items()}
            
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
                
#overriding the equals method
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
                        
                
                
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
                
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]
        
