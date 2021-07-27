import guizero as g
import tkinter as tk
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def gui():
    global thruster_power_data
    global voltage_data
    global temperature_data

    interface = tk.Tk()
    interface.title("OD - 4D ROV Interface")
    interface.geometry("1280x800+0+0")
    filename = tk.PhotoImage(file="BattleboxBack4.png")
    background_label = tk.Label(image=filename)
    background_label.place(x=0,
                           y=0,
                           relwidth=1,
                           relheight=1)

    # Exit Code Button
    button = tk.Button(text="QUIT",
                       activeforeground="Red",
                       activebackground="Blue",
                       highlightbackground="Black",
                       command=interface.destroy,
                       height=8,
                       width=7).place(x=23, y=30)

    thruster_power_data = [0, 0, 0, 0, 0, 0, 0, 0]
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    ax.bar(range(len(thruster_power_data)), thruster_power_data, align='edge')
    ax.set_axis_off()
    canvas = FigureCanvasTkAgg(fig, master=interface)
    canvas.draw()
    canvas.get_tk_widget().place(x=780, y=640, width=460, height=120)

    voltage_data = [20, 21, 22]
    fig_two = Figure(figsize=(5, 4), dpi=100)
    ax_two = fig_two.add_subplot()
    ax_two.plot(range(len(voltage_data)), voltage_data)
    canvas_two = FigureCanvasTkAgg(fig_two, master=interface)
    canvas_two.draw()
    canvas_two.get_tk_widget().place(x=780, y=50, width=460, height=250)

    temperature_data = [20, 21, 22]
    fig_three = Figure(figsize=(5, 4), dpi=100)
    ax_three = fig_three.add_subplot()
    ax_three.plot(range(len(temperature_data)), temperature_data)
    canvas_three = FigureCanvasTkAgg(fig_three, master=interface)
    canvas_three.draw()
    canvas_three.get_tk_widget().place(x=780, y=325, width=460, height=250)

    interface.mainloop()

