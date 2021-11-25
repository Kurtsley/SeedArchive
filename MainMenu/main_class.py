# Brian Beard

# Imports

import tkinter as tk
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main menu class


class MainMenu:
    """ Main menu class. """

    def __init__(self, master):
        self.master = master

        master.geometry("960x540")
        master.configure(bg="#FFFFFF")
        master.title("NDSU Seed Archive")
        master.resizable(False, False)

        # Placing assets

        self.canvas = tk.Canvas(
            master,
            bg="#FFFFFF",
            width=960,
            height=540,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = tk.PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            480,
            270,
            image=self.image_image_1
        )

        self.canvas.create_rectangle(
            616,
            0,
            960,
            540,
            fill="#D9D9D9",
            outline="")

        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="flat"
        )
        self.button_1.place(
            x=680,
            y=221,
            width=216,
            height=53
        )

        self.button_image_2 = tk.PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = tk.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="flat"
        )
        self.button_2.place(
            x=680,
            y=321,
            width=216,
            height=53
        )

        self.button_image_3 = tk.PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="flat"
        )
        self.button_3.place(
            x=680,
            y=421,
            width=216,
            height=53
        )

        self.button_image_4 = tk.PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = tk.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="flat"
        )
        self.button_4.place(
            x=680,
            y=121,
            width=216,
            height=53
        )

        self.canvas.create_text(
            866,
            529,
            anchor="nw",
            text="V 0.1 Brian Beard 2021",
            fill="#000000",
            font=("Roboto Bold", 9 * -1)
        )

        self.canvas.create_rectangle(
            0,
            0,
            960,
            90,
            fill="#187A00",
            outline=""
        )

        self.canvas.create_text(
            268,
            17,
            anchor="nw",
            text="NDSU Seed Archive",
            fill="#E4E800",
            font=("Roboto Bold", 48 * -1)
        )

        def launch_find_menu(self):
            """ Launch the find menu. """
            self.find_menu_window = tk.Toplevel(self.master)
            self.app = FindMenu(self.find_menu_window)


def main():
    """ Create main window. """
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
