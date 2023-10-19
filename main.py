import sys
import pygame as py
from minesweeper.constants import WIDTH, HEIGHT, SQUARE_SIZE, BACKGROUND, BLACK, DGREY
from minesweeper.game import Game

FPS = 60

# settinwg window display
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Minesweeper")


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


def getName(clock):
    player_name = ""
    font = py.font.Font(None, 36)

    # Calculate the center position of the screen
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Calculate the position of the input box relative to the center
    input_box_width = 140
    input_box_height = 32
    input_box_x = center_x - input_box_width // 2
    input_box_y = center_y - input_box_height // 2

    input_box = py.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

    color_inactive = py.Color(BLACK)
    color_active = py.Color(DGREY)
    color = color_inactive
    active = False
    text = ""

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

            if event.type == py.KEYDOWN:
                if active:
                    if event.key == py.K_RETURN:
                        player_name = text
                        text = ""
                    elif event.key == py.K_BACKSPACE:
                        text = text[:-1]  # Remove the last character
                    else:
                        text += event.unicode  # Append the character to the text

        WIN.fill((255, 255, 255))  # Clear the screen

        color = color_active if active else color_inactive

        py.draw.rect(WIN, color, input_box, 2)

        text_surface = font.render(text, True, color)
        width = max(200, text_surface.get_width() + 10)
        input_box.w = width
        WIN.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        py.display.flip()
        clock.tick(FPS)

        if player_name:
            break

    return player_name


def main():
    run = True
    clock = py.time.Clock()

    game = Game(WIN)  # create Game object as game

    opening = True  # whether we are starting the game or not
    row, col = -1, -1  # -1 as initial starting value
    flag = False  # whether or not we are adding a flag
    clicked = False  # whether or not we clicked on the screen
    play_again = True  # if we want to play again after game ends
    restart_game = (
        False  # if we are playing again and need to reset all starting values
    )

    while play_again:
        while run:
            if restart_game:  # if true, restarting the game and all values used
                game.reset()
                opening, row, col, flag, clicked, play_again, restart_game = reset()

            WIN.fill(BACKGROUND)
            clock.tick(FPS)

            # creating event loop
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False
                    play_again = False
                    break

                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button = click on a squares
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(
                            pos
                        )  # get the row and column number
                        clicked = True
                        pass
                    elif event.button == 3:  # Right mouse button = add a flag
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        flag = True
                        pass

                if event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE:  # Spacebar = add a flag
                        pos = py.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        flag = True

                opening = game.select(row, col, flag, clicked, opening)  #

                flag = False
                clicked = False

            game.update(opening)  # update the display

            continue_game, game_won = game.resume_game()  #

            run = continue_game  #

        end_time = py.time.get_ticks() - game.start_time  # get how long the game lasted
        elapsed_seconds = end_time // 1000  # convert to seconds

        # Delay before starting the game loop
        py.time.delay(1500)  # 1.5 second delay allowing players to see their mistake

        player_name = ""
        WIN.fill(BACKGROUND)

        if game_won:
            player_name = getName(clock)

        game.display_game_end(
            WIN, game_won, elapsed_seconds, player_name
        )  # update display depending on whether or not we won or lost the game

        (
            play_again_button,
            quit_button,
        ) = (
            game.display_buttons()
        )  # create the buttons used to restart or quit the game

        quit_game = False

        # loop to determine if we are continuing the game or not, allows the button to stop flickering and wait until either button is clicked
        while not restart_game and not quit_game:
            for event in py.event.get():
                if event.type == py.QUIT:
                    play_again = restart_game = False
                    quit_game = True

                elif event.type == py.MOUSEBUTTONDOWN:
                    mouse_pos = py.mouse.get_pos()
                    if play_again_button.collidepoint(
                        mouse_pos
                    ):  # Check if "Play Again" button is clicked
                        play_again = run = restart_game = True

                    elif quit_button.collidepoint(
                        mouse_pos
                    ):  # Check if "Quit" button is clicked
                        play_again = restart_game = False
                        quit_game = True

    py.quit()


main()
