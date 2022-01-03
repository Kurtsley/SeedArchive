# Brian Beard

# Find menu class file.

# imports
from datetime import datetime
from datetime import date
from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sqlite3 as sql
from tkinter.constants import BOTH, BOTTOM, END, HORIZONTAL, TOP
import pandas as pd
from tkinter import ttk
import sys
import traceback
import os
from tkinter import filedialog
import shutil

# Global paths and variables

if getattr(sys, 'frozen', False):
    """ Check if we are running in bundled mode or not. """
    OUTPUT_PATH = os.path.dirname(sys.executable)
else:
    OUTPUT_PATH = Path(__file__).parent

APP_VERSION = "0.2.4"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
DATA_PATH = OUTPUT_PATH / Path("./data")
BACKUP_PATH = OUTPUT_PATH / Path("./backup")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def relative_to_data(path: str) -> Path:
    return DATA_PATH / Path(path)


def relative_to_backup(path: str) -> Path:
    return BACKUP_PATH / Path(path)


# Global database variable
seedarchivedb = relative_to_data("seedarchivedb.db")


def create_version():
    """ Create a version file on start. """
    with open(relative_to_data("Version.txt"), "w") as f:
        f.write(APP_VERSION)


def create_connection(db_file):
    """ Create the connection to the database. """
    conn = None

    try:
        conn = sql.connect(db_file)
        return conn

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)


def test_connection():
    """ Test the sqlite3 connection. """
    conn = None

    try:
        conn = create_connection(seedarchivedb)
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()

        sql1 = """
            SELECT "Barcode ID" FROM currentcrop
        """
        sql2 = """
            SELECT "Barcode ID" FROM archivecrop
        """

        cursor1.execute(sql1)
        cursor2.execute(sql2)

        result1 = cursor1.fetchone()
        result2 = cursor2.fetchone()

        if result1 and result2:
            return True
        else:
            return False

    except sql.Error as e:
        pass

    finally:
        cursor1.close()
        cursor2.close()
        conn.close()


