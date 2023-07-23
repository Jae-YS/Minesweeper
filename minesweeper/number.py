import pygame as py
from .constants import SQUARE_SIZE, number_cases, BORDER_SIZE, BLACK

class Number:
    PADDING = 5
        
    def __init__(self, row, col, number):
        """
        Initialize the Number object.

        Parameters:
            row, col: spot to place in 2D array
            number: number of bomb surrounding the tile

        """
        self.row = row
        self.col = col
        self.number = number
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
        display image of the number object which represents the number of bombs surrounding the tile

        Parameters:
            win

        """  
        
        # Center the image within the square
        img_x = self.x + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - number_cases[self.number].get_width()) // 2
        img_y = self.y + BORDER_SIZE + (SQUARE_SIZE - BORDER_SIZE * 2 - number_cases[self.number].get_height()) // 2

        #displays the image of the current number of bombs surrounding the tile
        win.blit(number_cases[self.number], (img_x, img_y))
        py.draw.rect(win, BLACK, (self.col*SQUARE_SIZE, self.row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)

    
    def __repr__(self) -> str:
        return str(self.number)