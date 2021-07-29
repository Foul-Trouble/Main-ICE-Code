
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure

import threading

import time

voltage_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
temperature_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def gui(ICE, connected):
    global thruster_power_data
    global temperature_data
    global voltage_data

    global temperature_ax
    global voltage_ax
    global temperature_canvas
    global voltage_canvas

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

    thruster_power_data = [0, 0, 0, 0, 0, 0, 0, 0]
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor("black")
    thruster_ax = fig.add_subplot(xlim=[-0.5, len(thruster_power_data) - 0.5])
    thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
    thruster_ax.set_axis_off()
    thruster_gauge_canvas = FigureCanvasTkAgg(fig, master=interface)
    thruster_gauge_canvas.draw()
    thruster_gauge_canvas.get_tk_widget().place(x=692, y=640, width=620, height=120)

    voltage_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig_two = Figure(figsize=(5, 4), dpi=100)
    voltage_ax = fig_two.add_subplot()
    voltage_ax.plot(range(len(voltage_data)), voltage_data)
    voltage_canvas = FigureCanvasTkAgg(fig_two, master=interface)
    voltage_canvas.draw()
    voltage_canvas.get_tk_widget().place(x=780, y=50, width=460, height=250)

    temperature_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig_three = Figure(figsize=(5, 4), dpi=100)
    temperature_ax = fig_three.add_subplot()
    temperature_ax.set_ylim([0, 40])
    temperature_ax.plot(range(len(temperature_data)), temperature_data)
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

    def change_temperature_data():
        from random import randint
        global temperature_data
        temperature_data.pop(0)
        temperature_data.append(randint(1, 20))
        temperature_ax.clear()
        temperature_ax.set_ylim([0, 40])
        temperature_ax.plot(range(len(temperature_data)), temperature_data)
        temperature_canvas.draw()

    change_data_button = tk.Button(master=interface, text="New Temperature Data", command=change_temperature_data)

    change_data_button.place(x=200, y=200)

    def change_voltage_data():
        from random import randint
        global voltage_data
        voltage_data.pop(0)
        voltage_data.append(randint(1, 20))
        voltage_ax.clear()
        voltage_ax.set_ylim([0, 40])
        voltage_ax.plot(range(len(voltage_data)), voltage_data)
        voltage_canvas.draw()

    change_data_button = tk.Button(master=interface, text="New Voltage Data", command=change_voltage_data)

    change_data_button.place(x=200, y=250)

    def change_thruster_data():
        from random import randint
        global thruster_power_data
        for i in range(len(thruster_power_data)):
            thruster_power_data[i] = randint(1, 20)
        thruster_ax.clear()
        thruster_ax.patch.set_facecolor("black")
        thruster_ax.set_xlim([-0.5, len(thruster_power_data) - 0.5])
        thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
        thruster_gauge_canvas.draw()

    change_data_button = tk.Button(master=interface, text="New Thruster Data", command=change_thruster_data)

    change_data_button.place(x=200, y=300)

    def auto_run():
        threading.Thread(name='Live Updates', target=live_updates()).start()

    auto_run_button = tk.Button(master=interface, text="Auto Run", command=auto_run)
    auto_run_button.place(x=200, y=350)

    interface.mainloop()



def change_temperature_datas():
    from random import randint
    global temperature_data
    temperature_data.pop(0)
    temperature_data.append(randint(1, 20))
    temperature_ax.clear()
    temperature_ax.set_ylim([0, 40])
    temperature_ax.plot(range(len(temperature_data)), temperature_data)
    temperature_canvas.draw()


def change_voltage_datas():
    from random import randint
    global voltage_data
    voltage_data.pop(0)
    voltage_data.append(randint(1, 20))
    voltage_ax.clear()
    voltage_ax.set_ylim([0, 40])
    voltage_ax.plot(range(len(voltage_data)), voltage_data)
    voltage_canvas.draw()


def change_thruster_datas():
    from random import randint
    global thruster_power_data
    for i in range(len(thruster_power_data)):
        thruster_power_data[i] = randint(1, 20)
    thruster_ax.clear()
    thruster_ax.patch.set_facecolor("black")
    thruster_ax.set_xlim([-0.5, len(thruster_power_data) - 0.5])
    thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
    thruster_gauge_canvas.draw()


def live_updates():
    while True:
        try:
            while True:
                change_temperature_datas()
                change_voltage_datas()
                time.sleep(1)
        except:
            print("Nope")


gui(False, False)