def select_by_barcode(barcode=None):
    """ Sort by barcode. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""SELECT * FROM currentcrop WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()

        for i in result:
            return i


def update_quantity(value, barcode):
    """ Updates the quantity in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Quantity (g)" = {round(value, 2)} WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def update_location(value, barcode):
    """ Updates the location in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Location" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def update_notes(value, barcode):
    """ Updates the notes in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Notes" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def update_germ(value, barcode):
    """ Updates the germ in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Germ %" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def update_tkw(value, barcode):
    """ Updates the tkw in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "TKW (g)" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def update_date(value, barcode):
    """ Updates the date to the current date in the database. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f""" UPDATE currentcrop SET "Date Edited" = '{value}' WHERE "Barcode ID" = '{barcode}' """

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()


def max_variety_id():
    """ Finds the max variety id and adds one. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""SELECT MAX("Variety ID") FROM currentcrop"""

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()

        for i in result:
            return i


def add_entry(barcode, varietyid, varietyname, crop, source, year, quantity, germ, tkw, location, designation, entrant, notes, date):
    """ Add a new row to the database. """
    conn = create_connection(seedarchivedb)

    cursor = conn.cursor()

    sql1 = """INSERT INTO currentcrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    sql2 = """INSERT INTO archivecrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    record = (barcode, varietyid, varietyname, crop, source, year,
              quantity, germ, tkw, location, designation, entrant, notes, date)

    try:
        cursor.execute(sql1, record)
        cursor.execute(sql2, record)
        conn.commit()

    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        cursor.close()
        conn.close()


def add_to_archive(barcode, varietyid, varietyname, crop, source, year, quantity, germ, tkw, location, designation, entrant, notes, date):
    """ Add an entry to the archive when a change is made. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = """INSERT INTO archivecrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    record = (barcode, varietyid, varietyname, crop, source, year,
              quantity, germ, tkw, location, designation, entrant, notes, date)

    try:
        cursor.execute(sql, record)
        conn.commit()

    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        cursor.close()
        conn.close()


def delete_entry(barcode):
    """ Delete an entry from the currentcrop table when thrown out. """
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = f"""
        DELETE FROM currentcrop WHERE "Barcode ID" = '{barcode}' """

    try:
        cursor.execute(sql)
        conn.commit()
    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        cursor.close()
        conn.close()


def sql_to_dataframe():
    """ Take the current database and return a dataframe. """
    conn = create_connection(seedarchivedb)

    sql = """SELECT * FROM currentcrop ORDER BY "Year (rcv)" DESC"""
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=['Barcode ID', 'Variety ID', 'Variety', 'Crop', 'Source', 'Year (rcv)',
                      'Quantity (g)', 'Germ %', 'TKW (g)', 'Location', 'Designation / Project', 'Entrant', 'Notes', 'Date Edited'])

    conn.close()
    return df


def sql_recent_list():
    conn = create_connection(seedarchivedb)
    cursor = conn.cursor()

    sql = """ SELECT "Barcode ID" FROM currentcrop WHERE "Barcode ID" IS NOT NULL ORDER BY "Date Edited" DESC LIMIT 10 """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except sql.Error as e:
        messagebox.showerror(title="SQL Error", message=e)

    finally:
        cursor.close()
        conn.close()

        return result


def sql_history_dataframe(barcode):
    """ Return a dataframe of a specific barcode in archive. """
    conn = create_connection(seedarchivedb)

    sql = f"""SELECT * FROM archivecrop WHERE "Barcode ID" = '{barcode}' ORDER BY "Date Edited" DESC"""
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=['Barcode ID', 'Variety ID', 'Variety', 'Crop', 'Source', 'Year (rcv)',

                      'Quantity (g)', 'Germ %', 'TKW (g)', 'Location', 'Designation / Project', 'Entrant', 'Notes', 'Date Edited'])

    conn.close()
    return df


def sql_all_todataframe():
    """ Return all entries in a dataframe. """
    conn = create_connection(seedarchivedb)

    sql = """SELECT "Barcode ID", "Year (rcv)", "Date Edited" FROM currentcrop """
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=[
                      'Barcode ID', 'Year (rcv)', 'Date Edited'])

    conn.close()
    return df


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
        self.text_barcode_hidden = tk.StringVar()
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

        # Connection stringvar
        self.text_connected = tk.StringVar()

        # Connection test
        if test_connection():
            self.text_connected.set("Connected")
        else:
            messagebox.showerror(title="Connection Error",
                                 message="Not Connected!")

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

        self.canvas.create_text(
            540,
            220,
            anchor='nw',
            text="Current Barcode",
            fill="#000000",
            font=("Roboto Bold", 16 * -1)
        )

        # Creating labels

        # Connected label
        self.lbl_connected = tk.Label(
            textvariable=self.text_connected,
            font=(None, 9),
            justify='center'
        )
        self.lbl_connected.place(
            x=18,
            y=1004,
            width=65,
            height=14
        )

        # Other labels
        self.lbl_barcode = tk.Entry(
            textvariable=self.text_barcode,
            relief="raised",
            font=(None, 24),
            justify='center'
        )
        self.lbl_barcode.focus_force()
        #
        # This focuses the cursor on the barcode entry at the start of the
        # program.

        self.lbl_barcode.bind('<Return>', self.get_barcode)
        #
        # Binds the return key to the get_barcode function which is the same as
        # the scan button.

        self.lbl_barcode.place(
            x=459,
            y=134,
            width=493,
            height=65
        )

        # Label for barcode viewing and retrieval
        self.lbl_barcode_hidden = tk.Entry(
            textvariable=self.text_barcode_hidden,
            relief='raised',
            font=(None, 14),
            justify='center'
        )
        self.lbl_barcode_hidden.place(
            x=666,
            y=213,
            width=255,
            height=34
        )
        self.lbl_barcode_hidden.bind('<Return>', self.get_barcode)

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

        # Menu Bar
        menubar = MainMenuBar(master)
        master.config(menu=menubar)

        # History button
        self.but_image_7 = tk.PhotoImage(
            file=relative_to_assets("history.png"))
        self.but_history = tk.Button(
            image=self.but_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_history,
            relief='flat'
        )
        self.but_history.place(
            x=43,
            y=124,
            width=117,
            height=40
        )

        # Discard button
        self.but_image_9 = tk.PhotoImage(
            file=relative_to_assets("Discard.png"))
        self.but_discard = tk.Button(
            image=self.but_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.discard_barcode(), self.archive_on_update()],
            relief='flat',
            bg="#DADADA"
        )
        self.but_discard.place(
            x=465,
            y=365,
            width=103,
            height=40
        )

        # Scan button
        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("scan.png"))
        self.but_scan = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.get_barcode,
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
            command=self.open_entry,
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
            command=lambda: [self.add_quantity(), self.archive_on_update()],
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
            command=lambda: [self.remove_quantity(), self.archive_on_update()],
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
            command=self.open_table,
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
            command=lambda: [self.change_location(), self.archive_on_update()],
            relief='flat'
        )
        self.but_edit_location.place(
            x=465,
            y=317,
            width=61,
            height=40
        )

        # Edit tkw button
        self.but_edit_tkw = tk.Button(
            image=self.button_image_6,
            border=0,
            highlightthickness=0,
            command=lambda: [self.change_tkw(), self.archive_on_update()],
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
            command=lambda: [self.change_germ(), self.archive_on_update()],
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
            command=lambda: [self.change_notes(), self.archive_on_update()],
            relief='flat'
        )
        self.but_edit_notes.place(
            x=874,
            y=902,
            width=61,
            height=40
        )

        # Export to word button
        self.but_image_8 = tk.PhotoImage(
            file=relative_to_assets('Export.png')
        )
        self.but_export = tk.Button(
            image=self.but_image_8,
            border=0,
            highlightthickness=0,
            command=self.excel_export,
            relief='flat'
        )
        self.but_export.place(
            x=43,
            y=178,
            width=117,
            height=40
        )

    def update_labels(self):
        self.text_barcode.set(self.show_results(0))
        self.text_barcode_hidden.set(self.show_results(0))
        self.text_variety_id.set(self.show_results(1))
        self.text_variety_name.set(
            self.show_results(2))
        self.text_crop.set(self.show_results(3))
        self.text_source.set(self.show_results(4))
        self.text_year.set(self.show_results(5))
        self.text_quantity.set(self.show_results(6))
        self.text_germ.set(self.show_results(7))
        self.text_tkw.set(self.show_results(8))
        self.text_location.set(self.show_results(9))
        self.text_designation.set(
            self.show_results(10))
        self.text_entrant.set(self.show_results(11))
        self.text_notes.set(self.show_results(12))
        self.text_date.set(self.date_convert())

    def archive_on_update(self):
        """ Retrieve all the text for archiving purposes. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                pass
            else:
                varietyid = self.text_variety_id.get()
                varietyname = self.text_variety_name.get()
                crop = self.text_crop.get()
                source = self.text_source.get()
                year = self.text_year.get()
                quantityold = self.text_quantity.get()
                if quantityold == "":
                    quantity = "None"
                else:
                    quantity = float(quantityold)
                entrant = self.text_entrant.get()
                germold = self.text_germ.get()
                if germold == "None":
                    germ = "None"
                else:
                    germ = float(germold)
                tkw = self.text_tkw.get()
                location = self.text_location.get()
                designation = self.text_designation.get()
                notes = self.text_notes.get()
                date = self.show_results(13)

                add_to_archive(barcode, varietyid, varietyname, crop, source, year,
                               quantity, germ, tkw, location, designation, entrant, notes, date)
        except Exception as e:
            messagebox.showerror(title="Error", message=e)
            pass

    def date_convert(self):
        """ Convert date to correct format. """
        date = self.show_results(13)
        if len(date) == 10:
            return date
        else:
            date = date[:10]
            if date:
                return date
            else:
                return "NA"

    def show_results(self, label_num):
        """ Shows the results in the labels. """

        input = self.lbl_barcode_hidden.get()
        list = select_by_barcode(f"{input}")
        if list[label_num] is None:
            return "None"
        else:
            return list[label_num]

    def current_date(self):
        """ Sets the edited date to current date. """
        time = datetime.now()
        dateformat = time.strftime("%Y-%m-%d %H:%M:%S")
        barcode = self.text_barcode_hidden.get()
        update_date(dateformat, barcode)
        self.text_date.set(self.date_convert())

    def add_quantity(self):
        """ Change the quantity. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = QuantityPopupAdd(self).show()
                original = self.text_quantity.get()
                new = float(original) + value
                update_quantity(new, barcode)
                self.current_date()
                self.text_quantity.set(float(self.show_results(6)))
        except Exception:
            pass

    def remove_quantity(self):
        """ Change the quantity. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = QuantityPopupRemove(self).show()
                original = self.text_quantity.get()
                new = float(original) - value
                update_quantity(new, barcode)
                self.current_date()
                self.text_quantity.set(float(self.show_results(6)))
        except Exception:
            pass

    def change_location(self):
        """ Change the location field. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = LocationChangePopup(self).show()
                if value == "":
                    pass
                else:
                    update_location(value, barcode)
                    self.current_date()
                    self.text_location.set(self.show_results(9))
        except Exception:
            pass

    def discard_barcode(self):
        """ Delete the barcode from the currentcrop table. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = "THROWN OUT"
                update_location(value, barcode)
                self.current_date()
                self.text_location.set(self.show_results(9))
                delete_entry(barcode)
        except Exception:
            pass

    def change_notes(self):
        """ Change the notes field. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = NotesChangePopup(self).show()
                update_notes(value, barcode)
                self.current_date()
                self.text_notes.set(self.show_results(12))
        except Exception:
            pass

    def change_germ(self):
        """ Change the germ field. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = GermTKWChangePopup(self).show()
                update_germ(value, barcode)
                self.current_date()
                self.text_germ.set(float(self.show_results(7)))
        except Exception:
            pass

    def change_tkw(self):
        """ Change the tkw field. """
        try:
            barcode = self.text_barcode_hidden.get()
            if barcode == "":
                messagebox.showerror(
                    title="Error", message="No barcode scanned!")
                pass
            else:
                value = GermTKWChangePopup(self).show()
                update_tkw(value, barcode)
                self.current_date()
                self.text_tkw.set(float(self.show_results(8)))
        except Exception:
            pass

    def clear_barcode(self):
        """ Clear the barcode entry. """
        self.lbl_barcode.delete(0, END)

    def get_barcode(self, event=None):
        """ Get the barcode scan from the scanner. """
        try:
            value = self.lbl_barcode.get()
            if value == "":
                pass
            else:
                # This is necessary in case the barcode has any space around it
                # when scanned. It is present in the excel file so this is a
                # precaution.
                value = value.strip()
                self.text_barcode.set(value)
                self.text_barcode_hidden.set(value)

                # Update the entry widgets and then clear the barcode field for
                # future scanning.
                self.update_labels()
                self.clear_barcode()

        except Exception:
            pass

    def open_entry(self):
        try:
            EntryMenu(self).show()
        except Exception:
            pass

    def open_table(self):
        TableView(self).show()

    def open_history(self):
        barcode = self.text_barcode_hidden.get()
        if barcode == "":
            messagebox.showerror(title="Error", message="No barcode scanned!")
            pass
        else:
            HistoryView(self, barcode).show()

    def excel_export(self):
        """ Export the barcode to an excel file. """
        df = sql_all_todataframe()
        df.to_excel(relative_to_data("barcodes.xlsx"), index=False)
        try:
            os.startfile(relative_to_data("barcodes.xlsx"))
        except Error as e:
            messagebox.showerror(title="Excel Error", message=e)

    def set_barcode(self, value):
        """ Set the barcode for use in another class. """
        self.text_barcode.set(value)

    def save_database(self):
        """ Saves the database with a current date timestamp. """
        today = date.today()
        dateformat = today.strftime('%Y-%m-%d')

        source = seedarchivedb

        try:
            f = filedialog.asksaveasfile(initialfile=f'{dateformat}.db',
                                         defaultextension=".db", filetypes=[("Database Files", "*.db")], initialdir=relative_to_backup("."))
            if f is None:
                pass
            else:
                shutil.copy(source, f.name)

                messagebox.showinfo(title="File saved",
                                    message=f"{dateformat}.db has been saved")
        except Error as e:
            messagebox.showerror(title="Save Error", message=e)
            pass

    def load_database(self):
        """ Load the saved database. """
        today = date.today()
        dateformat = today.strftime('%Y-%m-%d')
        try:
            source = filedialog.askopenfilename(title="Choose database file.")
            if source == "":
                pass
            else:
                shutil.copy(seedarchivedb, relative_to_backup(
                    f"{dateformat}.db"))

                dest = seedarchivedb

                shutil.copy(source, dest)

                messagebox.showinfo(
                    title="Load", message=f"Successfully loaded {source}")
        except Error as e:
            messagebox.showerror(title=f"Load Error", message=e)
            pass


