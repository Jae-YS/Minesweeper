import pygame as py
from minesweeper.board import Board
from minesweeper.flag import Flag
from minesweeper.bomb import Bomb
from minesweeper.constants import COLS, ROWS, GREEN, WHITE, RED, BOMBS, HEIGHT, WIDTH, BLACK


class Game:
    def __init__(self, WIN):
        """
        Initialize the Board object.

        Parameters:
            win:

        """
        self._init()
        py.init()
        py.font.init()   
        self.font = py.font.Font(None, 36)
    
        self.WIN = WIN

    def display_buttons(self):
        """
        function to display the play again and quit button at the end

        Parameters:
            self:

        Returns:
            play_again_button, quit_button: rectangle button used to determine if we are playing again or quitting
        """

        font = py.font.SysFont(None, 40)

        # Play Again button
        play_again_button = py.Rect(WIDTH // 6, HEIGHT * 3 // 4, 200, 50)
        py.draw.rect(self.WIN, GREEN, play_again_button)
        # format play again as string
        play_again_text = font.render("Play Again", True, WHITE)
        self.WIN.blit(play_again_text, (play_again_button.x + 35, play_again_button.y + 15))

        # Quit button
        quit_button = py.Rect(WIDTH * 2 // 3, HEIGHT * 3 // 4 , 120, 50)
        py.draw.rect(self.WIN, RED, quit_button)
        # format quit as string
        quit_text = font.render("Quit", True, WHITE)
        self.WIN.blit(quit_text, (quit_button.x + 25, quit_button.y + 15))

        py.display.update()
        
        return play_again_button, quit_button
        
    def resume_game(self):
        """
        Function that checks at the end of every move to see if we are continuing the game or not

        Parameters:
            self:

        Returns:
            continue_game, game_won: True if we are continuing the game or we won the game, False if we are not continuing the game or we lost the game
        """
        
        if self.number_of_bomb == 0: #only checks when we placed all the flag that "matches" the spot the bombs are
            
            self.game_won = True
            self.continue_game = False
            
            for row in range(ROWS):
                for col in range(COLS):
                    if isinstance(self.hidden_board[row][col], Flag): #only if the current spot is a flag object, we check further
                        if isinstance(self.board.board[row][col], Bomb): #making sure the flag object is placed in the right spot where the Bomb object should be
                            continue
                        else: #flag was placed at an incorrect spot, but we don't stop the game and we haven't won the game yet
                            self.game_won = False
                            self.continue_game = True
                            break
                    else: 
                        continue
            
            return self.continue_game, self.game_won
            
        else: #can never reach this spot and win the game, so will always lose the game if we are not continuing the game
            if not self.continue_game:
                return self.continue_game, False
            return True, False
    
    def update(self, opening):
        """
        Function that checks at the end of every move to see if we are continuing the game or not

        Parameters:
            self:
            opening: True if we are starting a game, False if we have been playing the game
            
        Returns:
            continue_game, game_won: True if we are continuing the game or we won the game, False if we are not continuing the game or we lost the game
        """
        
        self.board.draw(self.WIN, opening, self.hidden_board)
        
         # Calculate elapsed time
        elapsed_time = py.time.get_ticks() - self.start_time

        # Convert elapsed time to seconds and format as string
        elapsed_seconds = elapsed_time // 1000
        elapsed_time_str = f"Time: {elapsed_seconds} seconds"

        # Render the game clock on the screen
        timer_surface = self.font.render(elapsed_time_str, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect()
        timer_rect.bottomleft = (20, HEIGHT - 20)
        self.WIN.blit(timer_surface, timer_rect)
        
        # format number of bomb as string
        number_of_bombs_str = f"Bombs: {self.number_of_bomb}"
        
        #render the number of bomb on screen
        bomb_surface = self.font.render(number_of_bombs_str, True, (0, 0, 0))
        bomb_rect = bomb_surface.get_rect()
        bomb_rect.bottomright = (WIDTH - 20, HEIGHT - 20)
        self.WIN.blit(bomb_surface, bomb_rect)
        
        py.display.update()
        
    def _init(self):
        """
        Private method that initializes any variables used

        Parameters:
            self:
            
        Returns:
        """
        
        # Game clock variables
        self.start_time = py.time.get_ticks()
        
        self.board = Board()
        self.hidden_board = [[0] * COLS for _ in range(ROWS)] 
        
        self.number_of_bomb = BOMBS
        
        self.continue_game = True
        self.game_won = False
    
    def reset(self):
        """
        Function that calls the private init() method to restart the game
        
        Parameters:
            self:
            
        Returns:
        """
        self._init()
    
    def add_flag(self, row, col):
        """
        Function that adds a flag at current row, column spot

        Parameters:
            row, col: current spot we want to add a flag in the 2d array
            
        Returns:
        """

        #check to see if current spot can't add flag because what's under is already visible
        if self.board.board[row][col].visible is True:
            return
        #if current spot already has a flag, then we are removing the flag
        elif isinstance(self.hidden_board[row][col], Flag):
            self.number_of_bomb += 1
            self.hidden_board[row][col] = 0
            
            #condition which makes sure we don't stop the game even if we go to the negative numbers of bombs and back up
            if self.number_of_bomb == 0:
                self.game_won = False
                self.continue_game = True
                
        #add a flag at current spot
        else:
            self.number_of_bomb -=1
            self.hidden_board[row][col] = Flag(row, col, RED)  
         
    def select(self, row, col, flag, clicked, opening):
        """
        Function that calls other methods to perform the desired action

        Parameters:
            row, col: current spot we want to perform an action
            flag: True if we are adding a flag, False if we are not
            clicked: True if we are clicking to change the visibility of current spot, False if we are not
            opening: True if we starting a game, False if we have been playing the game
            
        Returns:
            Boolean: True if we are haven't started the game, False if we have
        """
        if row < 0: #row will be -1 if we haven't started the game yet, prevent errors
            return True
        #adding a flag
        if flag:
            self.add_flag(row, col)
        #tile is clicked to change its visibility
        elif clicked:
            self.continue_game = self.board.square_clicked(row, col, opening)
        return False

        
        