import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure

from random import randint

import threading

import time


def gui(ICE, connected):
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
    quit_button = tk.Button(text="QUIT",
                            activeforeground="Red",
                            activebackground="Blue",
                            highlightbackground="Black",
                            command=interface.destroy,
                            height=8,
                            width=7).place(x=23, y=30)

    #    Thruster Graph
    thruster_power_data = [0, 0, 0, 0, 0, 0, 0, 0]
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor("black")
    thruster_ax = fig.add_subplot(xlim=[-0.5, len(thruster_power_data) - 0.5])
    thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
    thruster_ax.set_axis_off()
    thruster_gauge_canvas = FigureCanvasTkAgg(fig, master=interface)
    thruster_gauge_canvas.draw()
    thruster_gauge_canvas.get_tk_widget().place(x=692, y=640, width=620, height=120)

    #    Power Graph
    voltage_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    current_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig_two = Figure(figsize=(5, 4), dpi=100)
    voltage_ax = fig_two.add_subplot()
    voltage_ax.set_title('Power Usage')
    voltage_ax.set_ylabel('Voltage', color='y')
    voltage_ax.get_xaxis().set_visible(False)
    voltage_ax.set_ylim([0, 40])
    voltage_ax.plot(range(len(voltage_data)), voltage_data)
    voltage_ax2 = voltage_ax.twinx()
    voltage_ax2.set_ylabel('Current', color='orange')
    voltage_canvas = FigureCanvasTkAgg(fig_two, master=interface)
    voltage_canvas.draw()
    voltage_canvas.get_tk_widget().place(x=780, y=50, width=460, height=250)

    #    Climate Graph
    temperature_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    humidity_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig_three = Figure(figsize=(5, 4), dpi=100)
    temperature_ax = fig_three.add_subplot()
    temperature_ax.set_title('Onboard Climate')
    temperature_ax.set_ylabel('Temperature : Degrees (Celsius)', color='r')
    temperature_ax.get_xaxis().set_visible(False)
    temperature_ax.set_ylim([0, 40])
    temperature_ax.plot(range(len(temperature_data)), temperature_data)

    humidity_ax = temperature_ax.twinx()
    humidity_ax.set_ylabel('Humidity', color='b')
    humidity_ax.set_ylim([0, 100])
    humidity_ax.plot(range(len(humidity_data)), humidity_data)

    temperature_canvas = FigureCanvasTkAgg(fig_three, master=interface)
    temperature_canvas.draw()
    temperature_canvas.get_tk_widget().place(x=780, y=325, width=460, height=250)

    if not ICE:
        ICE_status = tk.Text(interface, height=2, width=30)
        ICE_status.place(x=250, y=720)
        ICE_status.insert(tk.END, "ICE Robot is not Connected")
    if not connected:
        Connected_status = tk.Text(interface, height=2, width=30)
        Connected_status.place(x=250, y=680)
        Connected_status.insert(tk.END, "Battlebox is not Connected")

    def change_climate_data():
        temperature_data.pop(0)
        temperature_data.append(randint(1, 40))
        temperature_ax.clear()

        humidity_data.pop(0)
        humidity_data.append(randint(1, 100))
        humidity_ax.clear()

        temperature_ax.set_title('Onboard Climate')
        temperature_ax.set_ylabel('Temperature : Degrees (Celsius)')
        temperature_ax.get_xaxis().set_visible(False)
        temperature_ax.set_ylim([0, 40])
        temperature_ax.plot(range(len(temperature_data)), temperature_data, color='r')
        humidity_ax = temperature_ax.twinx()
        humidity_ax.set_ylabel('Humidity', color='b')
        humidity_ax.set_ylim([0, 100])
        humidity_ax.plot(range(len(humidity_data)), humidity_data)
        temperature_canvas.draw()

    def change_power_data():
        voltage_data.pop(0)
        voltage_data.append(randint(1, 20))
        voltage_ax.clear()

        voltage_ax.set_title('Power Usage')
        voltage_ax.set_ylabel('Voltage')
        voltage_ax.get_xaxis().set_visible(False)
        voltage_ax.set_ylim([0, 40])
        voltage_ax.plot(range(len(voltage_data)), voltage_data, color='y')
        voltage_canvas.draw()

    def change_thruster_data():
        for i in range(len(thruster_power_data)):
            thruster_power_data[i] = randint(1, 20)
        thruster_ax.clear()

        thruster_ax.patch.set_facecolor("black")
        thruster_ax.set_xlim([-0.5, len(thruster_power_data) - 0.5])
        thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
        thruster_gauge_canvas.draw()

    change_climate_button = tk.Button(master=interface,
                                      text="New Climate Data",
                                      command=change_climate_data).place(x=500, y=680)
    change_power_button = tk.Button(master=interface,
                                    text="New Power Data",
                                    command=change_power_data).place(x=500, y=710)
    change_thruster_button = tk.Button(master=interface,
                                       text="New Thruster Data",
                                       command=change_thruster_data).place(x=500, y=740)

    s = tk.ttk.Style()
    s.theme_use('clam')
    s.configure("green.Horizontal.TProgressbar", foreground='green', background='black', )
    progress = tk.ttk.Progressbar
    progress(interface, style="green.Horizontal.TProgressbar", orient="horizontal", length=600, mode="determinate",
             maximum=100, value=47).place(x=23, y=600, height=50, width=700)

    programmable_button_1 = tk.Button(text="1",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=23, y=447)
    programmable_button_2 = tk.Button(text="2",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=113, y=447)
    programmable_button_3 = tk.Button(text="3",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=203, y=447)
    programmable_button_4 = tk.Button(text="4",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=293, y=447)
    programmable_button_5 = tk.Button(text="5",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=383, y=447)
    programmable_button_6 = tk.Button(text="6",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=473, y=447)
    programmable_button_7 = tk.Button(text="7",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=563, y=447)
    programmable_button_8 = tk.Button(text="8",
                                      activeforeground="Red",
                                      activebackground="Blue",
                                      highlightbackground="Black",
                                      command=None,
                                      height=8,
                                      width=7).place(x=653, y=447)

    blank = tk.Text(interface)
    blank.place(x=23, y=170, height=270, width=700)

    interface.mainloop()


gui(False, False)
