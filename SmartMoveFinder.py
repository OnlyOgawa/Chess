import random

pieceScores = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
checkmate = 1000
stalemate = 0




def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -checkmate
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = checkmate
        elif gs.stalemate:
            score = 0
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if score > maxScore:
            score = maxScore
            bestMove = playerMove
    return bestMove



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