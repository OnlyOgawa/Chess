import random

pieceScores = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
checkmate = 1000
stalemate = 0
DEPTH = 2



def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = checkmate
    bestPlayerMove = None
    
    random.shuffle(validMoves)  # Ensure the moves are shuffled for randomness
    
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -checkmate
        
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkmate:
                score = -checkmate
            elif gs.stalemate:
                score = stalemate
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        
        gs.undoMove()
    
    return bestPlayerMove


#helper method to make first recursive call
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    print("Initial valid moves:", validMoves)  # Debug print
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    print("Best move found:", nextMove)  # Debug print
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore



#positive score is good for white, negative score is good for black.
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return - checkmate #black wins.
        else:
            return checkmate #white wins.
    elif gs.stalemate:
        return stalemate
        
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -=pieceScores[square[1]]
    
    return score
    


#Score the borad based on material.
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -=pieceScores[square[1]]
    
    return score