class MainMenuBar(tk.Menu):
    """ Class for main menu bar. """

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        filemenu = tk.Menu(self, tearoff=False)
        recentmenu = tk.Menu(self, tearoff=False)

        list = sql_recent_list()

        self.barcode_vars = tk.StringVar()

        for x in list:
            recentmenu.add_radiobutton(
                label=x, value=x, variable=self.barcode_vars, command=self.select_barcode)

        self.add_cascade(label="File", underline=0, menu=filemenu)

        filemenu.add_cascade(label="Recent Barcodes", menu=recentmenu)
        filemenu.add_command(label="Save Database", command=self.save)
        filemenu.add_command(label="Load Database", command=self.load)
        filemenu.add_command(label="About", command=self.about)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close)

    def select_barcode(self):
        """ Select the barcode from the recent menu. """
        m = MainMenu(self.master)
        m.set_barcode(self.barcode_vars.get())
        m.get_barcode()
        sql_recent_list()

    def save(self):
        """ Save the database. """
        m = MainMenu(self.master)
        m.save_database()

    def load(self):
        """ Load a database. """
        m = MainMenu(self.master)
        m.load_database()

    def about(self):
        """ Version info popup. """
        AboutPopup(self).show()

    def close(self):
        """ Exit program. """
        sys.exit(0)


