# Brian Beard

# Find menu class file.

# imports
from datetime import datetime
from datetime import date
from sqlite3.dbapi2 import Cursor, Error, version
import tkinter as tk
from tkinter import Button, IntVar, StringVar, messagebox
from pathlib import Path
import sqlite3 as sql
from tkinter import font
from tkinter.constants import BOTH, BOTTOM, CENTER, E, END, HIDDEN, HORIZONTAL, N, S, TOP, W
import pandas as pd
from tkinter import ttk
import sys
import traceback
from docx import *
import os


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
DATA_PATH = OUTPUT_PATH / Path("./data")

program_version = "0.1.0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def relative_to_data(path: str) -> Path:
    return DATA_PATH / Path(path)


# Global database variables
currentdb = relative_to_assets("currentcrops.db")
archivedb = relative_to_assets("archivecrops.db")


def create_connection(db_file):
    """ Create the connection to the database. """
    conn = None

    try:
        conn = sql.connect(db_file)
        return conn

    except sql.Error as e:
        print(e)


def select_by_barcode(barcode=None):
    """ Sort by barcode. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""SELECT * FROM currentcrop WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()

        for i in result:
            return i


def update_quantity(value, barcode):
    """ Updates the quantity in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Quantity (g)" = {round(value, 2)} WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def update_location(value, barcode):
    """ Updates the location in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Location" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def update_notes(value, barcode):
    """ Updates the notes in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Notes" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def update_germ(value, barcode):
    """ Updates the germ in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Germ %" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def update_tkw(value, barcode):
    """ Updates the tkw in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "TKW (g)" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def update_date(value, barcode):
    """ Updates the date to the current date in the database. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""UPDATE currentcrop SET "Date Edited" = '{value}' WHERE "Barcode ID" = '{barcode}'"""

    try:
        cursor.execute(sql)
        conn.commit()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()


def max_variety_id():
    """ Finds the max variety id and adds one. """
    conn = create_connection(relative_to_assets(currentdb))
    cursor = conn.cursor()

    sql = f"""SELECT MAX("Variety ID") FROM currentcrop"""

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except sql.Error as e:
        print(e)

    finally:
        conn.close()

        for i in result:
            return i


def add_entry(barcode, varietyid, varietyname, crop, source, year, quantity, germ, tkw, location, designation, entrant, notes, date):
    """ Add a new row to the database. """
    conn1 = create_connection(relative_to_assets(currentdb))
    conn2 = create_connection(relative_to_assets(archivedb))

    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()

    sql1 = f"""INSERT INTO currentcrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    sql2 = f"""INSERT INTO archivecrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    record = (barcode, varietyid, varietyname, crop, source, year,
              quantity, germ, tkw, location, designation, entrant, notes, date)

    try:
        cursor1.execute(sql1, record)
        cursor2.execute(sql2, record)
        conn1.commit()
        conn2.commit()

    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        conn1.close()
        conn2.close()


