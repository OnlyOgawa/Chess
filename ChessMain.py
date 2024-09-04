'''
Driver File, responsible for user input and diplaying the current GameState object.
'''

import pygame as p
from ChessEngine import GameState, Move # * it call everything.
from SmartMoveFinder import findRandomMove, findBestMove


colors = [p.Color('white'), p.Color('grey')]
width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}

'''
initialize a global dictionary of images, will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (sq_size, sq_size))
    #we can access an image by saying 'image['wp']'
        
'''
The main driver for our code, will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when we should animate a move
    loadImages() # only once, before the while loop
    running = True
    sqSelected = None # no square is selected, keep track os the last click of the user. (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples:[(7, 4), (4, 4)])
    playerOne = True #if human is playing white, then this is true. If AI is playing then its False.
    playerTwo = False #Same as playerOne, but for black.
    
    while running:
        humanTurn = (gs. whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanTurn:
                    location = p.mouse.get_pos() # (x, y) location of mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sqSelected == (row, col): #the user clicked the same square twice 
                        sqSelected = None #deselect
                        playerClicks = [] #clear player clicks
                    else:        
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                            sqSelected = None
                    
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    sqSelected = None
                    playerClicks = []
                    animate = False
                if e.key == p.K_r: #reset the board when 'r' is pressed.
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
#AI move finder.
        if not humanTurn:
            AIMove = findRandomMove(validMoves)
            if AIMove is None:
                AIMove = findBestMove(gs, validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            
                 
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(max_fps)
        p.display.flip()
    
'''
Highlight square selected and moves for piece selected
'''    

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected is not None and sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved.
#highlight selected square            
            s = p.Surface ((sq_size, sq_size))
            s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
#hightlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))
    
    
'''
Responsible for all graphics within a current game state.
'''
    
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of squares
    
'''
Draw the squares on the board. Top left square is always light(both perspectives).
'''
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('grey')]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    
'''
Draw the pieces on the board using the current GameState.board.
'''    
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != '--': #not a empty square.
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


'''
Animating a move.
'''

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square.
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
#erase the piece moved from its ending square.
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
#draw captured piece onto rectangle.
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
#draw moving piece.
        screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)
    
    


if __name__ == '__main__':
    main()