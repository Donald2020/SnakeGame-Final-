from tkinter import*
from random import randint
import tkinter as tk


# The purpose of this was so we could set the colors
boardgameColor = 'green'
startpage = 'yellow'
tutorialpage = 'blue'




    def tutorial(self):
        """This takes you to the tutorial page"""
        if self.running == 0:
            self.configure(width=width, height=height, bg=tutorialpage)
            root = tk.Tk()
            tk.Label(root, 
		     text="Turtorial\n\n This is the snake game the rules are simiple:\n Rule #1: eat the food particles to score\n Rule #2: avoid eating yourself and hittig the boarder",
		     fg = "red",
		     font = "Times").pack()

root = Tk()
root.title("Anaconda")
game = Master(root)
game.grid(column=1, row=0, rowspan=3)
root.bind("<Key>", game.redirect)
buttons = Frame(root, width=35, height=3*height/5)
Button(buttons, text='Tutorial', command=game.tutorial).grid()