class AboutPopup(object):
    """ Version Popup. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("About")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.close)

        self.lbl = tk.Label(
            self.master, text=f"SeedArchive v{APP_VERSION}\n2021 Beard Industries")
        self.lbl.place(relx=.5, rely=.3, anchor='center')

        self.btn = tk.Button(self.master, anchor='center',
                             width=7, height=2, text="OK", command=self.close)
        self.btn.pack(side="bottom", pady=5)

    def close(self, event=None):
        self.master.destroy()

    def show(self):
        """ Show the popup. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 250
        h = 100
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)


class QuantityPopupAdd(object):
    """ Quantity edit window. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Edit Quantity")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.close)

        self.text_quantity_remove = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="How many grams to add?", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_quantity_remove)
        entry.pack(pady=10, padx=5)
        entry.focus()

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def close(self, event=None):
        self.master.destroy()

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

        self.master.bind('<Return>', self.close)

        self.text_quantity_remove = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="How many grams to remove?", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_quantity_remove)
        entry.pack(pady=10, padx=5)
        entry.focus()

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def close(self, event=None):
        self.master.destroy()

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
        self.master.title("Edit Location")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.close)

        self.location_change = tk.StringVar()

        self.locations = ('Cabinet 1 / Shelf 1', 'Cabinet 1 / Shelf 2', 'Cabinet 1 / Shelf 3', 'Cabinet 1 / Shelf 4', 'Cabinet 1 / Shelf 5', 'Cabinet 2 / Shelf 1', 'Cabinet 2 / Shelf 2', 'Cabinet 2 / Shelf 3', 'Cabinet 2 / Shelf 4', 'Cabinet 2 / Shelf 5', 'Cabinet 3 / Shelf 1', 'Cabinet 3 / Shelf 2', 'Cabinet 3 / Shelf 3', 'Cabinet 3 / Shelf 4', 'Cabinet 3 / Shelf 5', 'Cabinet 4 / Shelf 1', 'Cabinet 4 / Shelf 2', 'Cabinet 4 / Shelf 3', 'Cabinet 4 / Shelf 4',
                          'Cabinet 4 / Shelf 5', 'Cabinet 5 / Shelf 1', 'Cabinet 5 / Shelf 2', 'Cabinet 5 / Shelf 3', 'Cabinet 5 / Shelf 4', 'Cabinet 5 / Shelf 5', 'Cabinet 6 / Shelf 1', 'Cabinet 6 / Shelf 2', 'Cabinet 6 / Shelf 3', 'Cabinet 6 / Shelf 4', 'Cabinet 6 / Shelf 5', 'Cabinet 7 / Shelf 1', 'Cabinet 7 / Shelf 2', 'Cabinet 7 / Shelf 3', 'Cabinet 7 / Shelf 4', 'Cabinet 7 / Shelf 5', 'Cabinet 8 / Shelf 1', 'Cabinet 8 / Shelf 2', 'Cabinet 8 / Shelf 3', 'Cabinet 8 / Shelf 4', 'Cabinet 8 / Shelf 5', 'Cabinet 9 / Shelf 1', 'Cabinet 9 / Shelf 2', 'Cabinet 9 / Shelf 3', 'Cabinet 9 / Shelf 4', 'Cabinet 9 / Shelf 5', 'Cabinet 10 / Shelf 1', 'Cabinet 10 / Shelf 2', 'Cabinet 10 / Shelf 3', 'Cabinet 10 / Shelf 4', 'Cabinet 10 / Shelf 5', 'Cabinet 11 / Shelf 1', 'Cabinet 11 / Shelf 2', 'Cabinet 11 / Shelf 3', 'Cabinet 11 / Shelf 4', 'Cabinet 11 / Shelf 5', 'Open Shelf 1 / Shelf 1', 'Open Shelf 1 / Shelf 2', 'Open Shelf 1 / Shelf 3', 'Open Shelf 1 / Shelf 4', 'Open Shelf 2 / Shelf 1', 'Open Shelf 2 / Shelf 2', 'Open Shelf 2 / Shelf 3', 'Open Shelf 2 / Shelf 4', 'Open Shelf 2 / Shelf 5', 'Cart')

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        self.location_menu = tk.OptionMenu(
            frm2,
            self.location_change,
            * self.locations,
            command=None
        )
        self.location_menu.pack()

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def close(self, event=None):
        self.master.destroy()

    def show(self):
        """ Show the quantity window and return the grams to add or remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 270
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
        self.master.title("Edit Notes")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.close)

        self.text_notes = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter Notes:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(
            frm2, width=50, textvariable=self.text_notes, font=(None, 10))
        entry.pack(pady=10, padx=5)
        entry.focus()

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def close(self, event=None):
        self.master.destroy()

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
        self.master.title("Edit Value")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.close)

        self.text_germ_change = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=5, textvariable=self.text_germ_change)
        entry.pack(pady=10, padx=5)
        entry.focus()

        btn = tk.Button(self.master, text="Accept", padx=10,
                        command=self.master.destroy)
        btn.grid(row=1, column=2, columnspan=2)

    def close(self, event=None):
        self.master.destroy()

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


