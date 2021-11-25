
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sqlite3 as sql


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("960x540")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=540,
    width=960,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    480.0,
    270.0,
    image=image_image_1
)

canvas.create_rectangle(
    616.0,
    0.0,
    960.0,
    540.0,
    fill="#D9D9D9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=680.0,
    y=221.0,
    width=216.0,
    height=53.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=680.0,
    y=321.0,
    width=216.0,
    height=53.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=680.0,
    y=421.0,
    width=216.0,
    height=53.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=680.0,
    y=121.0,
    width=216.0,
    height=53.0
)

canvas.create_text(
    866.0,
    529.0,
    anchor="nw",
    text="V 0.1 Brian Beard 2021",
    fill="#000000",
    font=("Roboto Bold", 9 * -1)
)

canvas.create_rectangle(
    0.0,
    0.0,
    960.0,
    90.0,
    fill="#187A00",
    outline="")

canvas.create_text(
    268.0,
    17.0,
    anchor="nw",
    text="NDSU Seed Archive",
    fill="#E4E800",
    font=("Roboto Bold", 48 * -1)
)
window.resizable(False, False)
window.mainloop()