def add_to_archive(barcode, varietyid, varietyname, crop, source, year, quantity, germ, tkw, location, designation, entrant, notes, date):
    """ Add an entry to the archive when a change is made. """
    conn = create_connection(relative_to_assets(archivedb))
    cursor = conn.cursor()

    sql = f"""INSERT INTO archivecrop ("Barcode ID", "Variety ID", "Variety", "Crop", "Source", "Year (rcv)", "Quantity (g)", "Germ %", "TKW (g)", "Location", "Designation / Project", "Entrant", "Notes", "Date Edited") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

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
        conn.close()


def sql_to_dataframe():
    """ Take the current database and return a dataframe. """
    conn = create_connection(relative_to_assets(currentdb))

    sql = f"""SELECT * FROM currentcrop"""
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=['Barcode ID', 'Variety ID', 'Variety', 'Crop', 'Source', 'Year (rcv)',
                      'Quantity (g)', 'Germ %', 'TKW (g)', 'Location', 'Designation / Project', 'Entrant', 'Notes', 'Date Edited'])

    conn.close()
    return df


def sql_to_dataframe_recent():
    """ Take the current database and return a dataframe with the latest 10 entries only """
    conn = create_connection(relative_to_assets(currentdb))

    sql = f"""SELECT * FROM currentcrop ORDER BY "Date Edited" LIMIT 10"""
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=['Barcode ID', 'Variety ID', 'Variety', 'Crop', 'Source', 'Year (rcv)',
                      'Quantity (g)', 'Germ %', 'TKW (g)', 'Location', 'Designation / Project', 'Entrant', 'Notes', 'Date Edited'])

    conn.close()
    print(df)
    return df


def sql_history_dataframe(barcode):
    """ Return a dataframe of a specific barcode in archive. """
    conn = create_connection(relative_to_assets(archivedb))

    sql = f"""SELECT * FROM archivecrop WHERE "Barcode ID" = '{barcode}' ORDER BY "Date Edited" DESC"""
    sql_query = pd.read_sql_query(sql, conn)

    df = pd.DataFrame(sql_query, columns=['Barcode ID', 'Variety ID', 'Variety', 'Crop', 'Source', 'Year (rcv)',

                      'Quantity (g)', 'Germ %', 'TKW (g)', 'Location', 'Designation / Project', 'Entrant', 'Notes', 'Date Edited'])

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
            y=341,
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
            command=self.word_export,
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

    def archive_on_update(self):
        """ Retrieve all the text for archiving purposes. """
        try:
            barcode = self.text_barcode.get()
            varietyid = self.text_variety_id.get()
            varietyname = self.text_variety_name.get()
            crop = self.text_crop.get()
            source = self.text_source.get()
            year = self.text_year.get()
            quantityold = self.text_quantity.get()
            quantityfloat = float(quantityold)
            quantity = int(quantityfloat)
            entrant = self.text_entrant.get()
            germold = self.text_germ.get()
            germfloat = float(germold)
            germ = int(germfloat)
            tkw = self.text_tkw.get()
            location = self.text_location.get()
            designation = self.text_designation.get()
            notes = self.text_notes.get()
            date = self.text_date.get()

            add_to_archive(barcode, varietyid, varietyname, crop, source, year,
                           quantity, germ, tkw, location, designation, entrant, notes, date)
        except Exception:
            pass

    def date_convert(self):
        """ Convert date to correct format. """
        date = self.show_results(13)
        if len(date) == 10:
            return date
        else:
            date = date[:10]
            if date:
                return "NA"
            else:
                new_date = datetime.strptime(
                    date, '%Y-%m-%d').strftime('%m/%d/%Y')
                return new_date

    def show_results(self, label_num):
        """ Shows the results in the labels. """

        input = self.lbl_barcode.get()
        list = select_by_barcode(f"{input}")
        if list[label_num] is None:
            return "NA"
        else:
            return list[label_num]

    def current_date(self):
        """ Sets the edited date to current date. """
        today = date.today()
        dateformat = today.strftime('%m/%d/%Y')
        barcode = self.text_barcode.get()
        update_date(dateformat, barcode)
        self.text_date.set(self.show_results(13))

    def add_quantity(self):
        """ Change the quantity. """
        try:
            value = QuantityPopupAdd(self).show()
            original = self.text_quantity.get()
            new = float(original) + value
            barcode = self.text_barcode.get()
            update_quantity(new, barcode)
            self.current_date()
            self.text_quantity.set(float(self.show_results(6)))
        except Exception:
            pass

    def remove_quantity(self):
        """ Change the quantity. """
        try:
            value = QuantityPopupRemove(self).show()

            original = self.text_quantity.get()
            new = float(original) - value

            barcode = self.text_barcode.get()
            update_quantity(new, barcode)
            self.current_date()
            self.text_quantity.set(float(self.show_results(6)))
        except Exception:
            pass

    def change_location(self):
        """ Change the location field. """
        try:
            value = LocationChangePopup(self).show()

            barcode = self.text_barcode.get()
            update_location(value, barcode)
            self.current_date()
            self.text_location.set(self.show_results(9))
        except Exception:
            pass

    def change_notes(self):
        """ Change the notes field. """
        try:
            value = NotesChangePopup(self).show()
            value = f'"{value}"'

            barcode = self.text_barcode.get()
            update_notes(value, barcode)
            self.current_date()
            self.text_notes.set(self.show_results(12))
        except Exception:
            pass

    def change_germ(self):
        """ Change the germ field. """
        try:
            value = GermTKWChangePopup(self).show()

            barcode = self.text_barcode.get()
            update_germ(value, barcode)
            self.current_date()
            self.text_germ.set(float(self.show_results(7)))
        except Exception:
            pass

    def change_tkw(self):
        """ Change the tkw field. """
        try:
            value = GermTKWChangePopup(self).show()
            barcode = self.text_barcode.get()
            update_tkw(value, barcode)
            self.current_date()
            self.text_tkw.set(float(self.show_results(8)))
        except Exception:
            pass

    def get_barcode(self):
        """ Get the barcode scan from the scanner. """
        try:
            value = BarcodePopup(self).show()
            value = value.strip()
            self.text_barcode.set(value)
            self.update_labels()
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
        barcode = self.text_barcode.get()
        print(barcode)
        HistoryView(self, barcode).show()

    def word_export(self):
        """ Export the barcode to a word file. """
        barcode = self.text_barcode.get()
        document = Document()
        document.add_paragraph(str(barcode))
        document.save(relative_to_data('tmp.docx'))
        os.startfile(relative_to_data('tmp.docx'))


class MainMenuBar(tk.Menu):
    """ Class for main menu bar. """

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        filemenu = tk.Menu(self, tearoff=False)

        self.add_cascade(label="File", underline=0, menu=filemenu)

        filemenu.add_command(label="Recent Barcodes", command=None)
        filemenu.add_command(label="About", command=self.about)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close)

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

        self.lbl = tk.Label(
            self.master, text=f"SeedArchive v{program_version}\n2021 Beard Industries")
        self.lbl.place(relx=.5, rely=.3, anchor='center')

        self.btn = tk.Button(self.master, anchor='center',
                             width=7, height=2, text="OK", command=self.close)
        self.btn.pack(side="bottom", pady=5)

    def close(self):
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
                         width=5, textvariable=self.text_quantity_remove)
        entry.pack(pady=10, padx=5)
        entry.focus()

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
        self.master.title("Edit Location")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.location_change = tk.StringVar()

        self.locations = ('Cabinet 1 / Shelf 1', 'Cabinet 1 / Shelf 2', 'Cabinet 1 / Shelf 3', 'Cabinet 1 / Shelf 4', 'Cabinet 1 / Shelf 5', 'Cabinet 2 / Shelf 1', 'Cabinet 2 / Shelf 2', 'Cabinet 2 / Shelf 3', 'Cabinet 2 / Shelf 4', 'Cabinet 2 / Shelf 5', 'Cabinet 3 / Shelf 1', 'Cabinet 3 / Shelf 2', 'Cabinet 3 / Shelf 3', 'Cabinet 3 / Shelf 4', 'Cabinet 3 / Shelf 5', 'Cabinet 4 / Shelf 1', 'Cabinet 4 / Shelf 2', 'Cabinet 4 / Shelf 3', 'Cabinet 4 / Shelf 4',
                          'Cabinet 4 / Shelf 5', 'Cabinet 5 / Shelf 1', 'Cabinet 5 / Shelf 2', 'Cabinet 5 / Shelf 3', 'Cabinet 5 / Shelf 4', 'Cabinet 5 / Shelf 5', 'Cabinet 6 / Shelf 1', 'Cabinet 6 / Shelf 2', 'Cabinet 6 / Shelf 3', 'Cabinet 6 / Shelf 4', 'Cabinet 6 / Shelf 5', 'Cabinet 7 / Shelf 1', 'Cabinet 7 / Shelf 2', 'Cabinet 7 / Shelf 3', 'Cabinet 7 / Shelf 4', 'Cabinet 7 / Shelf 5', 'Cabinet 8 / Shelf 1', 'Cabinet 8 / Shelf 2', 'Cabinet 8 / Shelf 3', 'Cabinet 8 / Shelf 4', 'Cabinet 8 / Shelf 5', 'Cabinet 9 / Shelf 1', 'Cabinet 9 / Shelf 2', 'Cabinet 9 / Shelf 3', 'Cabinet 9 / Shelf 4', 'Cabinet 9 / Shelf 5', 'Cabinet 10 / Shelf 1', 'Cabinet 10 / Shelf 2', 'Cabinet 10 / Shelf 3', 'Cabinet 10 / Shelf 4', 'Cabinet 10 / Shelf 5', 'Cabinet 11 / Shelf 1', 'Cabinet 11 / Shelf 2', 'Cabinet 11 / Shelf 3', 'Cabinet 11 / Shelf 4', 'Cabinet 11 / Shelf 5', 'Open Shelf 1 / Shelf 1', 'Open Shelf 1 / Shelf 2', 'Open Shelf 1 / Shelf 3', 'Open Shelf 1 / Shelf 4', 'Open Shelf 2 / Shelf 1', 'Open Shelf 2 / Shelf 2', 'Open Shelf 2 / Shelf 3', 'Open Shelf 2 / Shelf 4', 'Open Shelf 2 / Shelf 5', 'Cart', 'THROWN OUT')

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Enter new value:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        self.location_menu = tk.OptionMenu(
            frm2,
            self.location_change,
            *self.locations,
            command=None
        )
        self.location_menu.pack()

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

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


class BarcodePopup(object):
    """ Germ edit window. """

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Scan")
        self.master.grab_set()
        self.master.focus_force()
        self.master.resizable(False, False)

        self.text_barcode = tk.StringVar()

        frm1 = tk.Frame(self.master, padx=5, pady=5)
        frm1.grid(row=0, column=1)

        lbl = tk.Label(frm1, text="Scan barcode now:", pady=5,
                       padx=5).pack()

        frm2 = tk.Frame(self.master, padx=5, pady=5)
        frm2.grid(row=0, column=2)

        entry = tk.Entry(frm2, justify='center',
                         width=20, textvariable=self.text_barcode)
        entry.pack(pady=10, padx=5)
        entry.focus()
        entry.bind('<Return>', self.close)

        btn = tk.Button(self.master, text="Accept", padx=10, command=self.master.destroy).grid(
            row=1, columnspan=5, pady=5)

    def close(self, event=None):
        self.master.destroy()

    def show(self):
        """ Show the quantity window and return the grams to remove. """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 350
        h = 90
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.attributes('-topmost', True)

        self.master.deiconify()
        self.master.wait_window()
        value = self.text_barcode.get()
        return value


class EntryMenu(object):
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("New Entry")
        self.master.grab_set()
        self.master.resizable(False, False)

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
            x=757,
            y=503,
            width=164,
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

        self.canvas.create_text(
            624.0,
            509.0,
            anchor="nw",
            text="Date Edited",
            fill="#000000",
            font=("Roboto Bold", 24 * -1)
        )

        self.canvas.create_rectangle(
            757.0,
            503.0,
            921.0,
            543.0,
            fill="#C4C4C4",
            outline="")

        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets(("accept.png")))
        self.but_accept = tk.Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.master.destroy,
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
        """ Display the current date. """
        today = date.today()
        dateformat = today.strftime('%m/%d/%Y')
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
        print(str(year_rcv[1:]))

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
            return "NA"

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
            return "NA"

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

        self.tree = ttk.Treeview(self.master)
        self.tree['show'] = 'headings'
        columns = list(self.df.columns)

        self.frm1 = tk.Frame(self.master)
        self.frm1.pack(side='left', anchor='nw', padx=5, pady=20)

        self.combo_crop = ttk.Combobox(self.frm1, values=list(
            self.df["Crop"].unique()), state='readonly')
        self.combo_crop.pack(side=BOTTOM)
        self.combo_crop.bind("<<ComboboxSelected>>", self.select_crop)

        self.lbl_crop = tk.Label(self.frm1, text="Select Crop")
        self.lbl_crop.pack(side=TOP)

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

        barcode = barcode

        self.df = sql_history_dataframe(barcode)
        self.df["Variety ID"] = self.df["Variety ID"].fillna(0).astype(int)

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
