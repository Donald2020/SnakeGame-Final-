from tkinter import*
from random import randint
import sys

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

root.mainloop()
