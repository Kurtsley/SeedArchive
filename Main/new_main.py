# Brian Beard

# Find menu class file.

# imports
import tkinter as tk
from pathlib import Path
import sqlite3 as sql

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_connection(db_file):
    """ Create the connection to the database. """
    conn = None

    try:
        conn = sql.connect(db_file)
    except sql.Error as e:
        print(e)

    return conn


def select_by_barcode(barcode):
    """ Sort by barcode. """

    list = []

    conn = create_connection(relative_to_assets("currentcrops.db"))

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT * FROM currentcrop WHERE "Barcode ID" = '{barcode}'
        """
    )
    result = cursor.fetchall()

    for i in result:
        return i


class MainMenu:
    """ Find menu class. """

    def __init__(self, master):
        self.master = master

        master.geometry("1024x1024")
        master.configure(bg="#FFFFFF")
        master.title("NDSU Seed Archive")
        master.resizable(False, False)

        # Setting up StringVar variables for updating labels

        self.text_barcode = tk.StringVar()
        self.text_variety_id = tk.StringVar()
        self.text_variety_name = tk.StringVar()
        self.text_location = tk.StringVar()
        self.text_crop = tk.StringVar()
        self.text_source = tk.StringVar()
        self.text_year = tk.StringVar()
        self.text_quantity = tk.StringVar()
        self.text_germ = tk.StringVar()
        self.text_tkw = tk.StringVar()
        self.text_designation = tk.StringVar()
        self.text_entrant = tk.StringVar()
        self.text_notes = tk.StringVar()

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

        # Creating labels

        self.text_barcode.set(self.show_results(0))
        self.text_variety_id.set(self.show_results(1))
        self.text_variety_name.set(self.show_results(2))
        self.text_crop.set(self.show_results(3))
        self.text_source.set(self.show_results(4))
        self.text_year.set(self.show_results(5))
        self.text_quantity.set(self.show_results(6))
        self.text_germ.set(self.show_results(7))
        self.text_tkw.set(self.show_results(8))
        self.text_location.set(self.show_results(9))
        self.text_designation.set(self.show_results(10))
        self.text_entrant.set(self.show_results(11))
        self.text_notes.set(self.show_results(12))

        self.lbl_barcode = tk.Label(
            textvariable=self.text_barcode,
            relief="raised",
            font=(None, 24)
        )
        self.lbl_barcode.place(
            x=459,
            y=134,
            width=493,
            height=65
        )

        self.lbl_variety_id = tk.Label(
            textvariable=self.text_variety_id,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_variety_id.place(
            x=202,
            y=260,
            width=257,
            height=40
        )

        self.lbl_variety_name = tk.Label(
            textvariable=self.text_variety_name,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_variety_name.place(
            x=666,
            y=260,
            width=255,
            height=40
        )

        self.lbl_location = tk.Label(
            textvariable=self.text_location,
            relief="raised",
            font=(None, 16)
        )
        self.lbl_location.place(
            x=202,
            y=341,
            width=257,
            height=40
        )

        self.lbl_crop = tk.Label(
            textvariable=self.text_crop,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_crop.place(
            x=666,
            y=341,
            width=255,
            height=40
        )

        self.lbl_source = tk.Label(
            textvariable=self.text_source,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_source.place(
            x=139,
            y=422,
            width=320,
            height=40
        )

        self.lbl_year = tk.Label(
            textvariable=self.text_year,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_year.place(
            x=665,
            y=422,
            width=256,
            height=40
        )

        self.lbl_quantity = tk.Label(
            textvariable=self.text_quantity,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_quantity.place(
            x=202,
            y=503,
            width=257,
            height=40
        )

        self.lbl_germ = tk.Label(
            textvariable=self.text_germ,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_germ.place(
            x=666,
            y=503,
            width=255,
            height=40
        )

        self.lbl_tkw = tk.Label(
            textvariable=self.text_tkw,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_tkw.place(
            x=202,
            y=584,
            width=257,
            height=40
        )

        self.lbl_designation = tk.Label(
            textvariable=self.text_designation,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_designation.place(
            x=575,
            y=695,
            width=346,
            height=40
        )

        self.lbl_entrant = tk.Label(
            textvariable=self.text_entrant,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_entrant.place(
            x=666,
            y=760,
            width=255,
            height=40
        )

        self.lbl_notes = tk.Label(
            textvariable=self.text_notes,
            relief="raised",
            font=(None, 18)
        )
        self.lbl_notes.place(
            x=162,
            y=859,
            width=699,
            height=125
        )

        # Scan button
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

        # New entry button
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

        # Edit quantity button
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

        # Inventory button
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

        # Horizontal seperator
        self.canvas.create_rectangle(
            0.0,
            656.0,
            1024.0,
            663.0,
            fill="#868686",
            outline="")

    def show_results(self, label_num):
        list = select_by_barcode("11409-SOYrr-SI-019")
        if list[label_num] is None:
            return "NA"
        else:
            return list[label_num]


def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
