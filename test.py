import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from random import randint

data =[0,0,0,0,0]
root = tkinter.Tk()
root.wm_title("Embedding in Tk")
#We could do it like this, but let's do it differently to allow for updating.
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot()
ax.bar(range(len(data)), data)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()


def change_data():
    global data
    for i in range(len(data)):
        data[i] = randint(1,20)
    print(data)
    #Re-Draw the graph!
    ax.clear()
    ax.bar(range(len(data)), data)
    canvas.draw()


label = tkinter.Label(master=root, text="Tkinter Matplotlib Example - Updatable bargraph!")
change_data_button = tkinter.Button(master=root, text="Change Data", command=change_data)
quit_button = tkinter.Button(master=root, text="Quit", command=root.quit)

label.grid(row=0, column=0, columnspan=2)
canvas.get_tk_widget().grid(row=1,column=0, columnspan=2)
change_data_button.grid(row=2, column=0)
quit_button.grid(row=2, column=1)
tkinter.mainloop()