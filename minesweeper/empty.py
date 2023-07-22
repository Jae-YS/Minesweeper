import pygame as py
from .constants import DGREY, SQUARE_SIZE, BORDER_SIZE, BLACK

class Empty:
    PADDING = 5
    
    def __init__(self, row, col):
        """
        Initialize the Empty object.

        Parameters:
            row, col: spot to place in 2D array

        """
        self.row = row
        self.col = col
        self.color = DGREY
        self.visible = False #initially not going to display in game screen
        self.calc_pos()
        
    def calc_pos(self): 
        """
        calculate the x,y coords of current object

        Parameters:
            row, col: spot to place in 2D array

        """
        self.x = self.col * SQUARE_SIZE
        self.y = self.row * SQUARE_SIZE

        
    def draw(self, win):
        """
        draw the tiles that represents the game squares

        Parameters:
            win

        """  
        
        py.draw.rect(win, self.color, (self.x, self.y *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        py.draw.rect(win, BLACK, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)

    
    def __repr__(self) -> str:
        return str(self.color)

    