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


def gui(ICE, connected):
    global thruster_power_data
    global temperature_data
    global voltage_data
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

    thruster_power_data = [1, 20, 3, 4, 6, 10, 7, 3]
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor("black")
    ax = fig.add_subplot(xlim=[-0.5, len(thruster_power_data) - 0.5])
    ax.bar(range(len(thruster_power_data)), thruster_power_data)
    ax.set_axis_off()
    canvas = FigureCanvasTkAgg(fig, master=interface)
    canvas.draw()
    canvas.get_tk_widget().place(x=692, y=640, width=620, height=120)

    voltage_data = [0, 0, 0, 0, 0]
    fig_two = Figure(figsize=(5, 4), dpi=100)
    ax_two = fig_two.add_subplot()
    ax_two.plot(range(len(voltage_data)), voltage_data)
    canvas_two = FigureCanvasTkAgg(fig_two, master=interface)
    canvas_two.draw()
    canvas_two.get_tk_widget().place(x=780, y=50, width=460, height=250)

    temperature_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig_three = Figure(figsize=(5, 4), dpi=100)
    ax_three = fig_three.add_subplot()
    ax_three.set_ylim([0, 40])
    ax_three.plot(range(len(temperature_data)), temperature_data)
    canvas_three = FigureCanvasTkAgg(fig_three, master=interface)
    canvas_three.draw()
    canvas_three.get_tk_widget().place(x=780, y=325, width=460, height=250)

    if not ICE:
        ICE_status = tk.Text(interface, height=2, width=30)
        ICE_status.place(x=250, y=720)
        ICE_status.insert(tk.END, "ICE Robot is not Connected")
    if not connected:
        Connected_status = tk.Text(interface, height=2, width=30)
        Connected_status.place(x=250, y=680)
        Connected_status.insert(tk.END, "Battlebox is not Connected")

    def change_data():
        from random import randint
        global temperature_data
        temperature_data.pop(0)
        temperature_data.append(randint(1, 20))
        ax_three.clear()
        ax_three.set_ylim([0, 40])
        ax_three.plot(range(len(temperature_data)), temperature_data)
        canvas_three.draw()

    change_data_button = tk.Button(master=interface, text="Change Data", command=change_data)

    change_data_button.place(x=200, y=200)

    def change_data_two():
        from random import randint
        global voltage_data
        voltage_data.pop(0)
        voltage_data.append(randint(1, 20))
        ax_two.clear()
        ax_two.set_ylim([0, 40])
        ax_two.plot(range(len(voltage_data)), voltage_data)
        canvas_two.draw()

    change_data_button = tk.Button(master=interface, text="Change Data", command=change_data_two)

    change_data_button.place(x=300, y=200)

    def change_data_one():
        from random import randint
        global thruster_power_data
        for i in range(len(thruster_power_data)):
            thruster_power_data[i] = randint(1, 20)
        ax.clear()
        ax.patch.set_facecolor("black")
        ax.set_xlim([-0.5, len(thruster_power_data) - 0.5])
        ax.bar(range(len(thruster_power_data)), thruster_power_data)
        canvas.draw()

    change_data_button = tk.Button(master=interface, text="Change Data", command=change_data_one)

    change_data_button.place(x=400, y=200)




        # for i in range(len(data)):
        #     data[i] = randint(1, 20)
        # print(data)
        # # Re-Draw the graph!
        # ax.clear()
        # ax.bar(range(len(data)), data)
        # canvas.draw()



    interface.mainloop()