class EntryMenu(object):
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("New Entry")
        self.master.grab_set()
        self.master.resizable(False, False)

        self.master.bind('<Return>', self.set_barcode)

        self.canvas = tk.Canvas(
            self.master,
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
            308.0,
            17.0,
            anchor="nw",
            text="Seed Archive Entry",
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
            241.0,
            153.0,
            anchor="nw",
            text="Barcode",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            420.0,
            821.0,
            anchor="nw",
            text="Notes",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            202.0,
            701.0,
            anchor="nw",
            text="Designation",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_text(
            346.0,
            767.0,
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
            534.0,
            509.0,
            anchor="nw",
            text="Date Edited",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        # List variables for the optionmenus
        self.locations = ('Cabinet 1 / Shelf 1', 'Cabinet 1 / Shelf 2', 'Cabinet 1 / Shelf 3', 'Cabinet 1 / Shelf 4', 'Cabinet 1 / Shelf 5', 'Cabinet 2 / Shelf 1', 'Cabinet 2 / Shelf 2', 'Cabinet 2 / Shelf 3', 'Cabinet 2 / Shelf 4', 'Cabinet 2 / Shelf 5', 'Cabinet 3 / Shelf 1', 'Cabinet 3 / Shelf 2', 'Cabinet 3 / Shelf 3', 'Cabinet 3 / Shelf 4', 'Cabinet 3 / Shelf 5', 'Cabinet 4 / Shelf 1', 'Cabinet 4 / Shelf 2', 'Cabinet 4 / Shelf 3', 'Cabinet 4 / Shelf 4',
                          'Cabinet 4 / Shelf 5', 'Cabinet 5 / Shelf 1', 'Cabinet 5 / Shelf 2', 'Cabinet 5 / Shelf 3', 'Cabinet 5 / Shelf 4', 'Cabinet 5 / Shelf 5', 'Cabinet 6 / Shelf 1', 'Cabinet 6 / Shelf 2', 'Cabinet 6 / Shelf 3', 'Cabinet 6 / Shelf 4', 'Cabinet 6 / Shelf 5', 'Cabinet 7 / Shelf 1', 'Cabinet 7 / Shelf 2', 'Cabinet 7 / Shelf 3', 'Cabinet 7 / Shelf 4', 'Cabinet 7 / Shelf 5', 'Cabinet 8 / Shelf 1', 'Cabinet 8 / Shelf 2', 'Cabinet 8 / Shelf 3', 'Cabinet 8 / Shelf 4', 'Cabinet 8 / Shelf 5', 'Cabinet 9 / Shelf 1', 'Cabinet 9 / Shelf 2', 'Cabinet 9 / Shelf 3', 'Cabinet 9 / Shelf 4', 'Cabinet 9 / Shelf 5', 'Cabinet 10 / Shelf 1', 'Cabinet 10 / Shelf 2', 'Cabinet 10 / Shelf 3', 'Cabinet 10 / Shelf 4', 'Cabinet 10 / Shelf 5', 'Cabinet 11 / Shelf 1', 'Cabinet 11 / Shelf 2', 'Cabinet 11 / Shelf 3', 'Cabinet 11 / Shelf 4', 'Cabinet 11 / Shelf 5', 'Open Shelf 1 / Shelf 1', 'Open Shelf 1 / Shelf 2', 'Open Shelf 1 / Shelf 3', 'Open Shelf 1 / Shelf 4', 'Open Shelf 2 / Shelf 1', 'Open Shelf 2 / Shelf 2', 'Open Shelf 2 / Shelf 3', 'Open Shelf 2 / Shelf 4', 'Open Shelf 2 / Shelf 5', 'Cart', 'THROWN OUT')
        self.crops = ('Alfalfa', 'Barley', 'RR Canola', 'Carinata', 'Corn', 'Dry Bean', 'Faba Bean', 'Field Pea', 'Flax', 'Lentil', 'Millet', 'Oat', 'Onion',
                      'Perenial Grass', 'Safflower', 'RR Soybean', 'Sunflower', 'Wheat, Durum', 'Wheat, Spring', 'Wheat, Winter', 'Conv Soybean', 'Conv Canola', 'Chickpea')
        self.sources = ('Drill Strip', 'Breeder / University',
                        'Company', 'Seed Increase', 'Other')
        self.designations = ('Border Seed', 'Dryland - Agronomic Trial', 'Dryland - Drill Strip', 'Dryland - Variety Trial',
                             'Extension Trial', 'Irrigation - Agronomic Trial', 'Irrigation - Variety Trial', 'Pathology Trial')

        # Stringvars for optionmenus
        self.location_menu_var = tk.StringVar()
        self.crop_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.designation_var = tk.StringVar()

        # Text variables for entry widgets
        self.text_date = tk.StringVar()
        self.text_varietyid = tk.StringVar()
        self.text_barcode = tk.StringVar()
        self.text_varietyname = tk.StringVar()
        self.text_year = tk.StringVar()
        self.text_quantity = tk.StringVar()
        self.text_tkw = tk.StringVar()
        self.text_germ = tk.StringVar()
        self.text_entrant = tk.StringVar()
        self.text_notes = tk.StringVar()

        # Functions to call when the window opens
        self.current_date()
        self.set_variety_id()

        # Create the widgets
        self.lbl_barcode = tk.Entry(
            self.master,
            relief='raised',
            font=(None, 24),
            justify='center',
            textvariable=self.text_barcode
        )
        self.lbl_barcode.place(
            x=339,
            y=137,
            width=493,
            height=65
        )

        self.lbl_varietyid = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_varietyid
        )
        self.lbl_varietyid.place(
            x=202,
            y=260,
            width=257,
            height=40
        )

        self.lbl_varietyname = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_varietyname
        )
        self.lbl_varietyname.place(
            x=666,
            y=260,
            width=255,
            height=40
        )

        self.lbl_location = tk.OptionMenu(
            self.master,
            self.location_menu_var,
            *self.locations,
            command=None
        )
        self.lbl_location.config(font=(None, 18))
        self.lbl_location.place(
            x=202,
            y=341,
            width=257,
            height=40
        )

        self.lbl_crop = tk.OptionMenu(
            self.master,
            self.crop_var,
            *self.crops,
            command=self.set_barcode
        )
        self.lbl_crop.config(font=(None, 18))
        self.lbl_crop.place(
            x=666,
            y=341,
            width=255,
            height=40
        )

        self.lbl_source = tk.OptionMenu(
            self.master,
            self.source_var,
            *self.sources,
            command=self.set_barcode
        )
        self.lbl_source.config(font=(None, 18))
        self.lbl_source.place(
            x=139,
            y=422,
            width=320,
            height=40
        )

        self.lbl_year = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_year
        )
        self.lbl_year.place(
            x=666,
            y=422,
            width=256,
            height=40
        )

        self.lbl_quantity = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_quantity
        )
        self.lbl_quantity.place(
            x=202,
            y=503,
            width=257,
            height=40
        )

        self.lbl_date = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_date
        )
        self.lbl_date.place(
            x=665,
            y=503,
            width=256,
            height=40
        )

        self.lbl_tkw = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_tkw
        )
        self.lbl_tkw.place(
            x=202,
            y=584,
            width=257,
            height=40
        )

        self.lbl_germ = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_germ
        )
        self.lbl_germ.place(
            x=666,
            y=584,
            width=255,
            height=40
        )

        self.lbl_designation = tk.OptionMenu(
            self.master,
            self.designation_var,
            *self.designations,
            command=self.set_barcode
        )
        self.lbl_designation.config(font=(None, 18))
        self.lbl_designation.place(
            x=339,
            y=695,
            width=346,
            height=40
        )

        self.lbl_entrant = tk.Entry(
            self.master,
            relief='raised',
            justify='center',
            font=(None, 18),
            textvariable=self.text_entrant
        )
        self.lbl_entrant.place(
            x=430,
            y=761,
            width=255,
            height=40
        )

        self.lbl_notes = tk.Entry(
            self.master,
            relief='raised',
            font=(None, 14),
            textvariable=self.text_notes
        )
        self.lbl_notes.place(
            x=102,
            y=855,
            width=699,
            height=125
        )

        self.canvas.create_rectangle(
            757.0,
            503.0,
            921.0,
            543.0,
            fill="#C4C4C4",
            outline="")

        # Set quantity and germ to 0 to avoid a Nonetype error when trying to add or
        # subtract in the main window.
        self.lbl_quantity.insert(END, 0)
        self.lbl_germ.insert(END, 0)

        # Accept button
        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets(("accept.png")))
        self.but_accept = tk.Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.set_barcode(), self.master.destroy()],
            relief="flat"
        )

        self.but_accept.image = self.button_image_1
        self.but_accept.place(
            x=845.0,
            y=883.0,
            width=139.0,
            height=69.0
        )

    def current_date(self):
        """ Sets the edited date to current date. """
        time = datetime.now()
        dateformat = time.strftime("%Y-%m-%d %H:%M:%S")
        self.text_date.set(dateformat)

    def set_variety_id(self):
        """ Sets the variety id. """
        value = max_variety_id()
        value = value[0]
        varietyid = value + 1
        self.text_varietyid.set(varietyid)

    def set_barcode(self, event=None):
        """ Sets the barcode based on crop, source, variety id, and year. """
        varietyid = self.text_varietyid.get()

        # Shorten crop
        crop = self.crop_var.get()
        crop_sort = self.sort_crop(crop)

        # Shorten source
        source = self.source_var.get()
        source_sort = self.sort_source(source)

        year_rcv = self.text_year.get()
        if year_rcv == "":
            short_year = "UK"
        else:
            short_year = str(year_rcv[1:])

        # Build barcode
        barcode = f"{varietyid}-{crop_sort}-{source_sort}-{short_year}"
        self.text_barcode.set(barcode)

    def sort_crop(self, crop):
        """ Sorts the crop and spits out a shortened version. """
        if crop == "Alfalfa":
            return "ALF"
        elif crop == "Barley":
            return "BAR"
        elif crop == "RR Canola":
            return "CANrr"
        elif crop == "Carinata":
            return "CAR"
        elif crop == "Corn":
            return "COR"
        elif crop == "Dry Bean":
            return "DB"
        elif crop == "Faba Bean":
            return "FAB"
        elif crop == "Field Pea":
            return "PEA"
        elif crop == "Flax":
            return "FLX"
        elif crop == "Lentil":
            return "LEN"
        elif crop == "Millet":
            return "MIL"
        elif crop == "Oat":
            return "OAT"
        elif crop == "Onion":
            return "ON"
        elif crop == "Perenial Grass":
            return "PG"
        elif crop == "Safflower":
            return "SAF"
        elif crop == "RR Soybean":
            return "SOYrr"
        elif crop == "Sunflower":
            return "SUN"
        elif crop == "Wheat, Durum":
            return "DUR"
        elif crop == "Wheat, Spring":
            return "SPW"
        elif crop == "Wheat, Winter":
            return "WIW"
        elif crop == "Conv Soybean":
            return "SOYconv"
        elif crop == "Conv Canola":
            return "CANconv"
        elif crop == "Chickpea":
            return "CHP"
        else:
            return "UK"

    def sort_source(self, source):
        """ Sort the source and return shortened version. """
        if source == "Drill Strip":
            return "DS"
        elif source == "Breeder / University":
            return "BREED"
        elif source == "Company":
            return "COMP"
        elif source == "Seed Increase":
            return "SI"
        elif source == "Other":
            return "OTH"
        else:
            return "UK"

    def return_all(self):
        """ Return all values. """
        barcode = self.text_barcode.get()
        date = self.text_date.get()
        varietyid = self.text_varietyid.get()
        varietyname = self.text_varietyname.get()
        year = self.text_year.get()
        quantity = self.text_quantity.get()
        tkw = self.text_tkw.get()
        germ = self.text_germ.get()
        entrant = self.text_entrant.get()
        notes = self.text_notes.get()
        location = self.location_menu_var.get()
        crop = self.crop_var.get()
        source = self.source_var.get()
        designation = self.designation_var.get()

        list = [barcode, date, varietyid, varietyname, year, quantity,
                tkw, germ, entrant, notes, location, crop, source, designation]
        return list

    def show(self):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 1024
        h = 1024
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        values = self.return_all()

        # Check for an emtpy barcode and pass if true.
        if values[0] == "":
            pass
        else:
            # Seperate the list by value
            barcode = values[0]
            date = values[1]
            varietyid = values[2]
            varietyname = values[3]
            year = values[4]
            quantity = values[5]
            tkw = values[6]
            germ = values[7]
            entrant = values[8]
            notes = values[9]
            location = values[10]
            crop = values[11]
            source = values[12]
            designation = values[13]

            add_entry(barcode, varietyid, varietyname, crop, source, year,
                      quantity, germ, tkw, location, designation, entrant, notes, date)


