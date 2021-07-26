import tkinter as tk


def gui():
    window = tk.Tk()
    window.title("OD - 4D ROV Interface")
    window.geometry("1280x800+0+0")
    filename = tk.PhotoImage(file="BattleboxBack4.png")
    background_label = tk.Label(image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Exit Code Button
    button = tk.Button(text="QUIT",
                       activeforeground="Red",
                       activebackground="Blue",
                       highlightbackground="Black",
                       command=exit,
                       height=8,
                       width=7).place(x=23, y=30)

    H1 = tk.Label(bg="red", height=8, width=4).place(x=780, y=632)
    H2 = tk.Label(bg="red", height=8, width=4).place(x=840, y=632)
    H3 = tk.Label(bg="red", height=8, width=4).place(x=900, y=632)
    H4 = tk.Label(bg="red", height=8, width=4).place(x=960, y=632)
    V1 = tk.Label(bg="red", height=8, width=4).place(x=1020, y=632)
    V2 = tk.Label(bg="red", height=8, width=4).place(x=1080, y=632)
    V3 = tk.Label(bg="red", height=8, width=4).place(x=1140, y=632)
    V4 = tk.Label(bg="red", height=8, width=4).place(x=1200, y=632)
    window.show()

gui()
