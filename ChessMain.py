'''
Driver File, responsible for user input and diplaying the current GameState object.
'''

import pygame as p
from ChessEngine import GameState, Move   # * it call everything.
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
The main driver for our code, will handle user input and ipdating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    
    loadImages() # only once, before the while loop
    running = True
    sqSelected = () # no square is selected, keep track os the last click of the user. (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples:[(7, 4), (4, 4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0] // sq_size
                row = location[1] // sq_size
                
                if sqSelected == (row, col): #the user clicked the same square twice 
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:        
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    
                if len(playerClicks) == 2: #after 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if (gs.whiteToMove and move.pieceMoved[0] == 'w') and (not gs.whiteToMove and move.pieceMoved[0] == 'b'): #adicionado depois
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                        sqSelected = () #reset user clicks
                        playerClicks = []
                    else: playerClicks = [sqSelected] #adicionado depois
                    
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                              
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
            
            
                                      
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()
    
'''
Responsible for all graphics within a current game state.
'''
    
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on board
    #add in piece highlighting or move suggestion(later)
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
Draw the pieces on the board using the current GameState.board
'''    
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != '--': #not a empty square
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


if __name__ == '__main__':
    main()