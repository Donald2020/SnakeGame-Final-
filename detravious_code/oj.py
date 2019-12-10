from tkinter import*
from random import randint
import tkinter as tk

# The purpose of defining all of these variable names is so that we could build the grid for the game.
grid = 90
gridPixel = 10
gridElement = 2 * gridPixel
width = gridPixel * grid
height = gridPixel * grid
# The purpose of this is to so that we could size the objects in the game
foodSizeScale = 1
predatorSizefactor = 0.9
foodSize = gridPixel * foodSizeScale
predatorSize = gridPixel * predatorSizefactor
# The purpose of this was so we could set the colors
boardgameColor = 'green'
startpage = 'yellow'
tutorialpage = 'blue'
foodColor = 'red'
predatorColor = 'yellow'
# this state's the shape's type in the snakeShape class
predator = 'snake'
obstacle = 'snakeFood'
gamepieceSizes = {predator: predatorSize, obstacle: foodSize}
# The puporsose of this is to set directional paths 
UP = 'Up'
DOWN = 'Down'
RIGHT = 'Right'
LEFT = 'Left'
# a dictionary to ease access to 'directions'
DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: 'Vertical', DOWN: 'Vertical', RIGHT: 'Horizontal', LEFT: 'Horizontal'}
# The purpose of this was to set the refresh time for motion in the game 
gamerefreshTime = 100


class Master(Canvas):
    """this creates the gameboard, the snake, the snakeFood, and  keeps track of the score"""
    def __init__(self, boss=None):
        super().__init__(boss)
        self.configure(width=width, height=height, bg=startpage)
        self.running = 0
        self.snake = None
        self.snakeFood = None
        self.direction = None
        self.current = None
        self.score = scoreTracker(boss)

    def start(self):
        """ this is what starts the  snake game"""
        if self.running == 0:
            self.configure(width=width, height=height, bg=boardgameColor)
            self.snake = snake(self)
            self.snakeFood = snakeFood(self)
            self.direction = RIGHT
            self.current = snakeMovement(self, RIGHT)
            self.current.begin()
            self.running = 1

    def tutorial(self):
        """This takes you to the tutorial page"""
        if self.running == 0:
            self.configure(width=width, height=height, bg=tutorialpage)
            root = tk.Tk()
            tk.Label(root, 
		     text="Turtorial\n\n This is the snake game the rules are simiple:\n Rule #1: eat the food particles to score\n Rule #2: avoid eating yourself and hittig the boarder",
		     fg = "red",
		     font = "Times").pack()

    def clean(self):
        """restarting the game"""
        if self.running == 1:
            self.current.stop()
            self.running = 0
            self.snakeFood.delete()
            for block in self.predator.blocks:
                block.delete()

    def redirect(self, event):
        """taking keyboard inputs and moving the snake accordingly"""
        if 1 == self.running and \
                event.keysym in AXES.keys() and\
                AXES[event.keysym] != AXES[self.direction]:
            self.current.flag = 0
            self.direction = event.keysym
            self.current = snakeMovement(self, event.keysym)  # a new instance at each turn to avoid confusion/tricking
            self.current.begin()  # program gets tricked if the user presses two arrow keys really quickly


class scoreTracker:
    """Objects that keep track of the score """
    def __init__(self, boss=None):
        self.counter = StringVar(boss, '0')
        self.maximum = StringVar(boss, '0')

    def increment(self):
        score = int(self.counter.get()) + 1
        self.counter.set(str(score))
 

    def reset(self):
        self.counter.set('0')


class snakeShape:
    """This is a template to make snakeFoods and snake body parts"""
    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        if kind == predator:
            self.ref = Canvas.create_rectangle(self.can, a - predatorSize, b - predatorSize, a + predatorSize, b + predatorSize, fill=predatorColor, width=2)
        elif kind == obstacle:
            self.ref = Canvas.create_oval(self.can, a - foodSize, b - foodSize, a + predatorSize, b + predatorSize, fill=foodColor, width=2)

    def modify(self, a, b):
        self.x, self.y = a, b
        self.can.coords(self.ref, a - gamepieceSizes[self.kind], b - gamepieceSizes[self.kind], a + gamepieceSizes[self.kind], b + gamepieceSizes[self.kind])

    def delete(self):
        self.can.delete(self.ref)


class snakeFood(snakeShape):
    """snake food"""
    def __init__(self, can):
        """the purpose of this is so that the snakeFoods only spawns randomly where there is no snake body part"""
        self.can = can
        p = int(grid/2 - 1)
        n, m = randint(0, p), randint(0, p)
        a, b = gridPixel * (2 * n + 1), gridPixel * (2 * m + 1)
        while [a, b] in [[block.x, block.y] for block in self.can.snake.blocks]:
            n, m = randint(0, p), randint(0, p)
            a, b = gridPixel * (2 * n + 1), gridPixel * (2 * m + 1)
        super().__init__(can, a, b, obstacle)


class snakeBody(snakeShape):
    """snake body part"""
    def __init__(self, can, a, y):
        super().__init__(can, a, y, predator)


class snake:
    """ the snake keeps track of its body parts"""
    def __init__(self, can):
        """ this what initial position chosen by me"""
        self.can = can
        a = gridPixel + 2 * int(grid/4) * gridPixel
        self.blocks = [snakeBody(can, a, a), snakeBody(can, a, a + gridElement)]

    def move(self, path):
        """an elementary gridElement consisting of putting the tail of the snake in the first position"""
        a = (self.blocks[-1].x + gridElement * path[0]) % width
        b = (self.blocks[-1].y + gridElement * path[1]) % height
        if a == self.can.snakeFood.x and b == self.can.snakeFood.y:  # the purpose of this is so that check if food was found
            self.can.score.increment()
            self.can.snakeFood.delete()
            self.blocks.append(snakeBody(self.can, a, b))
            self.can.snakeFood = snakeFood(self.can)
        elif [a, b] in [[block.x, block.y] for block in self.blocks]:  # the purpose of this is to check to make sure the snake ate a body part
            self.can.clean()
        else:
            self.blocks[0].modify(a, b)
            self.blocks = self.blocks[1:] + [self.blocks[0]]
            
    def outofbounds(self, x, y):
        if ((x < 20) or (x > 710) or (y < 40) or (y > 470)):
         return True 
         return False


class snakeMovement:
    """this helps determine the snakes direction after it absorbs the object"""
    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        """this start the motion"""
        if self.flag > 0:
            self.can.snake.move(DIRECTIONS[self.direction])
            self.can.after(gamerefreshTime, self.begin)

    def stop(self):
        """stop the movement"""
        self.flag = 0


root = Tk()
root.title("Anaconda")
game = Master(root)
game.grid(column=1, row=0, rowspan=3)
root.bind("<Key>", game.redirect)
buttons = Frame(root, width=35, height=3*height/5)
Button(buttons, text='Tutorial', command=game.tutorial).grid()
Button(buttons, text='Start', command=game.start).grid()
Button(buttons, text='Quit', command=root.destroy).grid()
buttons.grid(column=0, row=0)
scoreboard = Frame(root, width=35, height=2*height/5)
Label(scoreboard, text='Game Score').grid()
Label(scoreboard, textvariable=game.score.counter).grid()
scoreboard.grid(column=0, row=2)
root.mainloop()
