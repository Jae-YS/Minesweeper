import pygame as py
from minesweeper.constants import WIDTH, HEIGHT, SQUARE_SIZE, BACKGROUND, BLACK
from minesweeper.game import Game

FPS = 60

#setting window display
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Minesweeper')


def get_row_col_from_mouse(pos):
    """
    Get the x and y position from window and convert them into row and column numbers

    Parameters:
        pos: (x,y) coord

    Returns:
        row and column numbers
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_game_end(win, game_won, time_seconds):
    """
    Display that shows up when the game is over 

    Parameters:
        win: the window to update the display on
        game_won: if we won or lost
        time_seconds: how long it took to beat the game

    Returns:
        
    """
    
    win.fill(BACKGROUND)
    font = py.font.SysFont(None, 80)
    
    
    if game_won: #text shown if you won the game
        game_won_str = f"Game Won: {time_seconds} seconds"
        text = font.render(game_won_str, True, BLACK)
    else: #text shown if you lost the game
        text = font.render("Game Lost", True, BLACK)
        
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    py.display.update()
    
def reset():
    """
    Resets all variables used during the game to it's base form
        
    """
    opening = True
    row, col = -1, -1
    flag = False
    clicked = False
    play_again = True
    restart_game = False
    
    return opening, row, col, flag, clicked, play_again, restart_game
            



def main():
    
    run = True
    clock = py.time.Clock()
    
    game = Game(WIN) #create Game object as game
    
    opening = True #whether we are starting the game or not
    row, col = -1, -1 #-1 as initial starting value
    flag = False #whether or not we are adding a flag
    clicked = False #whether or not we clicked on the screen
    play_again = True #if we want to play again after game ends
    restart_game = False #if we are playing again and need to reset all starting values
    
    while play_again:
        
        while run:
            
            if restart_game: #if true, restarting the game and all values used
                game.reset()
                opening, row, col, flag, clicked, play_again, restart_game = reset()

            WIN.fill(BACKGROUND)
            clock.tick(60)
                        

            #creating event loop
            for event in py.event.get():
                
                if event.type == py.QUIT:
                    run = False
                    
                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button = click on a squares
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos) #get the row and column number 
                        clicked = True
                        pass
                    elif event.button == 3:  # Right mouse button = add a flag
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        flag = True
                        pass
                    
                if event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE: # Spacebar = add a flag
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        flag = True
                        
                    
                opening = game.select(row, col, flag, clicked, opening) #
                
                flag = False
                clicked = False 
                
            game.update(opening) #update the display
            
                        
            continue_game, game_won = game.resume_game() #
            
            run = continue_game #
                
                

        end_time = py.time.get_ticks() - game.start_time #get how long the game lasted
        elapsed_seconds = end_time // 1000 #convert to seconds
        
        # Delay before starting the game loop
        py.time.delay(5000)  # 5 second delay allowing players to see their mistake
        
        
        display_game_end(WIN, game_won, elapsed_seconds) #update display depending on whether or not we won or lost the game
        
        play_again_button, quit_button = game.display_buttons() #create the buttons used to restart or quit the game
        
        quit_game = False
        
        #loop to determine if we are continuing the game or not, allows the button to stop flickering and wait until either button is clicked
        while not restart_game and not quit_game:
            for event in py.event.get():
                if event.type == py.QUIT:
                    play_again = restart_game = False
                    quit_game = True
            
                elif event.type == py.MOUSEBUTTONDOWN:
                    mouse_pos = py.mouse.get_pos()
                    if play_again_button.collidepoint(mouse_pos):  # Check if "Play Again" button is clicked
                        play_again = run = restart_game = True
                        
                    elif quit_button.collidepoint(mouse_pos):     # Check if "Quit" button is clicked
                        play_again = restart_game = False
                        quit_game = True
                        
                        
            
    py.quit()    
    



    
main()