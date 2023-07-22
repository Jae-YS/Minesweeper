import pygame as py
import random

from minesweeper.bomb import Bomb
from minesweeper.number import Number
from minesweeper.empty import Empty
from minesweeper.flag import Flag
from .constants import LLGREY, ROWS, COLS, SQUARE_SIZE, BOMBS, BLACK, BORDER_SIZE, AXIS

class Board:
    def __init__(self):
        """
        Initialize the Board object.

        Parameters:

        """
        
        self.board = [] #2d array used to keep track of elements used
        self.bomb = BOMBS #number of bombs

    def create_board(self, first_row, first_col):
        """
        creates the board used during the game

        Parameters:
            self:
            first_row, first_col: when the game start, the first square that is clicked 

        Returns:
        """

        self.board = [[0] * COLS for _ in range(ROWS)] #initially create a 2d board that is filled with 0
        
                    
        empty_square = [] #keeps track of the initial tiles that are Empty objects
        
        x_coord, y_coord = first_col, first_row
        
        number_of_empty_squares = random.randint(1, 15)

        #When starting a game, the initial square can't be a bomb or a number (allows the person playing the game a chance to win)
        self.board[y_coord][x_coord] = Empty(y_coord, x_coord) #initial tile clicked
        empty_square.append((x_coord, y_coord))
        number_of_empty_squares -= 1 
            
        random_axis = random.choice(list(AXIS.values())) #randomly choses a direction the next Empty square will be (north, south, west, east)
        
        offset_col, offset_row = random_axis    
        empty_square, number_of_empty_squares = self.random_add(offset_row, offset_col, empty_square, number_of_empty_squares)
        
        
        while number_of_empty_squares > 0:

            # Generate a random number between -1 and 1 for both row and column offsets
            offset_row = random.randint(-1, 1)
            offset_col = random.randint(-1, 1)
            
            #add to the group of Empty objects that's initially displayed to allow the player to beat the game without guessing
            empty_square, number_of_empty_squares = self.random_add(offset_row, offset_col, empty_square, number_of_empty_squares)
    
        #create a list of squares which encloses the group of empty objects
        number_square = self.get_surrounding_number_square(empty_square)
        
        bomb_placed = 0
        
        #randomly placing bombs in board
        while bomb_placed != self.bomb:
        # Generate a random number between 0 and 15 
            random_number_row = random.randint(0, ROWS - 1)
            random_number_col = random.randint(0, COLS - 1)
            random_coords = (random_number_col, random_number_row)
            
            if random_coords not in number_square and random_coords not in empty_square:
                if not self.is_valid_spot(random_number_row, random_number_col, Bomb): #helper method that checks to see if a Bomb object can be placed in current row column spot
                    self.board[random_number_row][random_number_col] =  Bomb(random_number_row, random_number_col)
                    bomb_placed += 1
                        
        #fill in any squares with Number objects depending on how bombs are surrounding current tile (up to 8)
        for row in range(ROWS):
            for col in range(COLS):
                number_of_bombs = self.get_number(row, col) #gets the number of bombs surrounding current row column tile
                if not self.is_valid_spot(row, col, Bomb) and number_of_bombs > 0: #adds a Number object if that number of bombs is greater than 0 and current spot isn't a Bomb object
                    self.board[row][col] = Number(row, col, number_of_bombs)
                    
        #fill the rest of the squares with Empty objects
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    self.board[row][col] = Empty(row, col)
                    
        #helper method that double checks to see if the current number of Empty objects and Number objects are correct in the starting group
        empty_square, number_square = self.update_starting_board(empty_square, number_square)
                
        #sets the current list of Empty objects and Number objects to be visible allowing the player to play the game
        self.surrounding_center_visible(empty_square, number_square)
        
    def random_add(self, offset_row, offset_col, empty_square, number_of_empty_squares):
        """
        Calculate the sum of two numbers.

        Parameters:
            offset_row, offset_col: values between -1 and 1 used to calculate the next row and column
            empty_square: location of all current Empty objects surrounding the starting group
            number_of_empty_squares: number of Empty object left to add to the starting group
            
        Returns:
            empty_square: updated list of the location of all current Empty objects surrounding the starting group
            number_of_empty_squares: updated count of how many Empty objects need to be added
        """
        
        
        coords = empty_square[-1] #get the coords of the most recent addition of Empty objects
        x_coord, y_coord = coords
        
        #calculate new row and column values
        new_x = x_coord + offset_col
        new_y = y_coord + offset_row
            
        # Ensure the new coordinates are within the bounds of the array
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and (new_x, new_y) not in empty_square:
            self.board[new_y][new_x] = Empty(new_y, new_x)
            self.board[new_y][new_x].visible = True
            number_of_empty_squares -= 1
            empty_square.append((new_x, new_y))
        
        return empty_square, number_of_empty_squares
    
    def get_surrounding_number_square(self, empty_square):
        """
        Gets a list of up to eight tiles surrounding each empty_square. Making sure that none of the Empty objects in the starting board
        gets replaced by Number of Bomb objects 

        Parameters:
            offset_row, offset_col: values between -1 and 1 used to calculate the next row and column
            empty_square: location of all current Empty objects surrounding the starting group
            number_of_empty_squares: number of Empty object left to add to the starting group
            
        Returns:
            number_square: updated list of the location of all current Number objects surrounding the starting Empty group object
        
        """
        
        number_square = []
        for coords in empty_square:
            col, row  = coords
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row = row + i
                    new_col = col + j
                    new_coords = (new_col, new_row)
                    # Ensure the new coordinates are within the bounds of the array
                    if 0 <= new_col < COLS and 0 <= new_row < ROWS and new_coords not in empty_square and new_coords not in number_square:
                        number_square.append(new_coords)
    
        return number_square
    
    def is_valid_spot(self, row, col, object_type):
        """
        Helper method that returns where the row,col spot in the 2d array is a viable spot to place a Bomb object

        Parameters:
            row, col: spot to check in 2d array
            object_type: what object we are comparing to
            
        Returns:
            Boolean: True if the object in that spot matches the input object_type, False otherwise
        
        """

        # Get the object at the specified indices
        object_to_check = self.board[row][col]

        # return if the object is an instance of the class Bomb
        return isinstance(object_to_check, object_type)
    
    def get_number(self, row, col):
        """
        Helper method that returns the number of bomb surrounding the current row, column tile

        Parameters:
            row, col: spot to check in 2d array
            
        Returns:
            number_of_bombs: value between 0-8, which tells how many bombs are surrounding it
        
        """
        
        number_of_bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row = row + i
                new_col = col + j
                
                # Check if the new position is within the array bounds
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    if isinstance(self.board[new_row][new_col], Bomb):
                        number_of_bombs += 1
        
        return number_of_bombs
    
    def update_starting_board(self, empty_square, number_square):
        """
        Helper method checks to see if current list of Empty objects and Number objects are correct because initial creation of the board doesn't cover it,
        as the board was updated further with other objects

        Parameters:
            empty_square: location of all current Empty objects surrounding the starting group
            number_square: location of all current Number objects surrounding the starting group
            
        Returns:
            empty_square: updated list of the location of all current Empty objects surrounding the starting group
            number_square: updated list of the location of all current Number objects surrounding the starting group
        """
        
        for coords in empty_square:
            col, row  = coords
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row = row + i
                    new_col = col + j
                    # Ensure the new coordinates are within the bounds of the array
                    if 0 <= new_col < COLS and 0 <= new_row < ROWS:
                        new_coords = (new_col, new_row)
                        new_board = self.board[new_row][new_col]
                        if isinstance(new_board, Empty) and new_coords not in empty_square: #updates the list of Empty objects with new row, col coord
                            empty_square.append(new_coords)
                            if new_coords in number_square: #removes from list of Number objects because it was incorrectly
                                number_square.remove(new_coords)
                        elif isinstance(new_board, Number) and new_coords not in number_square: #updates the list of Number objects with new row, col coord
                            number_square.append(new_coords)
                        else:
                            continue
                    
        
        
        return empty_square, number_square
        
    def change_visibility(self, row, col):
        """
        Helper method that changes current object in given row and column visibility to be True

        Parameters:
            row, col: spot in the 2d array we want
            
        Returns:
        """
        self.board[row][col].visible = True
    
    def surrounding_center_visible(self, empty_square, number_square):
        """
        Finds the coords of every object in empty_square and number_square list and change their visibility to be True

        Parameters:
            empty_square: location of all current Empty objects surrounding the starting group
            number_square: location of all current Number objects surrounding the starting group
            
        Returns:
        
        """
        
        for coords in empty_square:
            col, row  = coords
            self.change_visibility(row, col) #helper method that changes their visibility to True
        
        for coords in number_square:
            col, row = coords
            self.change_visibility(row, col)

    def final_all_empty(self, row, col):
        """
        Helper method which finds the coords of every object in empty_square and number_square list and change their visibility to be True
        given a row and column

        Parameters:
            row, col: spot in the 2d array we want
            
        Returns:
        
        """        
        empty_square = []
        empty_square.append((col, row))
        number_square = []
        
        for coords in empty_square: #check all 8 possible spot of every coord in empty_square
            col, row  = coords
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row = row + i
                    new_col = col + j
                    new_coords = (new_col, new_row)
                    # Ensure the new coordinates are within the bounds of the array                  
                    if 0 <= new_col < COLS and 0 <= new_row < ROWS:  
                        if isinstance(self.board[new_row][new_col], Empty) and new_coords not in empty_square:
                            empty_square.append(new_coords)
                        elif isinstance(self.board[new_row][new_col], Number) and new_coords not in number_square:
                            number_square.append(new_coords)
        
        #sets the current list of Empty objects and Number objects to be visible
        self.surrounding_center_visible(empty_square, number_square)
        
    def square_clicked(self, row, col, opening):
        """
        Helper method which finds the coords of every object in empty_square and number_square list and change their visibility to be True
        given a row and column

        Parameters:
            row, col: spot in the 2d array we want
            
        Returns:
            Boolean: True if we are continuing the game, False if we are not 
        """        
        if opening:
            self.create_board(row,col)
            return True
        else:
            changeVis = self.board[row][col]
            if changeVis.visible is False:
                changeVis.visible = True
                self.board[row][col] = changeVis
            if isinstance(changeVis, Bomb):
                return False
            elif isinstance(changeVis, Empty):
                self.final_all_empty(row, col)
        return True
                               
    def draw_square(self, win, row, col):
        """
        converts the row and col to an x,y coord to draw a square tile on the window

        Parameters:
            row, col: spot in the 2d array which will be converted to an x,y coord we want to draw
            win: the window we are drawing on
            
        Returns:
        """   
        
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        
        # Draw the square
        py.draw.rect(win, LLGREY, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        # Draw the border
        py.draw.rect(win, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)
            
    def draw_empty_board(self, win):
        """
        Method that will draw the entire game board given that it is the first time starting the game

        Parameters:
            win: the window we are drawing on
            
        Returns:
        """   
        # Draw the game board
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                # Draw the square
                py.draw.rect(win, LLGREY, (x, y, SQUARE_SIZE, SQUARE_SIZE))

                # Draw the border
                py.draw.rect(win, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), BORDER_SIZE)


    def draw(self, win, opening, hidden_board):
        """
        Main draw method that's called initially from game object, if it's the opening board, then will call draw_empty_board()
        else it'll go through every spot in the window and check to see if which object we are drawing (Flag, Number, Bomb, Empty)

        Parameters:
            win: window we are drawing on
            opening: boolean which indicates if we want the starting board or not
            hidden_board: 2d array list that the game object keeps track of where we placed a flag
            
        Returns:
        """   
        
        if opening: #if true, we are drawing the starting board where nothing is visible
            self.draw_empty_board(win)
        else:    
            for row in range(ROWS):
                for col in range(COLS):
                    toDraw = self.board[row][col]
                    if isinstance(hidden_board[row][col], Flag): #there is a flag object at current row, col spot
                        hidden_board[row][col].draw(win) #draw flag
                    elif toDraw.visible is True:
                        toDraw.draw(win) #if current object has been clicked, draw whatever object we are at
                    else:
                        self.draw_square(win, row, col) #draw an Empty object tile