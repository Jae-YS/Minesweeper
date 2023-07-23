import pygame as py
from .constants import SQUARE_SIZE, FLAG_IMAGE, BORDER_SIZE, BLACK

class Flag:
    PADDING = 5
    def __init__(self, row, col, color):
        """
        Initialize the Flag object.

        Parameters:
            row, col: spot to place in 2D array

        """
        self.row = row
        self.col = col
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
        display image of the flag object

        Parameters:
            win

        """  

        # Center the image within the square
        img_x = self.x + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - FLAG_IMAGE.get_width()) // 2
        img_y = self.y + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - FLAG_IMAGE.get_height()) // 2
        
        # draw the FLAG_IMAGE at the calculated x,y coord
        win.blit(FLAG_IMAGE, (img_x, img_y))
        # Draw the border to fit within square
        py.draw.rect(win, BLACK, (self.col*SQUARE_SIZE, self.row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)
    
    def __repr__(self) -> str:
        return str(self.number)
        