class TableView(object):
    """ Show a filterable table. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Archive")
        self.master.grab_set()
        self.master.resizable(False, False)
        self.master.state("zoomed")

        self.df = sql_to_dataframe()
        self.df["Variety ID"] = self.df["Variety ID"].fillna(0).astype(int)

        self.df["Germ %"].fillna(value="None", inplace=True)
        self.df["TKW (g)"].fillna(value="None", inplace=True)

        self.tree = ttk.Treeview(self.master)
        self.tree['show'] = 'headings'
        columns = list(self.df.columns)

        self.frm1 = tk.Frame(self.master)
        self.frm1.pack(side='left', anchor='nw', padx=5, pady=20)

        self.combo_crop = ttk.Combobox(self.frm1, values=sorted(list(
            self.df["Crop"].unique())), state='readonly')
        self.combo_crop.pack()
        self.combo_crop.bind("<<ComboboxSelected>>", self.select_crop)

        self.combo_location = ttk.Combobox(self.frm1, values=sorted(list(
            self.df["Location"].unique())), state='readonly')
        self.combo_location.pack(side=BOTTOM)
        self.combo_location.bind("<<ComboboxSelected>>", self.select_location)

        self.lbl_crop = tk.Label(self.frm1, text="\u2191 Select Crop \u2191")
        self.lbl_crop.pack(side=TOP)

        self.lbl_location = tk.Label(
            self.frm1, text="\u2193 Select Location \u2193")
        self.lbl_location.pack()

        # !####################################################################
        # ! Bug - Scrollbar fills the entire bottom of the screen and throws
        # ! errors every time it moves?????
        self.scrollx = ttk.Scrollbar(self.master, orient=HORIZONTAL)
        self.scrollx.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.tree.set)
        self.scrollx.pack(side='bottom', fill='x')
        # !####################################################################

        self.tree["columns"] = columns
        self.tree.pack(expand=True, fill=BOTH)

        for i in columns:
            self.tree.column(i, anchor='w')
            self.tree.heading(i, text=i, anchor='w')

        for index, row in self.df.iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

    def select_crop(self, event=None):
        self.tree.delete(*self.tree.get_children())
        for index, row in self.df.loc[self.df["Crop"].eq(self.combo_crop.get())].iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

    def select_location(self, event=None):
        self.tree.delete(*self.tree.get_children())
        for index, row in self.df.loc[self.df["Location"].eq(self.combo_location.get())].iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

    def show(self):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 1024
        h = 1024
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)


class HistoryView(object):
    """ Show the history view window. """

    def __init__(self, master, barcode):
        self.master = tk.Toplevel(master)
        self.master.title("History")
        self.master.grab_set()
        self.master.resizable(False, False)
        self.master.state("zoomed")

        self.df = sql_history_dataframe(barcode)
        self.df["Variety ID"] = self.df["Variety ID"].fillna(0).astype(int)

        self.df["Germ %"].fillna(value="None", inplace=True)
        self.df["TKW (g)"].fillna(value="None", inplace=True)

        self.tree = ttk.Treeview(self.master)
        self.tree['show'] = 'headings'
        columns = list(self.df.columns)

        self.scrollx = ttk.Scrollbar(self.master, orient=HORIZONTAL)
        self.scrollx.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.tree.set)
        self.scrollx.pack(side='bottom', fill='x')

        self.tree["columns"] = columns
        self.tree.pack(expand=True, fill=BOTH)

        for i in columns:
            self.tree.column(i, anchor='w')
            self.tree.heading(i, text=i, anchor='w')

        for index, row in self.df.iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

    def show(self):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 1024
        h = 1024
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)


def main():
    """ Run the program. """
    create_version()
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
