import pygame as py


WIDTH, HEIGHT = 800, 850 #Window size
ROWS, COLS, BOMBS = 16, 16, 40 #Board size, number of bombs
SQUARE_SIZE = WIDTH//COLS #Square tile size
BORDER_SIZE = 2 #Size of border surrounding squares


#Colors used
RED = (255, 0 , 0)
LGREY = (192, 192, 192)
DGREY = (160, 160, 160)
LLGREY = (224, 224, 224)
BACKGROUND = (160, 160, 160)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


#images used
BOMB_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/bomb.png'), (20, 20))
FLAG_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/flag.png'), (20, 20))

ONE_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/one.png'), (20, 20))
TWO_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/two.png'), (20, 20))
THREE_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/three.png'), (20, 20))
FOUR_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/four.png'), (20, 20))
FIVE_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/five.png'), (20, 20))
SIX_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/six.png'), (20, 20))
SEVEN_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/seven.png'), (20, 20))
EIGHT_IMAGE = py.transform.scale(py.image.load('minesweeper/assets/eight.png'), (20, 20))

number_cases = {
    1: ONE_IMAGE,
    2: TWO_IMAGE,
    3: THREE_IMAGE,
    4: FOUR_IMAGE,
    5: FIVE_IMAGE,
    6: SIX_IMAGE,
    7: SEVEN_IMAGE, 
    8: EIGHT_IMAGE
}

AXIS = {
    "North" : (0, -1),
    "South" : (0, 1),
    "West" : (-1, 0),
    "East" : (1, 0),
}

