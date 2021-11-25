# Brian Beard

# Find menu class file.

# imports
import tkinter as tk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class FindMenu:
    """ Find menu class. """

    def __init__(self, master):
        self.master = master

        master.geometry("1024x1024")
        master.configure(bg="#FFFFFF")
        master.title("NDSU Seed Archive")
        master.resizable(False, False)

        # Placing assets

        self.canvas = tk.Canvas(
            master,
            bg="#FFFFFF",
            height=1024,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            1024.0,
            90.0,
            fill="#187A00",
            outline="")

        self.canvas.create_text(
            255.0,
            17.0,
            anchor="nw",
            text="Seed Archive Find / Edit",
            fill="#E4E800",
            font=("Roboto Bold", 48 * -1)
        )

        self.canvas.create_rectangle(
            0.0,
            90.0,
            1024.0,
            1024.0,
            fill="#DADADA",
            outline="")

        self.canvas.create_text(
            480.0,
            826.0,
            anchor="nw",
            text="Notes",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            439.0,
            701.0,
            anchor="nw",
            text="Designation",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            580.0,
            766.0,
            anchor="nw",
            text="Entrant",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            102.0,
            348.0,
            anchor="nw",
            text="Location",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            91.0,
            266.0,
            anchor="nw",
            text="Variety ID",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            512.0,
            266.0,
            anchor="nw",
            text="Variety Name",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            606.0,
            348.0,
            anchor="nw",
            text="Crop",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            56.0,
            428.0,
            anchor="nw",
            text="Source",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            553.0,
            428.0,
            anchor="nw",
            text="Year (rcv)",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            68.0,
            509.0,
            anchor="nw",
            text="Quantity (g)",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            575.0,
            509.0,
            anchor="nw",
            text="Germ %",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            108.0,
            590.0,
            anchor="nw",
            text="TKW (g)",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_rectangle(
            459.0,
            134.0,
            952.0,
            199.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            202.0,
            260.0,
            459.0,
            300.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            202.0,
            341.0,
            459.0,
            381.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            666.0,
            341.0,
            921.0,
            381.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            139.0,
            422.0,
            459.0,
            462.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            665.0,
            422.0,
            921.0,
            462.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            666.0,
            503.0,
            921.0,
            543.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            202.0,
            503.0,
            459.0,
            543.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            666.0,
            760.0,
            921.0,
            800.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            575.0,
            695.0,
            921.0,
            735.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            202.0,
            584.0,
            459.0,
            624.0,
            fill="#C4C4C4",
            outline="")

        self.canvas.create_rectangle(
            162.0,
            859.0,
            861.0,
            984.0,
            fill="#C4C4C4",
            outline="")

        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("scan.png"))
        self.but_scan = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.but_scan.place(
            x=202.0,
            y=134.0,
            width=192.0,
            height=65.0
        )

        self.canvas.create_rectangle(
            666.0,
            260.0,
            921.0,
            300.0,
            fill="#C4C4C4",
            outline="")

        self.button_image_2 = tk.PhotoImage(
            file=relative_to_assets("new_entry.png"))
        self.but_new_entry = tk.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.but_new_entry.place(
            x=162.0,
            y=686.0,
            width=221.0,
            height=65.0
        )

        self.button_image_3 = tk.PhotoImage(
            file=relative_to_assets("edit_quant.png"))
        self.but_edit_quant = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.but_edit_quant.place(
            x=683.0,
            y=582.0,
            width=221.0,
            height=42.0
        )

        self.button_image_4 = tk.PhotoImage(
            file=relative_to_assets("inventory.png"))
        self.but_inventory = tk.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("invent"),
            relief="flat"
        )
        self.but_inventory.place(
            x=162,
            y=779,
            width=221,
            height=52
        )

        self.canvas.create_rectangle(
            0.0,
            656.0,
            1024.0,
            663.0,
            fill="#868686",
            outline="")


def main():
    root = tk.Tk()
    app = FindMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
