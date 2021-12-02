# Brian Beard

# Find menu class file.

# imports
from datetime import datetime
from sqlite3.dbapi2 import Cursor, Error
import tkinter as tk
from tkinter import IntVar, StringVar, messagebox
from pathlib import Path
import sqlite3 as sql
from tkinter.constants import END, HIDDEN

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Global database variables
currentdb = relative_to_assets("currentcrops.db")
archivedb = relative_to_assets("archivecrops.db")
barcodedb = relative_to_assets("barcodes.db")


def create_connection(db_file):
    """ Create the connection to the database. """
    conn = None

    try:
        conn = sql.connect(db_file)
    except sql.Error as e:
        print(e)

    return conn


def select_by_barcode(barcode=None):
    """ Sort by barcode. """

    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT * FROM currentcrop WHERE "Barcode ID" = '{barcode}'
        """
    )
    result = cursor.fetchall()

    for i in result:
        return i

    def show_results(self, label_num):
        """ Show results in the main menu labels. """
        if select_by_barcode():
            list = select_by_barcode()
            if list[label_num] is None:
                return "NA"
            else:
                return list[label_num]
        else:
            return "  "


def update_quantity(value, barcode):
    """ Updates the quantity in the database. """
    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    sql = f"""
    UPDATE currentcrop SET "Quantity (g)" = {value}
    WHERE "Barcode ID" = '{barcode}'
    """

    cursor.execute(sql)

    conn.commit()


def update_location(value, barcode):
    """ Updates the location in the database. """
    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    sql = f"""
    UPDATE currentcrop SET "Location" = {value}
    WHERE "Barcode ID" = '{barcode}'
    """

    cursor.execute(sql)

    conn.commit()


def update_notes(value, barcode):
    """ Updates the notes in the database. """
    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    sql = f"""
        UPDATE currentcrop SET "Notes" = {value}
        WHERE "Barcode ID" = '{barcode}'
    """

    cursor.execute(sql)

    conn.commit()


def update_germ(value, barcode):
    """ Updates the germ in the database. """
    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    sql = f"""
        UPDATE currentcrop SET "Germ %" = {value}
        WHERE "Barcode ID" = '{barcode}'
    """

    cursor.execute(sql)

    conn.commit()


def update_tkw(value, barcode):
    """ Updates the tkw in the database. """
    conn = create_connection(relative_to_assets(currentdb))

    cursor = conn.cursor()

    sql = f"""
        UPDATE currentcrop SET "TKW (g)" = {value}
        WHERE "Barcode ID" = '{barcode}'
    """

    cursor.execute(sql)

    conn.commit()


class MainMenu(tk.Frame):
    """ Find menu class. """

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

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
        self.text_date = tk.StringVar()

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
            590.0,
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

        self.canvas.create_text(
            624,
            509,
            anchor='nw',
            text="Date Edited",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        # Creating labels

        def update_labels():
            self.text_barcode.set(self.show_results(0))
            self.text_variety_id.set(self.show_results(1))
            self.text_variety_name.set(
                self.show_results(2))
            self.text_crop.set(self.show_results(3))
            self.text_source.set(self.show_results(4))
            self.text_year.set(self.show_results(5))
            self.text_quantity.set(float(self.show_results(6)))
            self.text_germ.set(self.show_results(7))
            self.text_tkw.set(self.show_results(8))
            self.text_location.set(self.show_results(9))
            self.text_designation.set(
                self.show_results(10))
            self.text_entrant.set(self.show_results(11))
            self.text_notes.set(self.show_results(12))
            self.text_date.set(self.date_convert())

        self.lbl_barcode = tk.Entry(
            textvariable=self.text_barcode,
            relief="raised",
            font=(None, 24),
            justify='center'
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
            y=584,
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
            font=(None, 18),
            wraplength=500,
            justify='left'
        )
        self.lbl_notes.place(
            x=162,
            y=859,
            width=699,
            height=125
        )

        self.lbl_date = tk.Label(
            textvariable=self.text_date,
            relief='raised',
            font=(None, 14)
        )
        self.lbl_date.place(
            x=757,
            y=503,
            width=164,
            height=40
        )

        # Horizontal seperator
        self.canvas.create_rectangle(
            0.0,
            656.0,
            1024.0,
            663.0,
            fill="#868686",
            outline="")

        # Scan button
        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("scan.png"))
        self.but_scan = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=update_labels,
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
            command=None,
            relief="flat"
        )
        self.but_new_entry.place(
            x=162.0,
            y=686.0,
            width=221.0,
            height=65.0
        )

        # Add quantity button
        self.button_image_3 = tk.PhotoImage(
            file=relative_to_assets("add_but.png"))
        self.but_add_quant = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_quantity,
            relief="flat"
        )
        self.but_add_quant.place(
            x=465.0,
            y=476.0,
            width=72.0,
            height=40.0
        )

        # Remove quantity button
        self.button_image_5 = tk.PhotoImage(
            file=relative_to_assets("rem_but.png"))
        self.but_rem_quant = tk.Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.remove_quantity,
            relief='flat'
        )

        self.but_rem_quant.place(
            x=465,
            y=527,
            width=72,
            height=40
        )

        # Inventory button
        self.button_image_4 = tk.PhotoImage(
            file=relative_to_assets("inventory.png"))
        self.but_inventory = tk.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="flat"
        )
        self.but_inventory.place(
            x=162,
            y=779,
            width=221,
            height=52
        )

        # Edit location button
        self.button_image_6 = tk.PhotoImage(
            file=relative_to_assets("edit.png"))
        self.but_edit_location = tk.Button(
            image=self.button_image_6,
            border=0,
            highlightthickness=0,
            command=self.change_location,
            relief='flat'
        )
        self.but_edit_location.place(
            x=465,
            y=341,
            width=61,
            height=40
        )

        # Edit tkw button
        self.but_edit_tkw = tk.Button(
            image=self.button_image_6,
            border=0,
            highlightthickness=0,
            command=self.change_tkw,
            relief='flat'
        )
        self.but_edit_tkw.place(
            x=465,
            y=584,
            width=61,
            height=40
        )

        # Edit germ button
        self.but_edit_germ = tk.Button(
            image=self.button_image_6,
            border=0,
            highlightthickness=0,
            command=self.change_germ,
            relief='flat'
        )
        self.but_edit_germ.place(
            x=927,
            y=584,
            width=61,
            height=40
        )

        # Edit notes button
        self.but_edit_notes = tk.Button(
            image=self.button_image_6,
            border=0,
            highlightthickness=0,
            command=self.change_notes,
            relief='flat'
        )
        self.but_edit_notes.place(
            x=874,
            y=902,
            width=61,
            height=40
        )

    def date_convert(self):
        """ Convert date to correct format. """
        date = self.show_results(13)
        date = date[:10]
        if date == 'NA':
            return "NA"
        else:
            new_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
            return new_date

    def show_results(self, label_num):
        """ Shows the results in the labels. """

        input = self.lbl_barcode.get()
        list = select_by_barcode(f"{input}")
        if list[label_num] is None:
            return "NA"
        else:
            return list[label_num]

    def add_quantity(self):
        """ Change the quantity. """
        value = QuantityPopupAdd(self).show()

        original = self.text_quantity.get()
        new = float(original) + value

        barcode = self.text_barcode.get()
        update_quantity(new, barcode)
        self.text_quantity.set(float(self.show_results(6)))

    def remove_quantity(self):
        """ Change the quantity. """
        value = QuantityPopupRemove(self).show()

        original = self.text_quantity.get()
        new = float(original) - value

        barcode = self.text_barcode.get()
        update_quantity(new, barcode)
        self.text_quantity.set(float(self.show_results(6)))

    def change_location(self):
        """ Change the location field. """
        value = LocationChangePopup(self).show()
        value = f'"{value}"'

        barcode = self.text_barcode.get()
        update_location(value, barcode)
        self.text_location.set(self.show_results(9))

    def change_notes(self):
        """ Change the notes field. """
        value = NotesChangePopup(self).show()
        value = f'"{value}"'

        barcode = self.text_barcode.get()
        update_notes(value, barcode)
        self.text_notes.set(self.show_results(12))

    def change_germ(self):
        """ Change the germ field. """
        value = GermTKWChangePopup(self).show()

        barcode = self.text_barcode.get()
        update_germ(value, barcode)
        self.text_germ.set(float(self.show_results(7)))

    def change_tkw(self):
        """ Change the tkw field. """
        value = GermTKWChangePopup(self).show()

        barcode = self.text_barcode.get()
        update_tkw(value, barcode)
        self.text_tkw.set(float(self.show_results(8)))


class QuantityPopupAdd(object):
    """ Quantity edit window. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.text_quantity_remove = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="How many grams to add?", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_quantity_remove).pack(pady=10, padx=5)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def show(self):
        """ Show the quantity window and return the grams to add or remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 250
        h = 100
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.text_quantity_remove.get()
        return float(value)


class QuantityPopupRemove(object):
    """ Quantity edit window. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.text_quantity_remove = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="How many grams to remove?", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_quantity_remove).pack(pady=10, padx=5)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def show(self):
        """ Show the quantity window and return the grams to remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 250
        h = 100
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.text_quantity_remove.get()
        return float(value)


class LocationChangePopup(object):
    """ Change location popup. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.location_change = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='left',
                         width=20, textvariable=self.location_change).pack(pady=10, padx=5)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def show(self):
        """ Show the quantity window and return the grams to add or remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 250
        h = 100
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.location_change.get()
        return str(value)


class NotesChangePopup(object):
    """ Change notes popup. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.text_notes = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(
            frm2, width=50, textvariable=self.text_notes, font=(None, 10))
        entry.pack(pady=10, padx=5)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def show(self):
        """ Show the quantity window and return the grams to add or remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 500
        h = 90
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.text_notes.get()
        return value


class GermTKWChangePopup(object):
    """ Germ edit window. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.text_germ_change = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_germ_change).pack(pady=10, padx=5)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def show(self):
        """ Show the quantity window and return the grams to remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 250
        h = 100
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.text_germ_change.get()
        return float(value)


def main():
    """ Run the program. """
    root = tk.Tk()

    w = 1024
    h = 1024
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw / 2) - (w / 2)
    y = (sh / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    app = MainMenu(root)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
