
#Donald's code* 

from tkinter import*
from random import randint
import sys
####Start of Donald's code#####
#  Defined the variables so that we could build the grid for the game.
grid = 90
gridPixel = 10
gridElement = 2 * gridPixel
width = gridPixel * grid
height = gridPixel * grid
topHeight = -1 + height
# Added this to determine the size of the objects in the game
foodSizeScale = 1
predatorSizefactor = 0.9
foodSize = gridPixel * foodSizeScale
predatorSize = gridPixel * predatorSizefactor
# Added this to set the colors
boardgameColor = 'green'
foodColor = 'orange'
predatorColor = 'yellow'
# Added this to state's the shape's type in the snakeShape class
predator = 'snake'
obstacle = 'snakeFood'
gamepieceSizes = {predator: predatorSize, obstacle: foodSize}
# Added this to set directional paths
UP = 'Up'
DOWN = 'Down'
RIGHT = 'Right'
LEFT = 'Left'
# a dictionary to ease access to 'directions'
DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: 'Vertical', DOWN: 'Vertical', RIGHT: 'Horizontal', LEFT: 'Horizontal'}
# The purpose of this was to set the refresh time for motion in the game
gamerefreshTime = 100

#bg is short for "boardgame"
class Master(Canvas):
    """this creates the gameboard, the snake, the snakeFood, and  keeps track of the score"""
    def __init__(self, boss=None):
        super().__init__(boss)
        self.configure(width=width, height=height, bg=boardgameColor)
        self.running = 0
        self.snake = None
        self.snakeFood = None
        self.direction = None
        self.current = None
        self.score = scoreTracker(boss)

    def start(self):
        """ this is what starts the  snake game"""
        if self.running == 0:
            self.snake = snake(self)
            self.snakeFood = snakeFood(self)
            self.direction = RIGHT
            self.current = snakeMovement(self, RIGHT)
            self.current.begin()
            self.running = 1

    def clean(self):
        """this is what restarts the game"""
        if self.running == 1:
            self.current.stop()
            self.running = 0
            self.snakeFood.delete()
            for block in self.predator.blocks:
                block.delete()

    def redirect(self, event):
        """this is what takes in the keyboard inputs and moves the snake accordingly"""
        if (
            self.running == 1
            and event.keysym in AXES.keys()
            and AXES[event.keysym] != AXES[self.direction]
        ):
            self.current.flag = 0
            self.direction = event.keysym
            self.current = snakeMovement(self, event.keysym) 
            self.current.begin()  


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
#End of Donald's code

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


####Start of Donald's code####

class snakeFood(snakeShape):
    """snake food"""
    def __init__(self, can):
        """added this so that the snakeFoods only spawns randomly where there is no snake body part"""
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

####End of Donald's code####


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


#function should stop snake at border and end the game
#does not work properly.
    def outOfBounds(self):
#self.blocks[0] is the head of the snake
        a = self.blocks[0].x
#self.blocks[-1] is the end of the snake
        b = self.blocks[-1].x
#width, height, and topHeight from above
        if a == width and b == height and a == 0 and b == topHeight:
            exit(1)



####Start of Donald's code####
class snakeMovement:
    """this helps determine the snakes direction after it absorbs the object"""
    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        """this starts the motion"""
        if self.flag > 0:
            self.can.snake.move(DIRECTIONS[self.direction])
            self.can.after(gamerefreshTime, self.begin)

    def stop(self):
        """this stops the movement"""
        self.flag = 0

        if self.outOfBounds():
            return
####End of Donald's code####



root = Tk()
root.title("Anaconda")

game = Master(root)
game.grid(column=2, row=0, rowspan=6)
root.bind("<Key>", game.redirect)

buttons = Frame(root, width=40, height=6*height/10)
#game.start refers to start function above
Button(buttons, text='Start', padx=15, pady=15, command=game.start).grid()
#root.destroy is built in to tkinter
Button(buttons, text='Quit', padx=15, pady=15, command=root.destroy).grid()
buttons.grid(column=0, row=0)


####Start of Donald's code####
scoreboard = Frame(root, width=35, height=2*height/5)
Label(scoreboard, text='Game Score').grid()
Label(scoreboard, textvariable=game.score.counter).grid()
scoreboard.grid(column=0, row=2)
####End of Donald's code####



##### Start of DB #####
root.mainloop()
##### End of DB #####
