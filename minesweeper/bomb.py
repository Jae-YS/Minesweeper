import pygame as py
from .constants import SQUARE_SIZE, BOMB_IMAGE, BORDER_SIZE, BLACK

class Bomb:
    PADDING = 5
    
    def __init__(self, row, col):
        """
        Initialize the Bomb object.

        Parameters:
            row, col: spot to place in 2D array

        """
        self.row = row
        self.col = col
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
        display image of the bomb object

        Parameters:
            win

        """  

        # Center the image within the square
        img_x = self.x + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - BOMB_IMAGE.get_width()) // 2
        img_y = self.y + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - BOMB_IMAGE.get_height()) // 2
        
        # draw the BOMB_IMAGE at the calculated x,y coord
        win.blit(BOMB_IMAGE, (img_x, img_y))
        py.draw.rect(win, BLACK, (self.col*SQUARE_SIZE, self.row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)

    
    def __repr__(self) -> str:
        return str((self.row, self.col) )
    